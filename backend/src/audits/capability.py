"""Capability/depth audits.

Detects shallow zombie agents vs deep capable life.

Questions:
- Action diversity per agent (>3 distinct action_types over the run)
- Are relations forming? (any non-zero relation in dict)
- Is knowledge spreading? (TEACH events with success)
- Is memoria growing? (memoria_recent > 0)
- Are agents reflecting? (REFLECT count > 0 ideally per agent)
- Are artifacts being produced?
- Is the civilization producing institutions/rituals/posts?
"""
from collections import Counter
from sqlalchemy.orm import Session

from ..db.schema import (
    Agent, ActionLog, TextArtifact, CodeArtifact,
    Institution, Ritual, Post, Dilema,
)
from .base import AuditCheck


def check_action_diversity(session: Session) -> AuditCheck:
    flagged = []
    for agent in session.query(Agent).all():
        types = (
            session.query(ActionLog.action_type)
            .filter_by(agent_id=agent.id, status="accept")
            .distinct()
            .all()
        )
        ntypes = len(types)
        if ntypes < 3:
            flagged.append({"agent": agent.id, "distinct_actions": ntypes,
                            "tipos": [t[0] for t in types]})
    status = "PASS" if not flagged else "WARN"
    return AuditCheck(
        name="action_diversity_per_agent", category="capability", status=status,
        summary=(f"{len(flagged)} agentes con <3 tipos de accion distintos "
                 f"(zombie behavior risk)"
                 if flagged else "todos los agentes con diversidad de accion >= 3"),
        items=flagged, metric=len(flagged), threshold=3,
    )


def check_relations_forming(session: Session) -> AuditCheck:
    no_rel = []
    for agent in session.query(Agent).all():
        rel = agent.relaciones or {}
        if not rel or all(v == 0 for v in rel.values()):
            no_rel.append(agent.id)
    status = "PASS" if not no_rel else "INFO"
    return AuditCheck(
        name="relations_forming", category="capability", status=status,
        summary=(f"{len(no_rel)} agentes sin relaciones registradas "
                 f"(esperado en runs cortos; warn si persiste post-Day 3)"
                 if no_rel else "todos los agentes tienen relaciones"),
        items=[{"agent": a} for a in no_rel], metric=len(no_rel),
    )


def check_knowledge_spreading(session: Session) -> AuditCheck:
    teaches = (
        session.query(ActionLog)
        .filter_by(action_type="TEACH", status="accept")
        .count()
    )
    learns = (
        session.query(ActionLog)
        .filter_by(action_type="LEARN", status="accept")
        .count()
    )
    total = teaches + learns
    if total == 0:
        return AuditCheck(
            name="knowledge_spreading", category="capability", status="WARN",
            summary="0 transferencias de conocimiento (TEACH/LEARN). civilizacion estatica.",
            metric=0, threshold=1,
        )
    return AuditCheck(
        name="knowledge_spreading", category="capability", status="PASS",
        summary=f"{teaches} TEACH + {learns} LEARN = {total} transferencias",
        metric=total, threshold=1,
    )


def check_civilization_output(session: Session) -> AuditCheck:
    """A live civ produces stuff. Count macro-artifacts."""
    books = session.query(TextArtifact).filter_by(tipo="book").count()
    letters = session.query(TextArtifact).filter_by(tipo="letter").count()
    code = session.query(CodeArtifact).count()
    inst = session.query(Institution).count()
    rituals = session.query(Ritual).count()
    posts = session.query(Post).count()
    total = books + letters + code + inst + rituals + posts
    items = [{
        "books": books, "letters": letters, "code": code,
        "institutions": inst, "rituals": rituals, "posts": posts,
        "total": total,
    }]
    if total == 0:
        return AuditCheck(name="civilization_output", category="capability",
                          status="FAIL",
                          summary="0 artefactos producidos. civ no esta viva.",
                          items=items, metric=0, threshold=1)
    if total < 3:
        return AuditCheck(name="civilization_output", category="capability",
                          status="WARN",
                          summary=f"{total} artefactos. poca produccion.",
                          items=items, metric=total, threshold=3)
    return AuditCheck(name="civilization_output", category="capability",
                      status="PASS",
                      summary=f"{total} artefactos producidos. civ activa.",
                      items=items, metric=total, threshold=3)


def check_reflection(session: Session) -> AuditCheck:
    """At least 1 REFLECT per agent in the run is healthy. Caveat: cooldown 30 ticks."""
    flagged = []
    for agent in session.query(Agent).all():
        n = (
            session.query(ActionLog)
            .filter_by(agent_id=agent.id, action_type="REFLECT", status="accept")
            .count()
        )
        if n == 0:
            flagged.append({"agent": agent.id, "reflects": 0})
    status = "INFO" if flagged else "PASS"
    return AuditCheck(
        name="reflection_practice", category="capability", status=status,
        summary=(f"{len(flagged)} agentes sin REFLECT registrado"
                 if flagged else "todos los agentes reflexionaron al menos una vez"),
        items=flagged, metric=len(flagged),
    )


def check_acceptance_ratio(session: Session) -> AuditCheck:
    """Anti-bullshit health: rejects existir es BUENO. Pero >50% rejects = agentes
    constantemente intentando imposibles → algo mal en prompts."""
    total = session.query(ActionLog).count()
    if total == 0:
        return AuditCheck(name="acceptance_ratio", category="capability",
                          status="INFO", summary="0 actions logged yet")
    accepts = session.query(ActionLog).filter_by(status="accept").count()
    rejects = total - accepts
    ratio = accepts / total
    if ratio < 0.5:
        return AuditCheck(name="acceptance_ratio", category="capability",
                          status="WARN",
                          summary=f"{accepts}/{total} accept ({ratio:.0%}). "
                                  "Muchos rejects: prompts mal o agentes confundidos.",
                          metric=ratio, threshold=0.5)
    return AuditCheck(name="acceptance_ratio", category="capability",
                      status="PASS",
                      summary=f"{accepts} accepts / {rejects} rejects "
                              f"({ratio:.0%} acceptance). saludable.",
                      metric=ratio, threshold=0.5)


def check_personal_history_growing(session: Session) -> AuditCheck:
    """Pre-Day 3 will be empty (no LLM writing it). Day 3+ should populate."""
    empty = [a.id for a in session.query(Agent).all() if not (a.personal_history or [])]
    return AuditCheck(
        name="personal_history_growing", category="capability",
        status="INFO" if empty else "PASS",
        summary=(f"{len(empty)} agentes sin personal_history "
                 f"(esperado pre-Day 3; expected to grow Day 3+)"
                 if empty else "todos con personal_history poblada"),
        items=[{"agent": a} for a in empty], metric=len(empty),
    )


def run_capability_checks(session: Session) -> list[AuditCheck]:
    return [
        check_action_diversity(session),
        check_relations_forming(session),
        check_knowledge_spreading(session),
        check_civilization_output(session),
        check_reflection(session),
        check_acceptance_ratio(session),
        check_personal_history_growing(session),
    ]
