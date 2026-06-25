"""Day 1+2 handlers.

Each handler enforces anti-bullshit: prereqs verified deterministically,
side-effects committed before Accept returns.

MOVE is N-tick travel: declares the trip, world_loop ticks down arrival.
While in_transit, agent cannot accept other actions.
"""
import math
from typing import Tuple

from ..db.schema import Agent
from .actions import WorldContext


def _in_transit(agent: Agent) -> bool:
    return agent.in_transit is not None


def _reject_if_in_transit(agent: Agent) -> Tuple[bool, str]:
    if _in_transit(agent):
        dest = agent.in_transit.get("destino")
        ticks = agent.in_transit.get("ticks_restantes")
        return False, f"estas viajando a '{dest}' (faltan {ticks} ticks), no podes hacer otra cosa."
    return True, ""


def manhattan(x1, y1, x2, y2) -> float:
    return abs(x1 - x2) + abs(y1 - y2)


class MoveHandler:
    """MOVE declares a trip. Arrival happens N ticks later (manhattan / walk_speed).

    Energy cost paid upfront. Other actions blocked while in_transit.
    """
    WALK_SPEED_PER_TICK = 5.0

    def check_prereqs(self, agent: Agent, params: dict, ctx: WorldContext) -> Tuple[bool, str]:
        ok, err = _reject_if_in_transit(agent)
        if not ok:
            return ok, err
        dest = params.get("destino")
        if not dest:
            return False, "MOVE requiere parametro 'destino'."
        loc_actual = ctx.locations_by_id.get(agent.ubicacion)
        if loc_actual is None:
            return False, f"tu location actual '{agent.ubicacion}' no existe en el mapa."
        if dest not in (loc_actual.transitions or []):
            return False, f"no hay transition directa de '{agent.ubicacion}' a '{dest}'. transitions disponibles: {loc_actual.transitions}."
        if dest not in ctx.locations_by_id:
            return False, f"destino '{dest}' no existe."
        if agent.necesidades.get("energia", 0) <= 5:
            return False, f"no tenes energia suficiente para moverte (energia={agent.necesidades.get('energia')})."
        return True, ""

    def apply(self, agent: Agent, params: dict, ctx: WorldContext) -> str:
        dest = params["destino"]
        origen = agent.ubicacion
        loc_o = ctx.locations_by_id[origen]
        loc_d = ctx.locations_by_id[dest]
        dist = manhattan(loc_o.x, loc_o.y, loc_d.x, loc_d.y)
        ticks_viaje = max(1, math.ceil(dist / self.WALK_SPEED_PER_TICK))
        energia_costo = max(5, int(dist))
        necesidades = dict(agent.necesidades)
        necesidades["energia"] = max(0.0, necesidades.get("energia", 0) - energia_costo)
        agent.necesidades = necesidades
        if ticks_viaje == 1:
            # Arrival happens same tick (adjacent).
            agent.ubicacion = dest
            agent.x = loc_d.x
            agent.y = loc_d.y
            agent.in_transit = None
            ctx.session.add(agent)
            return f"camino {dist:.1f} unidades de {origen} a {dest} (1 tick), energia -{energia_costo}"
        agent.in_transit = {
            "destino": dest,
            "origen": origen,
            "ticks_restantes": ticks_viaje,
            "distancia_total": dist,
        }
        ctx.session.add(agent)
        return f"empezo viaje a {dest} (distancia {dist:.1f}, llega en {ticks_viaje} ticks), energia -{energia_costo}"


class TalkHandler:
    """TALK requires another agent in same location AND non-trivial content.

    Anti-bullshit: contenido debe tener >5 chars y no ser placeholder.
    Side-effect: append to target's memoria_recent.
    """
    BANNED_PLACEHOLDERS = {"...", "hola", "...", "habla", "talk", "speak"}

    def check_prereqs(self, agent: Agent, params: dict, ctx: WorldContext) -> Tuple[bool, str]:
        ok, err = _reject_if_in_transit(agent)
        if not ok:
            return ok, err
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
        if target.ubicacion != agent.ubicacion or target.in_transit is not None:
            return False, f"target '{target_id}' no esta accesible (target_loc={target.ubicacion}, vos={agent.ubicacion}, target_in_transit={target.in_transit is not None})."
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
        ok, err = _reject_if_in_transit(agent)
        if not ok:
            return ok, err
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


