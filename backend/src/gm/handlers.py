"""Day 1 handlers: MOVE, TALK, EAT.

Each handler enforces anti-bullshit: prereqs verified deterministically,
side-effects committed before Accept returns.
"""
from typing import Tuple

from ..db.schema import Agent
from .actions import WorldContext


class MoveHandler:
    def check_prereqs(self, agent: Agent, params: dict, ctx: WorldContext) -> Tuple[bool, str]:
        dest = params.get("destino")
        if not dest:
            return False, "MOVE requiere parametro 'destino'."
        loc_actual = ctx.locations_by_id.get(agent.ubicacion)
        if loc_actual is None:
            return False, f"tu location actual '{agent.ubicacion}' no existe en el mapa."
        if dest not in (loc_actual.transitions or []):
            return False, f"no hay transition directa de '{agent.ubicacion}' a '{dest}'. transitions disponibles: {loc_actual.transitions}."
        if agent.necesidades.get("energia", 0) <= 5:
            return False, f"no tenes energia suficiente para moverte (energia={agent.necesidades.get('energia')})."
        if dest not in ctx.locations_by_id:
            return False, f"destino '{dest}' no existe."
        return True, ""

    def apply(self, agent: Agent, params: dict, ctx: WorldContext) -> str:
        dest = params["destino"]
        origen = agent.ubicacion
        agent.ubicacion = dest
        necesidades = dict(agent.necesidades)
        necesidades["energia"] = max(0.0, necesidades.get("energia", 0) - 5)
        agent.necesidades = necesidades
        ctx.session.add(agent)
        return f"se movio de {origen} a {dest}, energia -5"


class TalkHandler:
    """TALK requires another agent in same location AND non-trivial content.

    Anti-bullshit: contenido debe tener >5 chars y no ser placeholder.
    Side-effect: append to target's memoria_recent.
    """
    BANNED_PLACEHOLDERS = {"...", "hola", "...", "habla", "talk", "speak"}

    def check_prereqs(self, agent: Agent, params: dict, ctx: WorldContext) -> Tuple[bool, str]:
        target_id = params.get("agente")
        contenido = (params.get("contenido") or "").strip()
        if not target_id:
            return False, "TALK requiere parametro 'agente' (id del destinatario)."
        if not contenido or len(contenido) <= 5:
            return False, "TALK requiere 'contenido' con mas de 5 chars (anti-bullshit)."
        if contenido.lower() in self.BANNED_PLACEHOLDERS:
            return False, f"contenido '{contenido}' es placeholder, no vale (anti-bullshit)."
        target = ctx.agents_by_id.get(target_id)
        if target is None:
            return False, f"no existe agente '{target_id}'."
        if target.id == agent.id:
            return False, "no podes hablarte a vos mismo via TALK (usa REFLECT)."
        if target.ubicacion != agent.ubicacion:
            return False, f"target '{target_id}' esta en '{target.ubicacion}', vos en '{agent.ubicacion}'. mismo lugar requerido."
        if not target.alive:
            return False, f"'{target_id}' esta muerto."
        return True, ""

    def apply(self, agent: Agent, params: dict, ctx: WorldContext) -> str:
        target_id = params["agente"]
        contenido = params["contenido"].strip()
        target = ctx.agents_by_id[target_id]
        mem = list(target.memoria_recent or [])
        mem.append({
            "tick": ctx.tick,
            "type": "heard",
            "from": agent.id,
            "msg": contenido,
        })
        from ..config import MEMORIA_RECENT_CAP
        target.memoria_recent = mem[-MEMORIA_RECENT_CAP:]
        ctx.session.add(target)
        return f"hablo a {target_id}: '{contenido[:60]}'"


class EatHandler:
    """EAT consumes a comestible item from inventario.

    Anti-bullshit: el item debe estar en inventario AND ser comestible.
    Side-effect: hambre -= calorias; item removido.
    """

    def check_prereqs(self, agent: Agent, params: dict, ctx: WorldContext) -> Tuple[bool, str]:
        item_id = params.get("item")
        if not item_id:
            return False, "EAT requiere parametro 'item'."
        inv = list(agent.inventario or [])
        match = next((it for it in inv if it.get("id") == item_id), None)
        if match is None:
            return False, f"item '{item_id}' no esta en tu inventario {[i.get('id') for i in inv]}."
        if not match.get("es_comestible", False):
            return False, f"item '{item_id}' no es comestible."
        return True, ""

    def apply(self, agent: Agent, params: dict, ctx: WorldContext) -> str:
        item_id = params["item"]
        inv = list(agent.inventario or [])
        idx = next(i for i, it in enumerate(inv) if it.get("id") == item_id)
        item = inv.pop(idx)
        calorias = float(item.get("calorias", 10))
        necesidades = dict(agent.necesidades)
        necesidades["hambre"] = max(0.0, necesidades.get("hambre", 0) - calorias)
        agent.necesidades = necesidades
        agent.inventario = inv
        ctx.session.add(agent)
        return f"comio {item_id} (-{calorias} hambre)"


def default_handlers() -> dict:
    return {
        "MOVE": MoveHandler(),
        "TALK": TalkHandler(),
        "EAT": EatHandler(),
    }
