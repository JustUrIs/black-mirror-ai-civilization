"""Day 1: spawn 1 hardcoded agent with scripted action queue.

This file proves end-to-end loop: agent → policy → GM → SQLite → log.
"""
import logging
from sqlalchemy.exc import IntegrityError

from ..db.session import get_session
from ..db.schema import Agent
from ..gm.actions import Action
from .world_loop import ScriptedAgentPolicy


log = logging.getLogger("seed_day1")


def spawn_test_agent() -> None:
    """Insert 1 test agent if not exists."""
    from ..db.schema import Location
    with get_session() as s:
        existing = s.get(Agent, "test_agent_1")
        if existing is not None:
            log.info("test_agent_1 already exists, skipping spawn")
            return
        loc = s.get(Location, "plaza_italia")
        spawn_x = loc.x if loc else 0.0
        spawn_y = loc.y if loc else 0.0
        agent = Agent(
            id="test_agent_1",
            nombre="Test Agent (Día 1)",
            seed_json={"day1_stub": True},
            avatar_sprite="default",
            clase="citizen",
            ubicacion="plaza_italia",
            x=spawn_x,
            y=spawn_y,
            in_transit=None,
            inventario=[
                {"id": "medialuna_inicial", "es_comestible": True, "calorias": 30}
            ],
            necesidades={
                "hambre": 20.0, "energia": 90.0, "sed": 10.0,
                "sueno": 5.0, "social": 50.0,
            },
            salud=100.0,
            gleam=10.0,
            memoria_recent=[],
            memoria_summary="",
            conocimiento=[],
            relaciones={},
            intencion_actual="",
            moral_lines=["no mentir", "no traicionar"],
            primary_conflict="explorar vs descansar",
            rol_emergente=None,
            welfare_birch={"frustracion": 0, "satisfaccion": 0},
            alive=True,
        )
        try:
            s.add(agent)
            s.commit()
            log.info("spawned test_agent_1")
        except IntegrityError:
            s.rollback()
            log.exception("spawn failed")


def build_test_policy() -> ScriptedAgentPolicy:
    """Hardcoded action queue exercising MOVE (valid), MOVE (invalid),
    TALK (rejected — no other agent), EAT (valid), MOVE (valid).
    """
    # With N-tick travel: plaza<->cafe is ~7 units / 5 walk_speed = 2 ticks.
    # Each MOVE consumes 2 ticks (action tick + 1 advance_transit tick before arrival).
    queue = [
        Action(type="MOVE", params={"destino": "cafe_palermo"}),                # T1: start trip 2t
        # T2 in_transit no action
        Action(type="EAT", params={"item": "medialuna_inicial"}),               # T3: arrived, eat (accept)
        Action(type="MOVE", params={"destino": "plaza_italia"}),                # T4: start trip back
        # T5 in_transit
        Action(type="TALK", params={"agente": "ghost", "contenido": "hola che todo bien?"}),  # T6: reject ghost
        Action(type="EAT", params={"item": "medialuna_inicial"}),               # T7: reject (consumed)
        Action(type="MOVE", params={"destino": "cafe_palermo"}),                # T8: start trip
        # T9 in_transit
        Action(type="MOVE", params={"destino": "parque_centenario"}),           # T10: reject (no transition from cafe to parque)
    ]
    return ScriptedAgentPolicy(agent_id="test_agent_1", queue=queue)