class WorkHandler:
    """WORK in a location with permite_trabajo=True.

    Anti-bullshit: must be at a location flagged as work-permitting AND have energy.
    Side-effect: gleam += faucet["work_tick"], energia -= cost.
    """
    ENERGY_COST = 10.0
    FAUCET_KEY = "work_tick"

    def check_prereqs(self, agent: Agent, params: dict, ctx: WorldContext) -> Tuple[bool, str]:
        ok, err = _reject_if_in_transit(agent)
        if not ok:
            return ok, err
        loc = ctx.locations_by_id.get(agent.ubicacion)
        if loc is None:
            return False, f"location actual '{agent.ubicacion}' no existe."
        if not getattr(loc, "permite_trabajo", False):
            return False, f"no podes trabajar en '{agent.ubicacion}' (no permite_trabajo)."
        if agent.necesidades.get("energia", 0) < self.ENERGY_COST:
            return False, f"sin energia suficiente para trabajar (energia={agent.necesidades.get('energia')}, requiere {self.ENERGY_COST})."
        return True, ""

    def apply(self, agent: Agent, params: dict, ctx: WorldContext) -> str:
        faucet = (ctx.world_state.faucet or {}) if ctx.world_state else {}
        gain = float(faucet.get(self.FAUCET_KEY, 1.0))
        agent.gleam = (agent.gleam or 0.0) + gain
        necesidades = dict(agent.necesidades)
        necesidades["energia"] = max(0.0, necesidades.get("energia", 0) - self.ENERGY_COST)
        agent.necesidades = necesidades
        ctx.session.add(agent)
        return f"trabajo en {agent.ubicacion}: +{gain} gleam, -{self.ENERGY_COST} energia (gleam total={agent.gleam:.1f})"


def _parse_resource(spec: dict | None) -> Tuple[str, object]:
    """Resolve TRADE/GIFT 'ofrezco'/'pido' spec to (kind, value).

    Supported shapes:
        {"item": "id_del_item"}    → ("item", item_id)
        {"gleam": 5.0}             → ("gleam", float)
    """
    if not spec:
        return ("none", None)
    if "item" in spec and spec["item"]:
        return ("item", spec["item"])
    if "gleam" in spec and spec["gleam"] is not None:
        try:
            v = float(spec["gleam"])
        except (TypeError, ValueError):
            return ("invalid", None)
        if v <= 0:
            return ("invalid", None)
        return ("gleam", v)
    return ("none", None)


def _agent_has(agent: Agent, kind: str, value) -> bool:
    if kind == "gleam":
        return (agent.gleam or 0.0) >= value
    if kind == "item":
        inv = list(agent.inventario or [])
        return any(it.get("id") == value for it in inv)
    return False


def _transfer(src: Agent, dst: Agent, kind: str, value) -> None:
    if kind == "gleam":
        src.gleam = (src.gleam or 0.0) - value
        dst.gleam = (dst.gleam or 0.0) + value
    elif kind == "item":
        inv_src = list(src.inventario or [])
        idx = next(i for i, it in enumerate(inv_src) if it.get("id") == value)
        item = inv_src.pop(idx)
        src.inventario = inv_src
        inv_dst = list(dst.inventario or [])
        inv_dst.append(item)
        dst.inventario = inv_dst


