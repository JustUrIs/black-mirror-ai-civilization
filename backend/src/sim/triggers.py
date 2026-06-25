"""Trigger classification (PLAN_v4.md §4).

4 trigger types determine how/whether an agent decides this tick:

1. crit_need    — necesidad fisica critica. Forzado, subset acciones permitidas.
2. crit_event   — evento externo critico (dilema activo, muerte cercana, ataque).
                  Forzado, respuesta obligatoria.
3. observation  — alguien hizo algo importante. Micro LLM call (no accion, solo memoria).
4. normal       — tick normal. LLM full prompt.
5. skip         — no LLM call este tick (cooldown N ticks, ahorro costo).

Subset of allowed actions for crit_need:
  hambre/energia/sed → GATHER, EAT, DRINK, SLEEP, MOVE
  salud baja        → FLEE-ish via MOVE, BEG via TALK, GIFT receive
"""
from dataclasses import dataclass, field
from typing import Literal

from ..db.schema import Agent, ActionLog, Dilema


TriggerKind = Literal["crit_need", "crit_event", "observation", "normal", "skip"]


@dataclass
class Trigger:
    kind: TriggerKind
    forced_subset: list[str] = field(default_factory=list)
    context_extra: dict = field(default_factory=dict)
    reason: str = ""


# Thresholds (PLAN_v4.md §4.1)
CRIT_HAMBRE_THRESHOLD = 80.0
CRIT_SED_THRESHOLD = 80.0
CRIT_ENERGIA_THRESHOLD = 20.0
CRIT_SALUD_THRESHOLD = 30.0

NORMAL_TICK_INTERVAL = 3  # full prompt every N ticks for non-critical agents


def _check_crit_need(agent: Agent) -> Trigger | None:
    n = agent.necesidades or {}
    if n.get("hambre", 0) >= CRIT_HAMBRE_THRESHOLD:
        return Trigger(
            kind="crit_need",
            forced_subset=["GATHER", "EAT", "MOVE", "TRADE", "TALK"],
            context_extra={"urgency": "hambre", "level": n.get("hambre")},
            reason=f"hambre critica ({n.get('hambre'):.0f}/100)",
        )
    if n.get("sed", 0) >= CRIT_SED_THRESHOLD:
        return Trigger(
            kind="crit_need",
            forced_subset=["DRINK", "GATHER", "MOVE"],
            context_extra={"urgency": "sed", "level": n.get("sed")},
            reason=f"sed critica ({n.get('sed'):.0f}/100)",
        )
    if n.get("energia", 100) <= CRIT_ENERGIA_THRESHOLD:
        return Trigger(
            kind="crit_need",
            forced_subset=["SLEEP", "EAT", "REFLECT"],
            context_extra={"urgency": "energia", "level": n.get("energia")},
            reason=f"energia critica ({n.get('energia'):.0f}/100)",
        )
    if (agent.salud or 100) <= CRIT_SALUD_THRESHOLD:
        return Trigger(
            kind="crit_need",
            forced_subset=["MOVE", "TALK", "GIFT", "TRADE"],
            context_extra={"urgency": "salud", "level": agent.salud},
            reason=f"salud critica ({agent.salud:.0f}/100)",
        )
    return None


def _check_crit_event(agent: Agent, session, tick: int) -> Trigger | None:
    # Active dilema → forced response
    active_dilema = session.query(Dilema).filter_by(active=True).order_by(Dilema.id.desc()).first()
    if active_dilema is not None:
        from ..db.schema import DilemaResponse
        already = session.query(DilemaResponse).filter_by(
            dilema_id=active_dilema.id, agent_id=agent.id
        ).first()
        if already is None:
            return Trigger(
                kind="crit_event",
                forced_subset=["RESPOND_TO_GOD"],
                context_extra={"dilema_id": active_dilema.id, "dilema_texto": active_dilema.texto},
                reason=f"dilema activo {active_dilema.id}",
            )
    # Recent ATTACK against self in last 2 ticks
    recent_attack = session.query(ActionLog).filter(
        ActionLog.tick >= tick - 2,
        ActionLog.action_type == "ATTACK",
        ActionLog.status == "accept",
    ).all()
    for atk in recent_attack:
        params = atk.params or {}
        if params.get("agente") == agent.id:
            return Trigger(
                kind="crit_event",
                forced_subset=["MOVE", "TALK", "ATTACK", "GIFT"],
                context_extra={"attacker": atk.agent_id, "tick": atk.tick},
                reason=f"fuiste atacado por {atk.agent_id} en tick {atk.tick}",
            )
    return None


def _check_observation(agent: Agent, session, tick: int) -> Trigger | None:
    """Recent notable events at agent.ubicacion or involving agent's relations."""
    # Recent artefacts produced THIS tick at same location
    notable = session.query(ActionLog).filter(
        ActionLog.tick == tick,
        ActionLog.status == "accept",
        ActionLog.action_type.in_([
            "WRITE_BOOK", "WRITE_CODE", "PROPOSE_INSTITUTION", "PROPOSE_RITUAL"
        ]),
        ActionLog.agent_id != agent.id,
    ).all()
    if notable:
        return Trigger(
            kind="observation",
            forced_subset=[],  # no forced action; just micro LLM
            context_extra={"events": [{"actor": l.agent_id, "type": l.action_type} for l in notable]},
            reason=f"{len(notable)} eventos notables observados",
        )
    return None


def classify_trigger(agent: Agent, session, tick: int) -> Trigger:
    """Return the most urgent trigger applying to agent at tick.
    Priority: crit_need > crit_event > observation > normal/skip.
    """
    t = _check_crit_need(agent)
    if t: return t
    t = _check_crit_event(agent, session, tick)
    if t: return t
    t = _check_observation(agent, session, tick)
    if t: return t

    # Normal vs skip — interval-based (cost saving)
    if tick % NORMAL_TICK_INTERVAL == 0:
        return Trigger(kind="normal", reason="tick normal (interval hit)")
    return Trigger(kind="skip", reason=f"skip tick (interval {NORMAL_TICK_INTERVAL})")
