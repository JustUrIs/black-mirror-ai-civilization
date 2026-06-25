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
    with get_session() as s:
        existing = s.get(Agent, "test_agent_1")
        if existing is not None:
            log.info("test_agent_1 already exists, skipping spawn")
            return
        agent = Agent(
            id="test_agent_1",
            nombre="Test Agent (Día 1)",
            seed_json={"day1_stub": True},
            avatar_sprite="default",
            clase="citizen",
            ubicacion="plaza_italia",
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
    queue = [
        # MOVE valid: plaza_italia → cafe_palermo
        Action(type="MOVE", params={"destino": "cafe_palermo"}),
        # EAT valid: medialuna_inicial in inventory
        Action(type="EAT", params={"item": "medialuna_inicial"}),
        # MOVE INVALID: from cafe_palermo no direct transition to parque_centenario
        Action(type="MOVE", params={"destino": "parque_centenario"}),
        # TALK INVALID: no other agent in cafe_palermo
        Action(type="TALK", params={"agente": "ghost", "contenido": "hola que tal todo bien?"}),
        # EAT INVALID: item already consumed
        Action(type="EAT", params={"item": "medialuna_inicial"}),
        # MOVE valid back to plaza
        Action(type="MOVE", params={"destino": "plaza_italia"}),
        # MOVE valid plaza → mercado
        Action(type="MOVE", params={"destino": "mercado_bonpland"}),
        # MOVE valid mercado → parque
        Action(type="MOVE", params={"destino": "parque_centenario"}),
        # MOVE valid parque → plaza
        Action(type="MOVE", params={"destino": "plaza_italia"}),
        # extra valid MOVE to fill 10 ticks
        Action(type="MOVE", params={"destino": "cafe_palermo"}),
    ]
    return ScriptedAgentPolicy(agent_id="test_agent_1", queue=queue)