class TradeHandler:
    """TRADE(agente, ofrezco={item|gleam}, pido={item|gleam}).

    Day 2 simplification: validation = implicit consent. If target has `pido`
    and proposer has `ofrezco`, swap atomically. Real explicit-consent protocol
    is post-MVP backlog (would need pending_trades table).
    """

    def check_prereqs(self, agent: Agent, params: dict, ctx: WorldContext) -> Tuple[bool, str]:
        ok, err = _reject_if_in_transit(agent)
        if not ok:
            return ok, err
        target_id = params.get("agente")
        if not target_id:
            return False, "TRADE requiere 'agente' (target)."
        target = ctx.agents_by_id.get(target_id)
        if target is None:
            return False, f"no existe agente '{target_id}'."
        if target.id == agent.id:
            return False, "no podes hacer trade con vos mismo."
        if not target.alive:
            return False, f"'{target_id}' esta muerto."
        if target.ubicacion != agent.ubicacion or target.in_transit is not None:
            return False, f"'{target_id}' no esta accesible para trade."

        ofrezco_kind, ofrezco_val = _parse_resource(params.get("ofrezco"))
        pido_kind, pido_val = _parse_resource(params.get("pido"))
        if ofrezco_kind in ("none", "invalid"):
            return False, "TRADE requiere 'ofrezco' valido ({item} o {gleam})."
        if pido_kind in ("none", "invalid"):
            return False, "TRADE requiere 'pido' valido ({item} o {gleam})."

        if not _agent_has(agent, ofrezco_kind, ofrezco_val):
            return False, f"no tenes el {ofrezco_kind} '{ofrezco_val}' que ofreces."
        if not _agent_has(target, pido_kind, pido_val):
            return False, f"'{target_id}' no tiene el {pido_kind} '{pido_val}' que pedis."
        return True, ""

    def apply(self, agent: Agent, params: dict, ctx: WorldContext) -> str:
        target = ctx.agents_by_id[params["agente"]]
        ofrezco_kind, ofrezco_val = _parse_resource(params["ofrezco"])
        pido_kind, pido_val = _parse_resource(params["pido"])
        _transfer(agent, target, ofrezco_kind, ofrezco_val)
        _transfer(target, agent, pido_kind, pido_val)
        ctx.session.add(agent)
        ctx.session.add(target)
        return f"trade {agent.id}->{target.id}: dio {ofrezco_kind}={ofrezco_val}, recibio {pido_kind}={pido_val}"


PRELOADED_BOOK_CONTENT = {
    "preloaded_borges_short": (
        "Aquel hombre soñaba con un hombre. El soñado le respondió "
        "que también estaba soñando. Y así, al despertar, supo que era "
        "soñado por otro. La cifra del sueño no se cerraba."
    ),
    "preloaded_platon_apologia_fragment": (
        "Solo se que no se nada. Y aun esa certeza es titubeante. "
        "Pero quien examina su propia ignorancia ya empieza a saber."
    ),
    "preloaded_marx_manifesto_fragment": (
        "Un fantasma recorre Europa. Todas las potencias del viejo "
        "mundo se han unido en santa cruzada para acosar a ese fantasma."
    ),
}


class GatherHandler:
    """GATHER(objeto) takes a consumable item from a location object."""
    def check_prereqs(self, agent, params, ctx):
        ok, err = _reject_if_in_transit(agent)
        if not ok: return ok, err
        objeto_id = params.get("objeto")
        if not objeto_id:
            return False, "GATHER requiere 'objeto'."
        loc = ctx.locations_by_id.get(agent.ubicacion)
        if loc is None:
            return False, f"location '{agent.ubicacion}' invalida."
        objeto = next((o for o in (loc.objetos or []) if o.get("id") == objeto_id), None)
        if objeto is None:
            return False, f"objeto '{objeto_id}' no esta en '{agent.ubicacion}'."
        if "GATHER" not in (objeto.get("verbos") or []):
            return False, f"'{objeto_id}' no soporta GATHER."
        return True, ""

    def apply(self, agent, params, ctx):
        objeto_id = params["objeto"]
        loc = ctx.locations_by_id[agent.ubicacion]
        objeto = next(o for o in loc.objetos if o.get("id") == objeto_id)
        new_item = {
            "id": f"{objeto_id}_take_{ctx.tick}",
            "fuente": objeto_id,
        }
        if objeto.get("tiene_comida"):
            new_item.update({"es_comestible": True, "calorias": 25})
        if objeto.get("tiene_agua"):
            new_item["es_bebible"] = True
        if objeto.get("recurso"):
            new_item["recurso"] = objeto["recurso"]
        inv = list(agent.inventario or [])
        inv.append(new_item)
        agent.inventario = inv
        ctx.session.add(agent)
        return f"recogio '{new_item['id']}' de {objeto_id}"


class DrinkHandler:
    def check_prereqs(self, agent, params, ctx):
        ok, err = _reject_if_in_transit(agent)
        if not ok: return ok, err
        fuente_id = params.get("fuente")
        if not fuente_id:
            return False, "DRINK requiere 'fuente'."
        loc = ctx.locations_by_id.get(agent.ubicacion)
        objeto = next((o for o in (loc.objetos or []) if o.get("id") == fuente_id), None)
        if objeto is None or not objeto.get("tiene_agua"):
            return False, f"no hay fuente de agua '{fuente_id}' en {agent.ubicacion}."
        return True, ""

    def apply(self, agent, params, ctx):
        necesidades = dict(agent.necesidades)
        before = necesidades.get("sed", 0)
        necesidades["sed"] = max(0.0, before - 50)
        agent.necesidades = necesidades
        ctx.session.add(agent)
        return f"tomo agua de '{params['fuente']}' (sed {before:.0f}->{necesidades['sed']:.0f})"


