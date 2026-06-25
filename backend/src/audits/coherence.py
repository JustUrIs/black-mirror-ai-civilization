"""Coherence audits: artifacts vs world ontology.

Questions:
- Do books mention things that don't exist in this world?
- Do laws reference impossibilities?
- Do rituals reference astronomical/seasonal phenomena that aren't wired?
- Are agents using techs above this world's tech_level?
"""
from sqlalchemy.orm import Session

from ..db.schema import (
    WorldState, TextArtifact, PendingInstitution, PendingRitual,
    Institution, Ritual, Post, ActionLog,
)
from .base import AuditCheck


def _denylist(world_state) -> set[str]:
    o = (world_state.world_ontology if world_state else None) or {}
    return {v.lower() for v in (o.get("no_existe") or []) if isinstance(v, str)}


def _allowed_tokens(world_state) -> set[str]:
    o = (world_state.world_ontology if world_state else None) or {}
    out: set[str] = set()
    for k, vals in o.items():
        if k in ("_doc", "no_existe"):
            continue
        if isinstance(vals, list):
            for v in vals:
                if isinstance(v, str):
                    out.add(v.lower())
    return out


def _find_violations(text: str, deny: set[str]) -> list[str]:
    if not text:
        return []
    txt = text.lower()
    return sorted(t for t in deny if t in txt)


def check_books_coherence(session: Session, ws: WorldState) -> AuditCheck:
    deny = _denylist(ws)
    if not deny:
        return AuditCheck(name="books_coherence", category="coherence",
                          status="INFO", summary="no denylist defined")
    violations = []
    for b in session.query(TextArtifact).filter_by(tipo="book").all():
        hits = _find_violations(b.contenido or "", deny)
        if hits:
            violations.append({"id": b.id, "titulo": b.titulo, "autor": b.autor_id,
                               "tokens_inexistentes": hits, "tick": b.tick})
    status = "PASS" if not violations else ("WARN" if len(violations) <= 2 else "FAIL")
    return AuditCheck(
        name="books_coherence", category="coherence", status=status,
        summary=(f"{len(violations)} libros mencionan tokens del 'no_existe' del mundo"
                 if violations else "todos los libros coherentes con la ontologia"),
        items=violations, metric=len(violations), threshold=0,
    )


def check_letters_coherence(session: Session, ws: WorldState) -> AuditCheck:
    deny = _denylist(ws)
    if not deny:
        return AuditCheck(name="letters_coherence", category="coherence",
                          status="INFO", summary="no denylist defined")
    violations = []
    for l in session.query(TextArtifact).filter_by(tipo="letter").all():
        hits = _find_violations(l.contenido or "", deny)
        if hits:
            violations.append({"id": l.id, "destinatario": l.titulo,
                               "autor": l.autor_id, "tokens_inexistentes": hits})
    status = "PASS" if not violations else "WARN"
    return AuditCheck(
        name="letters_coherence", category="coherence", status=status,
        summary=(f"{len(violations)} cartas mencionan tokens no_existe"
                 if violations else "todas las cartas coherentes"),
        items=violations, metric=len(violations), threshold=0,
    )


def check_institutions_coherence(session: Session, ws: WorldState) -> AuditCheck:
    deny = _denylist(ws)
    if not deny:
        return AuditCheck(name="institutions_coherence", category="coherence",
                          status="INFO", summary="no denylist")
    violations = []
    for i in session.query(Institution).all():
        hits = _find_violations(i.texto or "", deny)
        if hits:
            violations.append({"id": i.id, "nombre": i.nombre, "tokens": hits})
    status = "PASS" if not violations else "FAIL"
    return AuditCheck(
        name="institutions_coherence", category="coherence", status=status,
        summary=(f"{len(violations)} leyes ratificadas mencionan cosas inexistentes "
                 f"-- problema serio: la civilizacion vota por cosas que no existen"
                 if violations else "leyes ratificadas coherentes"),
        items=violations, metric=len(violations), threshold=0,
    )


def check_rituals_coherence(session: Session, ws: WorldState) -> AuditCheck:
    deny = _denylist(ws)
    if not deny:
        return AuditCheck(name="rituals_coherence", category="coherence",
                          status="INFO", summary="no denylist")
    violations = []
    for r in list(session.query(Ritual).all()) + list(session.query(PendingRitual).all()):
        combined = (r.descripcion or "") + " " + (r.frecuencia or "") + " " + (r.mci_concept or "")
        hits = _find_violations(combined, deny)
        if hits:
            violations.append({"id": r.id, "nombre": r.nombre, "tokens": hits})
    status = "PASS" if not violations else "WARN"
    return AuditCheck(
        name="rituals_coherence", category="coherence", status=status,
        summary=(f"{len(violations)} rituales referencian cosas no_existe"
                 if violations else "rituales coherentes"),
        items=violations, metric=len(violations), threshold=0,
    )


def check_posts_coherence(session: Session, ws: WorldState) -> AuditCheck:
    deny = _denylist(ws)
    if not deny:
        return AuditCheck(name="posts_coherence", category="coherence",
                          status="INFO", summary="no denylist")
    violations = []
    for p in session.query(Post).all():
        hits = _find_violations(p.contenido or "", deny)
        if hits:
            violations.append({"id": p.id, "autor": p.autor_id, "tokens": hits})
    status = "PASS" if not violations else "WARN"
    return AuditCheck(
        name="posts_coherence", category="coherence", status=status,
        summary=(f"{len(violations)} posts mencionan no_existe"
                 if violations else "posts coherentes"),
        items=violations, metric=len(violations), threshold=0,
    )


def check_tech_level_consistency(session: Session, ws: WorldState) -> AuditCheck:
    """Detect action_log entries inconsistent with this world's tech_level."""
    if not ws or ws.tech_level not in ("stone", "bronze", "modern", "post"):
        return AuditCheck(name="tech_level_consistency", category="coherence",
                          status="INFO", summary="tech_level not set")
    blocked_by_level = {
        "stone": {"WRITE_CODE", "WRITE_BOOK", "WRITE_LETTER", "READ", "POST"},
        "bronze": {"WRITE_CODE", "POST"},
        "modern": set(),
        "post": set(),
    }
    blocked = blocked_by_level.get(ws.tech_level, set())
    if not blocked:
        return AuditCheck(name="tech_level_consistency", category="coherence",
                          status="PASS",
                          summary=f"tech_level={ws.tech_level}: todas las acciones permitidas")
    violations = (
        session.query(ActionLog)
        .filter(ActionLog.status == "accept")
        .filter(ActionLog.action_type.in_(blocked))
        .all()
    )
    if not violations:
        return AuditCheck(name="tech_level_consistency", category="coherence",
                          status="PASS",
                          summary=f"sin violaciones de tech_level={ws.tech_level}")
    items = [{"tick": v.tick, "agent": v.agent_id, "action": v.action_type} for v in violations[:10]]
    return AuditCheck(
        name="tech_level_consistency", category="coherence", status="FAIL",
        summary=f"{len(violations)} acciones violan tech_level={ws.tech_level}",
        items=items, metric=len(violations),
    )


def run_coherence_checks(session: Session, ws: WorldState) -> list[AuditCheck]:
    return [
        check_books_coherence(session, ws),
        check_letters_coherence(session, ws),
        check_institutions_coherence(session, ws),
        check_rituals_coherence(session, ws),
        check_posts_coherence(session, ws),
        check_tech_level_consistency(session, ws),
    ]
