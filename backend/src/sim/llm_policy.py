"""LLM-driven agent policy: builds prompt context, calls LLM, parses JSON action.

Used for "leader" tier agents (3 famosos). For ScriptedAgentPolicy see world_loop.py.

Prompt structure (compacto, ~600 tokens):
  - identidad: nombre, moral_lines, primary_conflict, manera_de_hablar
  - estado: ubicacion + objetos visibles, necesidades, gleam, conocimiento
  - contexto: agentes en location, ultimo memoria, trigger info
  - acciones permitidas: filtradas por trigger.forced_subset si aplica
  - response schema: JSON estricto {type, params}

Anti-bullshit: LLM debe incluir contenido REAL para WRITE_BOOK/WRITE_CODE etc.
"""
import json
import logging
from dataclasses import dataclass

from ..db.schema import Agent
from ..mind.llm import LLMGateway
from ..gm.actions import Action
from ..gm.validator import GameMaster
from .triggers import Trigger


log = logging.getLogger("llm_policy")


ACTION_SCHEMA_HINT = """
Acciones disponibles (firmas + params requeridos):

MOVE(destino: str)
GATHER(objeto: str)
EAT(item: str)
DRINK(fuente: str)
SLEEP()
TALK(agente: str, contenido: str)        # contenido REAL >5 chars, no placeholders
TRADE(agente: str, ofrezco: {item|gleam}, pido: {item|gleam})
GIFT(agente: str, item: str)
ATTACK(agente: str)
TEACH(agente: str, tech: str)
LEARN(de: str, tech: str)
WRITE_BOOK(titulo: str, contenido_full: str)   # contenido_full >=200 chars REAL
WRITE_LETTER(destinatario: str, contenido: str) # >=30 chars
WRITE_CODE(spec: str, lenguaje: "python"|"html"|"js")  # spec >=50 chars
READ(libro_id: str)
WORK()                                    # solo en locations con permite_trabajo
REFLECT(prompt_interno: str)              # >=10 chars, cooldown 30 ticks
PROPOSE_INSTITUTION(nombre: str, texto_ley: str)   # texto >=100 chars
PROPOSE_RITUAL(nombre: str, mci_concept: str, frecuencia: str, descripcion: str)  # desc >=50 chars
RATIFY(tipo: "institution"|"ritual", proposal_id: int)
POST(red: str, contenido: str)            # >=10 chars
RESPOND_TO_GOD(dilema_id: int, respuesta: str)  # >=10 chars
""".strip()


def _format_world_ontology(world_state) -> str:
    """Render ontology as a compact bullet list for the prompt."""
    o = (world_state.world_ontology if world_state else None) or {}
    if not o:
        return "(sin ontologia definida)"
    parts = []
    label_map = {
        "fenomenos_naturales": "Fenomenos naturales",
        "estados_internos": "Estados internos",
        "abstractos_sociales": "Abstractos sociales",
        "objetos_disponibles": "Objetos del mundo",
        "no_existe": "NO EXISTE en este mundo (NO mencionar)",
    }
    for key, label in label_map.items():
        vals = o.get(key) or []
        if not vals:
            continue
        parts.append(f"  - {label}: {', '.join(vals)}")
    return "\n".join(parts)


def render_prompt(agent: Agent, trigger: Trigger, ctx) -> str:
    from .time_of_day import from_world_state
    seed = agent.seed_json or {}
    moral = ", ".join(agent.moral_lines or seed.get("moral_lines", []))
    voice = seed.get("manera_de_hablar", "neutro")
    loc = ctx.locations_by_id.get(agent.ubicacion)
    objetos = [o.get("id") for o in (loc.objetos or [])] if loc else []
    others_here = [
        a.id for a in ctx.agents_by_id.values()
        if a.id != agent.id and a.ubicacion == agent.ubicacion and not a.in_transit
    ]
    necesidades = ", ".join(f"{k}={v:.0f}" for k, v in (agent.necesidades or {}).items())
    inv_ids = [it.get("id") for it in (agent.inventario or [])]
    last_mem = (agent.memoria_recent or [])[-5:]
    last_mem_str = "; ".join(
        f"t{m.get('tick')}: {m.get('type')} {m.get('msg') or m.get('snippet') or ''}"
        for m in last_mem
    ) or "(sin memoria reciente)"

    wt = from_world_state(ctx.world_state)
    when = wt.describe()

    ontology_block = _format_world_ontology(ctx.world_state)

    trigger_block = ""
    if trigger.kind == "crit_need":
        trigger_block = (
            f"\n!! NECESIDAD CRITICA: {trigger.reason}. "
            f"Solo podes usar: {trigger.forced_subset}."
        )
    elif trigger.kind == "crit_event":
        trigger_block = (
            f"\n!! EVENTO CRITICO: {trigger.reason}. "
            f"Acciones permitidas: {trigger.forced_subset}. "
            f"Contexto: {trigger.context_extra}"
        )
    elif trigger.kind == "observation":
        trigger_block = (
            f"\n(observacion: {trigger.context_extra.get('events', [])})"
        )

    prompt = f"""Sos {agent.nombre}. Pensas en castellano rioplatense.
Tu manera de hablar: {voice}
Tus lineas morales: {moral}
Tu conflicto principal: {agent.primary_conflict or seed.get('primary_conflict', '')}

CUANDO (tick {ctx.tick}): {when}

ESTADO ACTUAL:
- Ubicacion: {agent.ubicacion} ({loc.nombre_display if loc else '?'})
- Objetos en location: {objetos}
- Otros agentes aqui: {others_here}
- Tu inventario: {inv_ids}
- Tu conocimiento: {list(agent.conocimiento or [])}
- Necesidades: {necesidades}
- Gleam (dinero): {agent.gleam:.1f}
- Salud: {agent.salud:.0f}/100
- Memoria reciente: {last_mem_str}
{trigger_block}

ONTOLOGIA DE ESTE MUNDO (que existe y que no — coherencia obligatoria):
{ontology_block}

REGLA DE COHERENCIA: cuando escribas (TALK, WRITE_BOOK, WRITE_LETTER,
PROPOSE_INSTITUTION, PROPOSE_RITUAL, POST), referencia SOLO cosas que existen
en este mundo. No hables de fuego, espadas, magia, naves espaciales, etc.
Si necesitas describir algo abstracto (silencio, amor, justicia), usa los
'abstractos_sociales' y 'estados_internos' listados.

{ACTION_SCHEMA_HINT}

REGLA ANTI-BULLSHIT: si declaras WRITE_BOOK, el contenido_full DEBE estar en el JSON,
con >=200 chars reales. Lo mismo para WRITE_CODE (spec >=50), WRITE_LETTER (>=30),
PROPOSE_INSTITUTION (texto_ley >=100), PROPOSE_RITUAL (descripcion >=50).
Si declaras y no incluis contenido real, la accion sera RECHAZADA y vas a quedar
en ridiculo en el log auditable.

Respondeme UN solo JSON con esta forma EXACTA, sin texto extra:
{{"type": "<ACCION>", "params": {{...}}, "razonamiento_breve": "<1 oracion>"}}
"""
    return prompt