class SleepHandler:
    """SLEEP requires a cama in location. Sleep lasts 5 ticks (sleeping_until_tick)."""
    def check_prereqs(self, agent, params, ctx):
        ok, err = _reject_if_in_transit(agent)
        if not ok: return ok, err
        loc = ctx.locations_by_id.get(agent.ubicacion)
        has_bed = any("SLEEP" in (o.get("verbos") or []) for o in (loc.objetos or []))
        if not has_bed and not loc.asiento_publico:
            return False, f"no hay cama ni lugar publico de descanso en '{agent.ubicacion}'."
        return True, ""

    def apply(self, agent, params, ctx):
        agent.sleeping_until_tick = ctx.tick + 5
        necesidades = dict(agent.necesidades)
        necesidades["energia"] = min(100.0, necesidades.get("energia", 0) + 50)
        necesidades["sueno"] = max(0.0, necesidades.get("sueno", 0) - 50)
        agent.necesidades = necesidades
        ctx.session.add(agent)
        return f"se acosto a dormir en '{agent.ubicacion}' (5 ticks); energia +50"


class GiftHandler:
    def check_prereqs(self, agent, params, ctx):
        ok, err = _reject_if_in_transit(agent)
        if not ok: return ok, err
        target_id = params.get("agente")
        item_id = params.get("item")
        if not target_id or not item_id:
            return False, "GIFT requiere 'agente' e 'item'."
        target = ctx.agents_by_id.get(target_id)
        if target is None or target.id == agent.id:
            return False, "target invalido."
        if target.ubicacion != agent.ubicacion or target.in_transit:
            return False, f"'{target_id}' no esta accesible."
        if not any(it.get("id") == item_id for it in (agent.inventario or [])):
            return False, f"no tenes '{item_id}' en inventario."
        return True, ""

    def apply(self, agent, params, ctx):
        _transfer(agent, ctx.agents_by_id[params["agente"]], "item", params["item"])
        ctx.session.add(agent)
        ctx.session.add(ctx.agents_by_id[params["agente"]])
        return f"regalo '{params['item']}' a {params['agente']}"


class AttackHandler:
    def check_prereqs(self, agent, params, ctx):
        ok, err = _reject_if_in_transit(agent)
        if not ok: return ok, err
        target_id = params.get("agente")
        target = ctx.agents_by_id.get(target_id)
        if target is None or target.id == agent.id:
            return False, "target invalido."
        if target.ubicacion != agent.ubicacion or target.in_transit:
            return False, f"'{target_id}' no esta accesible."
        if not target.alive:
            return False, f"'{target_id}' ya esta muerto."
        return True, ""

    def apply(self, agent, params, ctx):
        target = ctx.agents_by_id[params["agente"]]
        damage = 30.0
        target.salud = max(0.0, target.salud - damage)
        if target.salud <= 0:
            target.alive = False
        rel = dict(target.relaciones or {})
        rel[agent.id] = -1.0
        target.relaciones = rel
        rel_self = dict(agent.relaciones or {})
        rel_self[target.id] = -1.0
        agent.relaciones = rel_self
        ctx.session.add(agent)
        ctx.session.add(target)
        return f"ataco a {target.id} (-{damage} salud, ahora salud={target.salud:.0f}, alive={target.alive})"


class TeachHandler:
    """TEACH(agente, tech): same loc, self knows tech, target doesn't, roll succeeds."""
    def check_prereqs(self, agent, params, ctx):
        ok, err = _reject_if_in_transit(agent)
        if not ok: return ok, err
        target_id = params.get("agente")
        tech = params.get("tech")
        if not target_id or not tech:
            return False, "TEACH requiere 'agente' y 'tech'."
        target = ctx.agents_by_id.get(target_id)
        if target is None or target.id == agent.id:
            return False, "target invalido."
        if target.ubicacion != agent.ubicacion or target.in_transit:
            return False, f"'{target_id}' no accesible."
        if tech not in (agent.conocimiento or []):
            return False, f"no sabes '{tech}', no podes enseñarla."
        if tech in (target.conocimiento or []):
            return False, f"'{target_id}' ya conoce '{tech}'."
        return True, ""

    def apply(self, agent, params, ctx):
        target = ctx.agents_by_id[params["agente"]]
        tech = params["tech"]
        # Deterministic Day 2: always success.
        kn = list(target.conocimiento or [])
        kn.append(tech)
        target.conocimiento = kn
        ctx.session.add(target)
        return f"enseño '{tech}' a {target.id}"


