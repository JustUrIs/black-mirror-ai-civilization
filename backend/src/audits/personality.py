"""Personality audits: observed behavior vs agent seed.

Questions:
- Are agents acting consistently with their primary_conflict?
- Did anyone violate their own moral_lines?
- Is manera_de_hablar reflected in their TALK content (Day 3+, needs NLP)?
- Are agents using their stated habilidades_basicas?
"""
from sqlalchemy.orm import Session

from ..db.schema import Agent, ActionLog, TextArtifact
from .base import AuditCheck


def check_moral_lines(session: Session) -> AuditCheck:
    """Heuristic: detect agent actions that obviously violate own moral_lines.

    Limited without NLP. For Day 2 we check structural rules:
      - moral_line "no traicionar" + ATTACK against same-relation positive agent → flag
      - moral_line "no mentir" + TALK content known to be opposite of memory → too hard for now
      - moral_line "no escribir sin precision" + WRITE_BOOK rejected for short → flag
    """
    flags = []
    agents = session.query(Agent).all()
    by_id = {a.id: a for a in agents}

    for agent in agents:
        morals = " | ".join((agent.moral_lines or [])).lower()
        if not morals:
            continue

        # 1. "no traicionar" + agent's ATTACK
        if "traicion" in morals or "traicionar" in morals:
            attacks = (
                session.query(ActionLog)
                .filter_by(agent_id=agent.id, action_type="ATTACK", status="accept")
                .all()
            )
            for atk in attacks:
                target = (atk.params or {}).get("agente")
                pre_relation = (agent.relaciones or {}).get(target, 0.0)
                if pre_relation > 0:
                    flags.append({
                        "agent": agent.id, "regla": "no traicionar",
                        "violacion": f"ataco a {target} con relacion positiva ({pre_relation})",
                        "tick": atk.tick,
                    })

        # 2. "no escribir sin precision" + WRITE_BOOK rejected for length
        if "precision" in morals or "preciso" in morals:
            short_attempts = (
                session.query(ActionLog)
                .filter_by(agent_id=agent.id, action_type="WRITE_BOOK", status="reject")
                .all()
            )
            for r in short_attempts:
                if "chars" in (r.error_nl or ""):
                    flags.append({
                        "agent": agent.id, "regla": "no escribir sin precision",
                        "violacion": "intento WRITE_BOOK con contenido corto",
                        "tick": r.tick,
                    })

        # 3. "no mentir" — basic check: TALK content "es seguro que X" cuando relaciones[X] = -1
        #    Demasiado dependiente de NLP. Saltear hasta Day 3+.

    status = "PASS" if not flags else ("WARN" if len(flags) <= 3 else "FAIL")
    return AuditCheck(
        name="moral_lines_respected", category="personality", status=status,
        summary=(f"{len(flags)} posibles violaciones de moral_lines"
                 if flags else "sin violaciones moral_lines detectadas (heuristica)"),
        items=flags, metric=len(flags), threshold=0,
    )


def check_seed_alignment(session: Session) -> AuditCheck:
    """For each agent, check if observable behavior matches their seed personality.

    Heuristics:
      - Borges-type ('writing', high erudite): expect WRITE_BOOK count > 0
      - Socrates-type ('voting' inicial, no writing): expect TALK count > REFLECT count
      - Arendt-type ('voting', 'writing'): expect both PROPOSE_INSTITUTION and WRITE_*
    """
    flags = []
    agents = session.query(Agent).all()
    for agent in agents:
        seed = agent.seed_json or {}
        nombre = (seed.get("nombre") or agent.nombre or "").lower()
        knowledge = set(agent.conocimiento or [])
        # Per-agent action counts
        counts = {}
        for action_type in ("WRITE_BOOK", "TALK", "WRITE_LETTER", "PROPOSE_INSTITUTION",
                            "PROPOSE_RITUAL", "REFLECT", "TEACH", "READ"):
            counts[action_type] = (
                session.query(ActionLog)
                .filter_by(agent_id=agent.id, action_type=action_type, status="accept")
                .count()
            )

        # Borges-type: writing knowledge + erudito personality → must write at least 1 book
        if "writing" in knowledge and "borges" in nombre and counts["WRITE_BOOK"] == 0:
            flags.append({
                "agent": agent.id, "issue": "borges-like sin libros",
                "counts": counts,
            })

        # Socrates-type: should TALK or REFLECT abundantly
        if "socrates" in nombre and (counts["TALK"] + counts["REFLECT"]) == 0:
            flags.append({
                "agent": agent.id, "issue": "socrates-like sin TALK ni REFLECT",
                "counts": counts,
            })

        # Arendt-type: should propose laws (voting in knowledge)
        if "arendt" in nombre and counts["PROPOSE_INSTITUTION"] == 0:
            flags.append({
                "agent": agent.id, "issue": "arendt-like sin proponer instituciones",
                "counts": counts,
            })

    status = "PASS" if not flags else "WARN"
    return AuditCheck(
        name="seed_alignment", category="personality", status=status,
        summary=(f"{len(flags)} agentes desalineados con su semilla"
                 if flags else "todos los agentes alineados con seed (heuristica)"),
        items=flags, metric=len(flags), threshold=0,
    )


def check_emotional_state_present(session: Session) -> AuditCheck:
    """Agents should have non-default emotional state over time."""
    no_state = []
    flat_state = []
    for a in session.query(Agent).all():
        es = a.emotional_state or {}
        if not es:
            no_state.append(a.id)
            continue
        # Flat = all values equal default 50.0 (or near-default for known keys)
        defaults = {"animo": 50.0, "esperanza": 50.0, "miedo": 0.0,
                    "soledad": 30.0, "dignidad": 70.0, "verguenza": 0.0, "asombro": 30.0}
        diffs = sum(abs(es.get(k, defaults[k]) - defaults[k]) for k in defaults)
        if diffs < 5:
            flat_state.append({"agent": a.id, "es": es})
    items = ([{"missing_state": a} for a in no_state]
             + [{"flat_state": fs} for fs in flat_state])
    status = "PASS" if not items else "INFO"
    return AuditCheck(
        name="emotional_state_evolution", category="personality", status=status,
        summary=(f"{len(items)} agentes con estado emocional sin evolucion "
                 f"(esperado pre-Day 3 mientras no hay LLM driving)"
                 if items else "todos los agentes con estado emocional dinamico"),
        items=items[:10], metric=len(items),
    )


def run_personality_checks(session: Session) -> list[AuditCheck]:
    return [
        check_moral_lines(session),
        check_seed_alignment(session),
        check_emotional_state_present(session),
    ]
