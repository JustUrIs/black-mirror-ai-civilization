"""Emotional state updates from world events.

Cada tick, despues de classify_trigger, este module mira las observations
y actualiza agent.emotional_state + agent.personal_history.

Sin necesitar LLM. Heuristica determinista. Day 5+ LLM puede sobrescribir
con mejor matiz pero esto da el piso.

Mapping de eventos a emociones:
- ATTACK observado          → miedo +25, animo -10
- ATTACK contra self        → miedo +40, dignidad -20 (mas fuerte)
- THROW observado           → miedo +15, asombro +10
- WRITE_BOOK ajeno         → asombro +5
- PROPOSE_INSTITUTION ajeno → curiosidad-like (no campo; usa asombro +5)
- SPAWN_OBJECT creator     → asombro +15, miedo +5
- MOVE_OBJECT creator      → asombro +8
- REVIVE creator           → asombro +20, animo +15
- death cercana            → miedo +20, soledad +10

Decay natural por tick (sin eventos): miedo -1, asombro -1, animo regresa a 50.
"""
import logging
from .triggers import OBSERVABLE_AGENT_ACTIONS, CREATOR_OBSERVABLE_ACTIONS


log = logging.getLogger("emotions")


EMOTION_DEFAULTS = {
    "animo": 50.0,
    "esperanza": 50.0,
    "miedo": 0.0,
    "soledad": 30.0,
    "dignidad": 70.0,
    "verguenza": 0.0,
    "asombro": 30.0,
}


def _clamp(v, lo=0.0, hi=100.0):
    return max(lo, min(hi, v))


def _drift_to_default(es: dict) -> dict:
    """Per-tick natural drift hacia defaults (decay emocional)."""
    out = dict(es) if es else {}
    for k, default in EMOTION_DEFAULTS.items():
        cur = out.get(k, default)
        if cur > default:
            out[k] = _clamp(cur - 0.5)
        elif cur < default:
            out[k] = _clamp(cur + 0.3)
    return out


def apply_event_effects(agent, events: list[dict], history: list[dict]) -> tuple[dict, list[dict]]:
    """Applies emotional deltas to agent based on observed events.

    Returns (new_emotional_state, updated_personal_history).
    """
    es = _drift_to_default(agent.emotional_state)
    ph = list(history or [])
    sig_added = False

    for ev in events:
        actor = ev.get("actor")
        etype = ev.get("type")
        from_creator = ev.get("from_creator", False)
        tick = ev.get("tick")

        if etype == "ATTACK":
            # Si el target del ATTACK era yo (no se en este module) → miedo +40.
            # Aca asumimos observador external (mismo location, no target).
            es["miedo"] = _clamp(es.get("miedo", 0) + 25)
            es["animo"] = _clamp(es.get("animo", 50) - 10)
            ph.append({"tick": tick, "type": "presencie_violencia",
                       "summary": f"{actor} ataco a alguien en {agent.ubicacion}"})
            sig_added = True
        elif etype == "THROW":
            es["miedo"] = _clamp(es.get("miedo", 0) + 15)
            es["asombro"] = _clamp(es.get("asombro", 30) + 10)
        elif etype == "WRITE_BOOK":
            es["asombro"] = _clamp(es.get("asombro", 30) + 5)
        elif etype == "PROPOSE_INSTITUTION":
            es["asombro"] = _clamp(es.get("asombro", 30) + 5)
            es["esperanza"] = _clamp(es.get("esperanza", 50) + 3)
        elif etype == "PROPOSE_RITUAL":
            es["asombro"] = _clamp(es.get("asombro", 30) + 3)
        elif etype == "SPAWN_OBJECT" and from_creator:
            es["asombro"] = _clamp(es.get("asombro", 30) + 15)
            es["miedo"] = _clamp(es.get("miedo", 0) + 5)
            ph.append({"tick": tick, "type": "intervencion_divina",
                       "summary": f"aparecio algo en {agent.ubicacion} sin que nadie lo trajera"})
            sig_added = True
        elif etype == "MOVE_OBJECT" and from_creator:
            es["asombro"] = _clamp(es.get("asombro", 30) + 8)
        elif etype == "REVIVE" and from_creator:
            es["asombro"] = _clamp(es.get("asombro", 30) + 20)
            es["animo"] = _clamp(es.get("animo", 50) + 15)
            ph.append({"tick": tick, "type": "milagro",
                       "summary": "volvi a la vida sin saber como"})
            sig_added = True

    return es, ph


def apply_need_effects(agent) -> dict:
    """Necesidades extremas afectan emotional state."""
    es = dict(agent.emotional_state or {})
    n = agent.necesidades or {}
    if n.get("hambre", 0) >= 70:
        es["animo"] = _clamp(es.get("animo", 50) - 0.5)
        es["esperanza"] = _clamp(es.get("esperanza", 50) - 0.3)
    if n.get("energia", 100) <= 25:
        es["animo"] = _clamp(es.get("animo", 50) - 0.5)
    if (agent.salud or 100) <= 40:
        es["miedo"] = _clamp(es.get("miedo", 0) + 0.5)
        es["dignidad"] = _clamp(es.get("dignidad", 70) - 0.2)
    return es


def update_agent_emotions(agent, observations: list[dict] | None, tick: int) -> None:
    """Mutates agent in place. Call once per tick per agent."""
    new_es, new_ph = apply_event_effects(agent, observations or [], agent.personal_history)
    new_es = {**new_es, **{k: v for k, v in apply_need_effects(agent).items() if k not in new_es}}
    # Merge need effects on top of event effects
    need_es = apply_need_effects(agent)
    for k, v in need_es.items():
        if k in new_es:
            # Average slightly to combine
            new_es[k] = (new_es[k] + v) / 2
        else:
            new_es[k] = v
    agent.emotional_state = new_es
    # Trim personal_history to last 50 events for size
    agent.personal_history = new_ph[-50:]