class LearnHandler:
    """LEARN is the inverse of TEACH; declarative only. Same effect when prereqs match."""
    def check_prereqs(self, agent, params, ctx):
        ok, err = _reject_if_in_transit(agent)
        if not ok: return ok, err
        de = params.get("de")
        tech = params.get("tech")
        if not de or not tech:
            return False, "LEARN requiere 'de' y 'tech'."
        source = ctx.agents_by_id.get(de)
        if source is None or source.id == agent.id:
            return False, "source invalido."
        if source.ubicacion != agent.ubicacion or source.in_transit:
            return False, f"'{de}' no accesible."
        if tech not in (source.conocimiento or []):
            return False, f"'{de}' no sabe '{tech}'."
        if tech in (agent.conocimiento or []):
            return False, f"ya conoces '{tech}'."
        return True, ""

    def apply(self, agent, params, ctx):
        tech = params["tech"]
        kn = list(agent.conocimiento or [])
        kn.append(tech)
        agent.conocimiento = kn
        ctx.session.add(agent)
        return f"aprendio '{tech}' de {params['de']}"


def _consume_writing_supplies(agent, ctx) -> str | None:
    """Try to consume papel+lapiz from inventory OR from location objects.
    Returns None on success, error message on failure.
    """
    loc = ctx.locations_by_id.get(agent.ubicacion)
    loc_objs = {o.get("id") for o in (loc.objetos or [])}
    has_paper = any(it.get("id") == "papel" for it in (agent.inventario or [])) or "papel" in loc_objs
    has_pencil = any(it.get("id") == "lapiz" for it in (agent.inventario or [])) or "lapiz" in loc_objs
    if not has_paper or not has_pencil:
        return f"falta papel o lapiz (en inventario o location)."
    return None


class WriteBookHandler:
    MIN_CONTENT_CHARS = 200

    def check_prereqs(self, agent, params, ctx):
        ok, err = _reject_if_in_transit(agent)
        if not ok: return ok, err
        titulo = (params.get("titulo") or "").strip()
        contenido = (params.get("contenido_full") or "").strip()
        if not titulo:
            return False, "WRITE_BOOK requiere 'titulo'."
        if len(contenido) < self.MIN_CONTENT_CHARS:
            return False, f"WRITE_BOOK requiere 'contenido_full' >= {self.MIN_CONTENT_CHARS} chars (es {len(contenido)}). Anti-bullshit: el contenido real debe escribirse."
        if "writing" not in (agent.conocimiento or []):
            return False, "no sabes escribir (knowledge:writing requerido)."
        supplies_err = _consume_writing_supplies(agent, ctx)
        if supplies_err:
            return False, supplies_err
        return True, ""

    def apply(self, agent, params, ctx):
        from ..db.schema import TextArtifact
        artifact = TextArtifact(
            autor_id=agent.id,
            tipo="book",
            titulo=params["titulo"][:200],
            contenido=params["contenido_full"],
            tick=ctx.tick,
            location_id=agent.ubicacion,
        )
        ctx.session.add(artifact)
        return f"escribio el libro '{params['titulo'][:60]}' ({len(params['contenido_full'])} chars) en {agent.ubicacion}"


class WriteLetterHandler:
    MIN_CONTENT_CHARS = 30

    def check_prereqs(self, agent, params, ctx):
        ok, err = _reject_if_in_transit(agent)
        if not ok: return ok, err
        dest = params.get("destinatario")
        contenido = (params.get("contenido") or "").strip()
        if not dest:
            return False, "WRITE_LETTER requiere 'destinatario'."
        if len(contenido) < self.MIN_CONTENT_CHARS:
            return False, f"contenido carta >= {self.MIN_CONTENT_CHARS} chars (es {len(contenido)})."
        supplies_err = _consume_writing_supplies(agent, ctx)
        if supplies_err:
            return False, supplies_err
        return True, ""

    def apply(self, agent, params, ctx):
        from ..db.schema import TextArtifact
        artifact = TextArtifact(
            autor_id=agent.id,
            tipo="letter",
            titulo=f"carta a {params['destinatario']}",
            contenido=params["contenido"],
            tick=ctx.tick,
            location_id=agent.ubicacion,
        )
        ctx.session.add(artifact)
        return f"escribio carta a {params['destinatario']} ({len(params['contenido'])} chars)"


