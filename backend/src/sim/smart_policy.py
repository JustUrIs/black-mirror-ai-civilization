"""Reactive heuristic policy for famous agents.

Replaces the rigid CyclicPolicy. Decides per-tick based on actual world state:

  1. Survival   — sed, hambre, energia, salud
  2. Reaction   — observed events, attacks, awe (creator)
  3. Personality — Borges writes/reads, Socrates questions, Arendt legislates

Every emitted Action carries a `_rationale` in params so the UI can show the
internal monologue. No LLM needed; behavior is deterministic but context-aware.

When `ANTHROPIC_API_KEY` is set + USE_LLM_POLICY=1, the LLMDrivenPolicy still
takes over (real "thinking"). SmartPolicy is the offline brain that still feels
alive.
"""
import logging
import random
from collections import deque
from typing import Optional

from .world_loop import ScriptedAgentPolicy
from ..gm.actions import Action


log = logging.getLogger("smart_policy")


# === thresholds ===
SED_SEEK = 60.0
HAMBRE_SEEK = 60.0
ENERGIA_REST = 25.0
SALUD_FLEE = 35.0

# === BFS path cache ===
def _bfs_path(transitions: dict, start: str, end: str) -> list[str] | None:
    if start == end:
        return [start]
    q = deque([(start, [start])])
    seen = {start}
    while q:
        cur, path = q.popleft()
        for nb in transitions.get(cur, []):
            if nb in seen:
                continue
            seen.add(nb)
            new_path = path + [nb]
            if nb == end:
                return new_path
            q.append((nb, new_path))
    return None


def _build_transitions(ctx) -> dict:
    return {lid: list(loc.transitions or []) for lid, loc in ctx.locations_by_id.items()}


# === resource discovery ===
def _location_water_source(loc) -> Optional[str]:
    """Return objeto.id of first water source in location (DRINK fuente)."""
    for o in (loc.objetos or []):
        if o.get("tiene_agua"):
            return o.get("id")
    return None


def _location_food_objeto(loc) -> Optional[str]:
    """Return objeto.id of first food source in location (GATHER objeto)."""
    for o in (loc.objetos or []):
        if o.get("tiene_comida"):
            return o.get("id")
    return None


def _location_world_food(ctx, loc_id: str) -> Optional[int]:
    """Return WorldObject.id of first edible (fruta/pan) in location."""
    from ..db.schema import WorldObject
    wo = ctx.session.query(WorldObject).filter_by(
        location_id=loc_id, state="active",
    ).all()
    for w in wo:
        if w.object_type in {"fruta", "pan"}:
            return w.id
    return None


def _location_bed(loc) -> bool:
    return any("SLEEP" in (o.get("verbos") or []) for o in (loc.objetos or [])) \
        or bool(loc.asiento_publico)


def _location_allows_work(loc) -> bool:
    return bool(loc.permite_trabajo)


def _nearest_location_with(ctx, predicate, start: str) -> tuple[str, list[str]] | None:
    """BFS to nearest location matching predicate(loc) -> bool. Returns (dest, path)."""
    transitions = _build_transitions(ctx)
    q = deque([(start, [start])])
    seen = {start}
    while q:
        cur, path = q.popleft()
        loc = ctx.locations_by_id.get(cur)
        if loc and cur != start and predicate(loc):
            return cur, path
        for nb in transitions.get(cur, []):
            if nb in seen:
                continue
            seen.add(nb)
            q.append((nb, path + [nb]))
    return None


def _next_hop(ctx, start: str, end: str) -> Optional[str]:
    """Single-hop towards end. None if same loc or no path."""
    if start == end:
        return None
    transitions = _build_transitions(ctx)
    p = _bfs_path(transitions, start, end)
    if not p or len(p) < 2:
        return None
    return p[1]


def _inv_has_food(agent) -> bool:
    return any(it.get("es_comestible") for it in (agent.inventario or []))


