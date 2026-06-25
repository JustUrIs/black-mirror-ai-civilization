"""Sealed-world audits: detect outside influence beyond authorized channels.

Principle: agents live their lives without external influence. Only authorized
external inputs:
  - tick advancement (system physics: decay, sink)
  - bootstrap (spawning, world init)
  - creator-injected events (Dilema launched via /admin endpoint)
  - explicit agent uploads (seed JSON spawning new agent)

Anything else = leak.

Questions:
- Are there ActionLog entries with agent_id = "system" outside expected events?
- Are there Dilemas without a launched_tick? (unauthorized)
- Are there text artifacts created without an agent author?
- Are there agents whose state changed without a corresponding action_log entry?
  (hard to verify without full diff history — skip for now)
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_

from ..db.schema import (
    Agent, ActionLog, TextArtifact, CodeArtifact, Institution,
    Ritual, Dilema, DilemaResponse, Post,
)
from .base import AuditCheck


# Allowed non-agent action_log entries (system-originated, audited)
ALLOWED_SYSTEM_AGENTS = {"system", "creator", "bootstrap"}
ALLOWED_SYSTEM_ACTIONS = {"AUTO_PROMOTE", "TICK_DECAY", "SINK_TAX", "BOOTSTRAP"}


def check_action_log_origins(session: Session) -> AuditCheck:
    """All accepted actions should have agent_id matching a real agent OR be in
    the allowed system list."""
    agent_ids = {a.id for a in session.query(Agent).all()}
    bad = []
    for entry in session.query(ActionLog).all():
        if entry.agent_id in agent_ids:
            continue
        if entry.agent_id in ALLOWED_SYSTEM_AGENTS:
            continue
        bad.append({"tick": entry.tick, "agent_id": entry.agent_id,
                    "action": entry.action_type})
    status = "PASS" if not bad else "FAIL"
    return AuditCheck(
        name="action_log_origins", category="sealed_world", status=status,
        summary=(f"{len(bad)} entradas en ActionLog sin origen agente conocido "
                 "ni sistema autorizado"
                 if bad else "todas las acciones tienen origen autorizado"),
        items=bad[:10], metric=len(bad),
    )


def check_artifacts_have_authors(session: Session) -> AuditCheck:
    agent_ids = {a.id for a in session.query(Agent).all()}
    orphans = []
    for t in session.query(TextArtifact).all():
        if not t.autor_id or t.autor_id not in agent_ids:
            orphans.append({"type": "text_artifact", "id": t.id,
                            "autor_id": t.autor_id, "titulo": t.titulo})
    for c in session.query(CodeArtifact).all():
        if not c.autor_id or c.autor_id not in agent_ids:
            orphans.append({"type": "code_artifact", "id": c.id,
                            "autor_id": c.autor_id})
    for p in session.query(Post).all():
        if not p.autor_id or p.autor_id not in agent_ids:
            orphans.append({"type": "post", "id": p.id,
                            "autor_id": p.autor_id})
    status = "PASS" if not orphans else "FAIL"
    return AuditCheck(
        name="artifacts_have_authors", category="sealed_world", status=status,
        summary=(f"{len(orphans)} artefactos sin autor agente valido"
                 if orphans else "todos los artefactos tienen autor agente"),
        items=orphans[:10], metric=len(orphans),
    )


def check_dilemas_authorized(session: Session) -> AuditCheck:
    """Dilemas without launched_tick or with launched_tick == 0 are suspicious."""
    bad = []
    for d in session.query(Dilema).all():
        if d.launched_tick is None or d.launched_tick < 0:
            bad.append({"id": d.id, "texto": d.texto[:80],
                        "launched_tick": d.launched_tick})
    status = "PASS" if not bad else "WARN"
    return AuditCheck(
        name="dilemas_authorized", category="sealed_world", status=status,
        summary=(f"{len(bad)} dilemas sin tick valido"
                 if bad else "todos los dilemas con tick autorizado"),
        items=bad, metric=len(bad),
    )


def check_dilema_responses_match_agents(session: Session) -> AuditCheck:
    agent_ids = {a.id for a in session.query(Agent).all()}
    bad = []
    for r in session.query(DilemaResponse).all():
        if r.agent_id not in agent_ids:
            bad.append({"id": r.id, "dilema": r.dilema_id, "agent": r.agent_id})
    status = "PASS" if not bad else "FAIL"
    return AuditCheck(
        name="dilema_responses_match_agents", category="sealed_world", status=status,
        summary=(f"{len(bad)} respuestas de agentes inexistentes"
                 if bad else "respuestas atadas a agentes reales"),
        items=bad, metric=len(bad),
    )


def check_inventory_origin(session: Session) -> AuditCheck:
    """Check that no agent suddenly has an item that wasn't gathered, traded,
    given, or part of starting_inventory."""
    # Heuristic: just count items that look "auto-generated" (id starts with
    # something common). For deeper audit we'd need full provenance ledger.
    return AuditCheck(
        name="inventory_origin", category="sealed_world", status="INFO",
        summary="inventory origin auditing requires per-item provenance ledger (post-MVP)",
    )


def run_sealed_world_checks(session: Session) -> list[AuditCheck]:
    return [
        check_action_log_origins(session),
        check_artifacts_have_authors(session),
        check_dilemas_authorized(session),
        check_dilema_responses_match_agents(session),
        check_inventory_origin(session),
    ]