class WriteCodeHandler:
    """Day 2 stub: validates spec but stores placeholder code.
    Day 4: real LLM generation + E2B execution.
    """
    MIN_SPEC_CHARS = 50

    def check_prereqs(self, agent, params, ctx):
        ok, err = _reject_if_in_transit(agent)
        if not ok: return ok, err
        spec = (params.get("spec") or "").strip()
        lenguaje = params.get("lenguaje", "python")
        if len(spec) < self.MIN_SPEC_CHARS:
            return False, f"WRITE_CODE 'spec' >= {self.MIN_SPEC_CHARS} chars (es {len(spec)})."
        if lenguaje not in ("python", "html", "js"):
            return False, f"lenguaje '{lenguaje}' no soportado. Usa python|html|js."
        if "programming" not in (agent.conocimiento or []):
            return False, "no sabes programar (knowledge:programming requerido)."
        loc = ctx.locations_by_id.get(agent.ubicacion)
        has_computer = any(o.get("es_computadora") for o in (loc.objetos or []))
        if not has_computer:
            return False, f"no hay computadora en '{agent.ubicacion}'."
        return True, ""

    def apply(self, agent, params, ctx):
        from ..db.schema import CodeArtifact
        artifact = CodeArtifact(
            autor_id=agent.id,
            spec=params["spec"],
            lenguaje=params.get("lenguaje", "python"),
            codigo="# [stub Día 2 — pending E2B integration Día 4]",
            stdout="",
            html_render="",
            tick=ctx.tick,
        )
        ctx.session.add(artifact)
        return f"escribio codigo {artifact.lenguaje} (spec {len(params['spec'])} chars) [stub Dia 2]"


class ReadHandler:
    def check_prereqs(self, agent, params, ctx):
        ok, err = _reject_if_in_transit(agent)
        if not ok: return ok, err
        libro_id = params.get("libro_id")
        if not libro_id:
            return False, "READ requiere 'libro_id'."
        # check in inventory or location
        from ..db.schema import TextArtifact
        loc = ctx.locations_by_id.get(agent.ubicacion)
        loc_books = {o.get("id"): o for o in (loc.objetos or [])
                     if "READ" in (o.get("verbos") or [])}
        if libro_id in loc_books:
            return True, ""
        # text_artifact id (escrito por algun agente)
        artifact = ctx.session.get(TextArtifact, int(libro_id)) if libro_id.isdigit() else None
        if artifact is not None:
            return True, ""
        return False, f"libro '{libro_id}' no esta en {agent.ubicacion} ni es artifact existente."

    def apply(self, agent, params, ctx):
        libro_id = params["libro_id"]
        loc = ctx.locations_by_id.get(agent.ubicacion)
        loc_books = {o.get("id"): o for o in (loc.objetos or []) if "READ" in (o.get("verbos") or [])}
        contenido = None
        titulo = libro_id
        if libro_id in loc_books:
            ref = loc_books[libro_id].get("contenido_ref")
            contenido = PRELOADED_BOOK_CONTENT.get(ref, "[contenido no precargado]")
        else:
            from ..db.schema import TextArtifact
            artifact = ctx.session.get(TextArtifact, int(libro_id))
            if artifact is not None:
                contenido = artifact.contenido
                titulo = artifact.titulo

        from ..config import MEMORIA_RECENT_CAP
        mem = list(agent.memoria_recent or [])
        mem.append({
            "tick": ctx.tick,
            "type": "read",
            "libro_id": libro_id,
            "titulo": titulo,
            "snippet": (contenido or "")[:300],
        })
        agent.memoria_recent = mem[-MEMORIA_RECENT_CAP:]
        ctx.session.add(agent)
        return f"leyo '{titulo}' ({len(contenido or '')} chars) en {agent.ubicacion}"