def parse_action_response(text: str) -> Action | None:
    """Try to extract a JSON action from LLM response. Returns None if unparseable."""
    text = text.strip()
    # Strip markdown fences if present
    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(l for l in lines if not l.startswith("```"))
    # Find first { ... } block
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end < 0 or end <= start:
        return None
    chunk = text[start:end+1]
    try:
        data = json.loads(chunk)
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict) or "type" not in data:
        return None
    return Action(type=str(data["type"]), params=data.get("params", {}) or {})


@dataclass
class LLMDrivenPolicy:
    """LLM-driven agent policy. Calls LLMGateway per tick (subject to trigger).

    Tier mapping:
      - crit_need / crit_event / normal → "leader"
      - observation                     → "micro" (no action returned)
    """
    agent_id: str
    gateway: LLMGateway
    ignore_triggers: bool = False
    _ctx_ref: object = None   # injected by world_loop each tick

    def next_action(self, trigger: Trigger | None = None) -> Action | None:
        if trigger is None or trigger.kind == "skip":
            return None
        if self._ctx_ref is None:
            log.warning("policy missing ctx_ref; cannot build prompt")
            return None
        agent = self._ctx_ref.agents_by_id.get(self.agent_id)
        if agent is None:
            return None

        # Observation: micro LLM call (1 line). Inject into agent's memoria_recent
        # so the next decision tick has fresh context. No action returned.
        if trigger.kind == "observation":
            try:
                prompt = self._render_observation_prompt(agent, trigger)
                result = self.gateway.call(prompt, tier="micro", max_tokens=200)
                self._inject_memory(agent, result.text.strip()[:280])
            except Exception as e:
                log.warning("observation micro-call failed for %s: %s", self.agent_id, e)
            return None

        # Decision (crit_need / crit_event / normal): full prompt, leader tier.
        try:
            prompt = render_prompt(agent, trigger, self._ctx_ref)
            result = self.gateway.call(prompt, tier="leader", max_tokens=1200)
        except Exception as e:
            log.warning("LLM decision call failed for %s: %s", self.agent_id, e)
            return None
        action = parse_action_response(result.text)
        if action is None:
            log.warning("LLM returned unparseable JSON for %s: %s",
                        self.agent_id, result.text[:160])
            return None
        return action

    def _render_observation_prompt(self, agent, trigger) -> str:
        events = trigger.context_extra.get("events", [])
        evt_str = ", ".join(
            f"{e.get('actor')}={e.get('type')}" for e in events
        )
        return (
            f"Sos {agent.nombre}. Estas en {agent.ubicacion}. "
            f"Acabas de observar: {evt_str}. "
            "Escribi UNA oracion (en castellano rioplatense, primera persona) "
            "describiendo que pensaste o sentiste en este instante. "
            "Maximo 200 chars. No declares ninguna accion. Solo el pensamiento."
        )

    def _inject_memory(self, agent, snippet: str):
        from ..config import MEMORIA_RECENT_CAP
        mem = list(agent.memoria_recent or [])
        mem.append({
            "tick": self._ctx_ref.tick,
            "type": "observation",
            "snippet": snippet,
        })
        agent.memoria_recent = mem[-MEMORIA_RECENT_CAP:]
        self._ctx_ref.session.add(agent)