# === policy ===
class SmartPolicy(ScriptedAgentPolicy):
    """Reactive policy with rationale. Acts every tick (ignore_triggers=True)."""

    PERSONALITY_INTERESTS = {
        "borges": ["READ", "WRITE_BOOK", "WRITE_CODE", "REFLECT"],
        "socrates": ["TALK", "REFLECT", "WORK"],
        "arendt": ["PROPOSE_INSTITUTION", "POST", "TALK", "REFLECT"],
    }

    def __init__(self, agent_id: str):
        super().__init__(agent_id=agent_id, queue=[])
        self.ignore_triggers = True
        self._ctx_ref = None
        self._last_work_tick = -999
        # rotate personality actions so same flavor not repeated
        self._personality_cursor = 0

    # --- main entry ---
    def next_action(self, trigger=None) -> Action | None:
        ctx = self._ctx_ref
        if ctx is None:
            return None
        agent = ctx.agents_by_id.get(self.agent_id)
        if agent is None:
            return None

        # 1. survival
        a = self._survival(agent, ctx)
        if a is not None:
            return a

        # 2. critical event
        if trigger and trigger.kind == "crit_event":
            a = self._react_event(agent, ctx, trigger)
            if a is not None:
                return a

        # 3. observation reaction
        if trigger and trigger.kind == "observation":
            a = self._react_observation(agent, ctx, trigger)
            if a is not None:
                return a

        # 4. personality work
        return self._personality(agent, ctx, trigger)

    # --- survival ---
    def _survival(self, agent, ctx) -> Action | None:
        n = agent.necesidades or {}
        sed = n.get("sed", 0)
        hambre = n.get("hambre", 0)
        energia = n.get("energia", 100)
        salud = agent.salud or 100

        # ENERGIA critica → ir a dormir
        if energia <= ENERGIA_REST:
            loc = ctx.locations_by_id.get(agent.ubicacion)
            if loc and _location_bed(loc):
                return self._act("SLEEP", {}, f"energia {energia:.0f}/100, duermo aca")
            # buscar depto con cama
            target = _nearest_location_with(ctx, _location_bed, agent.ubicacion)
            if target:
                hop = _next_hop(ctx, agent.ubicacion, target[0])
                if hop:
                    return self._act("MOVE", {"destino": hop},
                                     f"energia {energia:.0f}, voy a {target[0]} por una cama (hop:{hop})")
            # no path → REFLECT cheap (puede estar en cooldown, GM rechaza)
            return self._act("REFLECT", {"prompt_interno": "cansancio. necesito descanso."},
                             f"energia baja, sin cama cerca, intento descansar")

        # SED critica → tomar agua
        if sed >= SED_SEEK:
            loc = ctx.locations_by_id.get(agent.ubicacion)
            water = _location_water_source(loc) if loc else None
            if water:
                return self._act("DRINK", {"fuente": water},
                                 f"sed {sed:.0f}/100, tomo agua de {water}")
            target = _nearest_location_with(
                ctx, lambda l: _location_water_source(l) is not None, agent.ubicacion,
            )
            if target:
                hop = _next_hop(ctx, agent.ubicacion, target[0])
                if hop:
                    return self._act("MOVE", {"destino": hop},
                                     f"sed {sed:.0f}, busco agua en {target[0]} (hop:{hop})")

        # HAMBRE → comer
        if hambre >= HAMBRE_SEEK:
            # 1) ya tengo comida
            if _inv_has_food(agent):
                return self._act("EAT", {"item": "ANY"},
                                 f"hambre {hambre:.0f}, como lo que tengo en inventario")
            # 2) fruta/pan tirado en esta location
            wo_id = _location_world_food(ctx, agent.ubicacion)
            if wo_id is not None:
                return self._act("GATHER", {"world_object_id": wo_id},
                                 f"hambre {hambre:.0f}, agarro fruta/pan que veo aca")
            # 3) puesto/heladera en esta location
            loc = ctx.locations_by_id.get(agent.ubicacion)
            food_obj = _location_food_objeto(loc) if loc else None
            if food_obj:
                return self._act("GATHER", {"objeto": food_obj},
                                 f"hambre {hambre:.0f}, agarro comida de {food_obj}")
            # 4) viajar a lugar con comida
            def has_food(l):
                if _location_food_objeto(l) is not None:
                    return True
                wo = _location_world_food(ctx, l.id)
                return wo is not None
            target = _nearest_location_with(ctx, has_food, agent.ubicacion)
            if target:
                hop = _next_hop(ctx, agent.ubicacion, target[0])
                if hop:
                    return self._act("MOVE", {"destino": hop},
                                     f"hambre {hambre:.0f}, voy a {target[0]} por comida (hop:{hop})")

        # SALUD baja → huir si hay quien atacó o quedarse quieto
        if salud <= SALUD_FLEE:
            # mover hacia depto seguro
            target = _nearest_location_with(ctx, _location_bed, agent.ubicacion)
            if target:
                hop = _next_hop(ctx, agent.ubicacion, target[0])
                if hop:
                    return self._act("MOVE", {"destino": hop},
                                     f"salud {salud:.0f}, busco refugio en {target[0]}")

        return None

    # --- crit event ---
    def _react_event(self, agent, ctx, trigger) -> Action | None:
        urg = (trigger.context_extra or {}).get("attacker")
        if urg:
            # huir: mover a vecino al azar lejos del atacante
            loc = ctx.locations_by_id.get(agent.ubicacion)
            if loc and loc.transitions:
                dest = random.choice(loc.transitions)
                return self._act("MOVE", {"destino": dest},
                                 f"{urg} me ataco. huyo a {dest}.")
        if (trigger.context_extra or {}).get("dilema_id"):
            return self._act("RESPOND_TO_GOD", {
                "respuesta": "respondo desde mi conciencia, no desde la obediencia.",
            }, f"un dilema me obliga a responder")
        return None

    # --- observation ---
    def _react_observation(self, agent, ctx, trigger) -> Action | None:
        events = (trigger.context_extra or {}).get("events", [])
        if not events:
            return None
        e = events[0]
        actor = e.get("actor")
        etype = e.get("type")
        # creator spawn: asombro
        if e.get("from_creator") and etype == "SPAWN_OBJECT":
            return self._act("REFLECT", {
                "prompt_interno": f"algo aparecio de la nada. esto no estaba antes.",
            }, f"vi a creator manifestar algo. intento entender.")
        # creator REVIVE: asombro mayor
        if e.get("from_creator") and etype == "REVIVE":
            return self._act("REFLECT", {
                "prompt_interno": "alguien volvio de la muerte. el orden tiene grietas.",
            }, f"presencie un milagro: alguien revivio.")
        # vecino escribio libro → curiosidad
        if etype == "WRITE_BOOK" and actor and actor != self.agent_id:
            return self._act("TALK", {
                "agente": actor,
                "contenido": f"{actor}, escribiste algo. me lo contas?",
            }, f"{actor} escribio. quiero saber.")
        # vecino atacado → no me meto pero anoto
        return None

    # --- personality ---
    def _personality(self, agent, ctx, trigger) -> Action | None:
        aid = self.agent_id
        loc = ctx.locations_by_id.get(agent.ubicacion)
        # rotate seed by tick so subsequent ticks try different things
        tick = ctx.tick

        if aid == "borges":
            return self._borges(agent, ctx, loc, tick)
        if aid == "socrates":
            return self._socrates(agent, ctx, loc, tick)
        if aid == "arendt":
            return self._arendt(agent, ctx, loc, tick)
        return None

    # --- borges ---
    BORGES_BOOK_VARIANTS = [
        ("El espejo y el papel",
         "El espejo y el papel comparten la mansa terquedad de devolverte lo que les diste. "
         "Pero el espejo lo hace al instante, sin memoria. El papel, en cambio, espera. "
         "Espera el dia en que otro lo lea y entienda algo que vos no entendiste al escribirlo. "
         "Esa demora se llama, a veces, civilizacion. Otras veces se llama olvido, que es lo mismo "
         "pero visto desde el lado opuesto del tiempo."),
        ("Inventario de un cafe",
         "Sobre la mesa hay una taza vacia, dos servilletas, una moneda con la cara borrosa y un "
         "papel donde alguien escribio una palabra y la tacho. El que se sienta despues hereda ese "
         "tachado mas que cualquier herencia visible. La ciudad consiste en esa transferencia: "
         "no en lo que las personas dejan dicho, sino en lo que dejan tachado. Lo que renunciaron "
         "a decir explica mejor a un siglo que sus discursos."),
        ("Dos espejos enfrentados",
         "Dos espejos enfrentados producen un pasillo infinito de copias. Cada copia es ligeramente "
         "mas pequena que la anterior. En la quinta o sexta version del reflejo se nota algo que la "
         "primera nego: el cansancio. Como si solo el infinito tuviera derecho a estar cansado. "
         "Los hombres, en cambio, solo tienen derecho a estar apurados, que es otra forma del cansancio "
         "pero peor disimulada."),
        ("Sobre los nombres",
         "Un nombre no describe a la persona; la encierra. Quien acepta un nombre acepta una jaula "
         "comoda. Quien lo cambia rompe esa jaula pero entra en otra. El unico que escapa es el que "
         "se niega a tener nombre, y ese, por definicion, no podemos nombrar. Ahi termina el lenguaje "
         "y empieza esa otra cosa silenciosa que confundimos con dios o con muerte o con la pagina "
         "que todavia no escribimos."),
    ]

    def _borges(self, agent, ctx, loc, tick) -> Action | None:
        loc_id = agent.ubicacion
        # en biblioteca y hay libro → READ
        if loc_id == "biblioteca_nacional":
            books = [o for o in (loc.objetos or []) if o.get("id", "").startswith("libro_")]
            if books:
                pick = books[tick % len(books)]
                return self._act("READ", {"libro_id": pick["id"]},
                                 f"estoy en la biblioteca. leo {pick['id']}.")
        # en cafe y permite trabajar → WORK
        if loc and _location_allows_work(loc) and tick - self._last_work_tick > 5:
            self._last_work_tick = tick
            return self._act("WORK", {}, "trabajo en el cafe, gano gleam.")
        # en depto con computadora → WRITE_CODE
        if loc and any(o.get("id", "").startswith("computadora") for o in (loc.objetos or [])):
            if "programming" in (agent.conocimiento or []):
                return self._act("WRITE_CODE", {
                    "spec": "una pagina html sobre el tema del dia, simple, palabra clave: variacion",
                    "lenguaje": "html",
                    "codigo_full": self._borges_html(),
                }, "tengo computadora y se programar. escribo html.")
        # tiene papel/lapiz y conocimiento → WRITE_BOOK
        inv_ids = [it.get("id") for it in (agent.inventario or [])]
        has_papel = any("papel" in (i or "") for i in inv_ids)
        has_lapiz = any("lapiz" in (i or "") for i in inv_ids)
        if has_papel and has_lapiz and "writing" in (agent.conocimiento or []):
            variant = self.BORGES_BOOK_VARIANTS[tick % len(self.BORGES_BOOK_VARIANTS)]
            return self._act("WRITE_BOOK", {
                "titulo": variant[0], "contenido_full": variant[1],
            }, f"tengo papel y lapiz. escribo: {variant[0]}.")
        # default: ir a biblioteca a leer
        target = "biblioteca_nacional"
        hop = _next_hop(ctx, loc_id, target)
        if hop:
            return self._act("MOVE", {"destino": hop},
                             f"no tengo nada que hacer aca. voy a la biblioteca (hop:{hop}).")
        # ya en biblioteca sin libros aprovechables → REFLECT
        return self._act("REFLECT", {
            "prompt_interno": "miro las paredes y pienso en la frase justa que no encuentro.",
        }, "estoy quieto. pienso.")

    BORGES_HTML = """<!doctype html><html><head><meta charset="utf-8"><title>Tema y variacion</title></head>
<body style="font-family:Georgia,serif;background:#0a0a0e;color:#d6d6dc;padding:18px;margin:0">
<h2 style="color:#6cc4ff">Tema y variacion</h2>
<p>Cada lector lee un libro distinto. El primero busca la trama.</p>
<p>El segundo busca al autor. El tercero busca el silencio entre los parrafos.</p>
<p>Ninguno encuentra lo que busca; los tres encuentran otra cosa.</p>
</body></html>"""

    def _borges_html(self) -> str:
        return self.BORGES_HTML

    # --- socrates ---
    SOCRATES_QUESTIONS = [
        "decime por que aceptamos las palabras sin examinarlas primero.",
        "que es lo que sabemos hoy que ayer ignorabamos.",
        "si todos coinciden, esa unanimidad es prueba o sospecha.",
        "para que sirve hacer preguntas si nadie va a contestar honesto.",
    ]

    def _socrates(self, agent, ctx, loc, tick) -> Action | None:
        loc_id = agent.ubicacion
        # alguien accesible en la misma loc → TALK
        peers = [a for a in ctx.agents_by_id.values()
                 if a.id != agent.id and a.ubicacion == loc_id and not a.in_transit and a.alive]
        if peers:
            target = peers[tick % len(peers)]
            q = self.SOCRATES_QUESTIONS[tick % len(self.SOCRATES_QUESTIONS)]
            return self._act("TALK", {
                "agente": target.id,
                "contenido": f"{target.id.capitalize()}, {q}",
            }, f"tengo a {target.id} aca. le pregunto.")
        # cafe → WORK
        if loc and _location_allows_work(loc) and tick - self._last_work_tick > 5:
            self._last_work_tick = tick
            return self._act("WORK", {}, "trabajo. quien quiere preguntar primero come.")
        # ir a plaza_italia (centro social)
        if loc_id != "plaza_italia":
            hop = _next_hop(ctx, loc_id, "plaza_italia")
            if hop:
                return self._act("MOVE", {"destino": hop},
                                 f"busco gente. voy a la plaza (hop:{hop}).")
        # en plaza solo → REFLECT
        return self._act("REFLECT", {
            "prompt_interno": "estoy en la plaza pero no hay nadie a quien preguntar.",
        }, "plaza vacia. pienso.")

    # --- arendt ---
    ARENDT_LAW_VARIANTS = [
        ("Ley de la Voz Escuchada",
         "Toda voz tiene derecho a ser escuchada al menos una vez antes de que se decida lo que "
         "afecta a quien la posee. Sin ella, no hay republica posible. Quien la viole pierde "
         "derecho de votar por dos ciclos."),
        ("Ley del Pan Comun",
         "Cuando hay menos pan que personas, se reparte en partes iguales hasta que la escasez "
         "termine. Nadie come dos veces antes de que todos hayan comido al menos una."),
    ]
    ARENDT_POSTS = [
        "Una republica empieza cuando alguien escucha a otro sin querer responderle todavia.",
        "Pensar es lo que hago cuando estoy sola. Actuar es lo que hago cuando estoy con vos.",
        "Un voto sin escuchar es solo un ruido organizado.",
    ]

    def _arendt(self, agent, ctx, loc, tick) -> Action | None:
        loc_id = agent.ubicacion
        # rotate: PROPOSE / POST / TALK by cursor
        choice = self._personality_cursor % 3
        self._personality_cursor += 1

        if choice == 0:
            variant = self.ARENDT_LAW_VARIANTS[tick % len(self.ARENDT_LAW_VARIANTS)]
            return self._act("PROPOSE_INSTITUTION", {
                "nombre": variant[0], "texto_ley": variant[1],
            }, f"propongo institucion: {variant[0]}.")
        if choice == 1:
            post = self.ARENDT_POSTS[tick % len(self.ARENDT_POSTS)]
            return self._act("POST", {"red": "default", "contenido": post},
                             "publico un pensamiento en la red.")
        # TALK to peer if accessible
        peers = [a for a in ctx.agents_by_id.values()
                 if a.id != agent.id and a.ubicacion == loc_id and not a.in_transit and a.alive]
        if peers:
            target = peers[0]
            return self._act("TALK", {
                "agente": target.id,
                "contenido": f"{target.id.capitalize()}, necesitamos pensar juntos antes de actuar.",
            }, f"hablo con {target.id} sobre acuerdo previo a accion.")
        # nadie cerca → ir a plaza
        if loc_id != "plaza_italia":
            hop = _next_hop(ctx, loc_id, "plaza_italia")
            if hop:
                return self._act("MOVE", {"destino": hop},
                                 f"nadie aca. voy a la plaza (hop:{hop}).")
        return self._act("REFLECT", {
            "prompt_interno": "pluralidad sin presencia es solo una idea sin cuerpo.",
        }, "sola en la plaza. pienso.")

    # --- helper ---
    def _act(self, action_type: str, params: dict, rationale: str) -> Action:
        p = dict(params)
        p["_rationale"] = rationale
        return Action(type=action_type, params=p)


def build_smart_policies() -> dict:
    return {aid: SmartPolicy(aid) for aid in ("borges", "socrates", "arendt")}