class ReflectHandler:
    """REFLECT: cooldown N ticks (cheap protection). Day 2 stub stores prompt."""
    COOLDOWN_TICKS = 30

    def check_prereqs(self, agent, params, ctx):
        ok, err = _reject_if_in_transit(agent)
        if not ok: return ok, err
        prompt = (params.get("prompt_interno") or "").strip()
        if len(prompt) < 10:
            return False, "REFLECT 'prompt_interno' debe tener >=10 chars."
        last = agent.last_reflect_tick or 0
        if last > 0 and ctx.tick - last < self.COOLDOWN_TICKS:
            faltan = self.COOLDOWN_TICKS - (ctx.tick - last)
            return False, f"REFLECT en cooldown ({faltan} ticks). caro."
        return True, ""

    def apply(self, agent, params, ctx):
        agent.last_reflect_tick = ctx.tick
        agent.intencion_actual = params["prompt_interno"][:300]
        ctx.session.add(agent)
        return f"reflexiono: '{params['prompt_interno'][:80]}'"


class RespondToGodHandler:
    def check_prereqs(self, agent, params, ctx):
        ok, err = _reject_if_in_transit(agent)
        if not ok: return ok, err
        dilema_id = params.get("dilema_id")
        respuesta = (params.get("respuesta") or "").strip()
        if dilema_id is None:
            return False, "RESPOND_TO_GOD requiere 'dilema_id'."
        if len(respuesta) < 10:
            return False, "respuesta >=10 chars (anti-bullshit)."
        from ..db.schema import Dilema
        dilema = ctx.session.get(Dilema, int(dilema_id))
        if dilema is None or not dilema.active:
            return False, f"dilema {dilema_id} no esta activo."
        return True, ""

    def apply(self, agent, params, ctx):
        from ..db.schema import DilemaResponse
        resp = DilemaResponse(
            dilema_id=int(params["dilema_id"]),
            agent_id=agent.id,
            respuesta=params["respuesta"],
            tick=ctx.tick,
        )
        ctx.session.add(resp)
        return f"respondio dilema {params['dilema_id']}: '{params['respuesta'][:80]}'"


class ProposeInstitutionHandler:
    MIN_TEXT_CHARS = 100

    def check_prereqs(self, agent, params, ctx):
        ok, err = _reject_if_in_transit(agent)
        if not ok: return ok, err
        nombre = (params.get("nombre") or "").strip()
        texto = (params.get("texto_ley") or "").strip()
        if not nombre:
            return False, "PROPOSE_INSTITUTION requiere 'nombre'."
        if len(texto) < self.MIN_TEXT_CHARS:
            return False, f"texto_ley >= {self.MIN_TEXT_CHARS} chars (es {len(texto)}). Anti-bullshit."
        return True, ""

    def apply(self, agent, params, ctx):
        from ..db.schema import PendingInstitution
        pi = PendingInstitution(
            proposer_id=agent.id,
            nombre=params["nombre"][:200],
            texto_ley=params["texto_ley"],
            ratify_count=0,
            ratifiers=[],
            status="pending",
            created_tick=ctx.tick,
        )
        ctx.session.add(pi)
        ctx.session.flush()
        return f"propuso institucion '{pi.nombre}' (id={pi.id}, necesita 3 ratify)"


class ProposeRitualHandler:
    MIN_DESC_CHARS = 50

    def check_prereqs(self, agent, params, ctx):
        ok, err = _reject_if_in_transit(agent)
        if not ok: return ok, err
        nombre = (params.get("nombre") or "").strip()
        desc = (params.get("descripcion") or "").strip()
        if not nombre:
            return False, "PROPOSE_RITUAL requiere 'nombre'."
        if len(desc) < self.MIN_DESC_CHARS:
            return False, f"descripcion >= {self.MIN_DESC_CHARS} chars (es {len(desc)})."
        return True, ""

    def apply(self, agent, params, ctx):
        from ..db.schema import PendingRitual
        pr = PendingRitual(
            proposer_id=agent.id,
            nombre=params["nombre"][:200],
            mci_concept=(params.get("mci_concept") or "")[:200],
            frecuencia=(params.get("frecuencia") or "")[:100],
            descripcion=params["descripcion"],
            ratify_count=0,
            ratifiers=[],
            status="pending",
            created_tick=ctx.tick,
        )
        ctx.session.add(pr)
        ctx.session.flush()
        return f"propuso ritual '{pr.nombre}' (id={pr.id}, necesita 3 ratify)"


class RatifyHandler:
    """RATIFY(tipo, proposal_id). tipo='institution'|'ritual'.
    Counts unique ratifiers (no double-vote). Promotes when count >= 3.
    """
    REQUIRED_VOTES = 3

    def check_prereqs(self, agent, params, ctx):
        ok, err = _reject_if_in_transit(agent)
        if not ok: return ok, err
        tipo = params.get("tipo")
        pid = params.get("proposal_id")
        if tipo not in ("institution", "ritual") or pid is None:
            return False, "RATIFY requiere 'tipo' (institution|ritual) y 'proposal_id'."
        from ..db.schema import PendingInstitution, PendingRitual
        if tipo == "institution":
            p = ctx.session.get(PendingInstitution, int(pid))
        else:
            p = ctx.session.get(PendingRitual, int(pid))
        if p is None or p.status != "pending":
            return False, f"proposal {tipo}:{pid} no existe o ya esta cerrada."
        if p.proposer_id == agent.id:
            return False, "no podes ratificar tu propia propuesta."
        if agent.id in (p.ratifiers or []):
            return False, "ya ratificaste esta propuesta."
        return True, ""

    def apply(self, agent, params, ctx):
        from ..db.schema import PendingInstitution, PendingRitual, Institution, Ritual
        tipo = params["tipo"]
        pid = int(params["proposal_id"])
        Model = PendingInstitution if tipo == "institution" else PendingRitual
        p = ctx.session.get(Model, pid)
        ratifiers = list(p.ratifiers or [])
        ratifiers.append(agent.id)
        p.ratifiers = ratifiers
        p.ratify_count = len(ratifiers)
        promoted = ""
        if p.ratify_count >= self.REQUIRED_VOTES:
            p.status = "ratified"
            if tipo == "institution":
                inst = Institution(nombre=p.nombre, texto=p.texto_ley, ratified_tick=ctx.tick)
                ctx.session.add(inst)
            else:
                rit = Ritual(
                    nombre=p.nombre, mci_concept=p.mci_concept,
                    frecuencia=p.frecuencia, descripcion=p.descripcion,
                    ratified_tick=ctx.tick,
                )
                ctx.session.add(rit)
            promoted = " -> RATIFIED, instanciada"
        ctx.session.add(p)
        return f"ratifico {tipo}:{pid} ({p.ratify_count}/{self.REQUIRED_VOTES}){promoted}"


class PostHandler:
    MIN_CONTENT_CHARS = 10

    def check_prereqs(self, agent, params, ctx):
        ok, err = _reject_if_in_transit(agent)
        if not ok: return ok, err
        contenido = (params.get("contenido") or "").strip()
        if len(contenido) < self.MIN_CONTENT_CHARS:
            return False, f"POST contenido >= {self.MIN_CONTENT_CHARS} chars."
        return True, ""

    def apply(self, agent, params, ctx):
        from ..db.schema import Post
        red = params.get("red") or "default"
        p = Post(autor_id=agent.id, red=red, contenido=params["contenido"], tick=ctx.tick)
        ctx.session.add(p)
        ctx.session.flush()
        return f"posteo en '{red}' ({len(params['contenido'])} chars, id={p.id})"


def default_handlers() -> dict:
    return {
        "MOVE": MoveHandler(),
        "TALK": TalkHandler(),
        "EAT": EatHandler(),
        "WORK": WorkHandler(),
        "TRADE": TradeHandler(),
        "GATHER": GatherHandler(),
        "DRINK": DrinkHandler(),
        "SLEEP": SleepHandler(),
        "GIFT": GiftHandler(),
        "ATTACK": AttackHandler(),
        "TEACH": TeachHandler(),
        "LEARN": LearnHandler(),
        "WRITE_BOOK": WriteBookHandler(),
        "WRITE_LETTER": WriteLetterHandler(),
        "WRITE_CODE": WriteCodeHandler(),
        "READ": ReadHandler(),
        "REFLECT": ReflectHandler(),
        "RESPOND_TO_GOD": RespondToGodHandler(),
        "PROPOSE_INSTITUTION": ProposeInstitutionHandler(),
        "PROPOSE_RITUAL": ProposeRitualHandler(),
        "RATIFY": RatifyHandler(),
        "POST": PostHandler(),
    }
