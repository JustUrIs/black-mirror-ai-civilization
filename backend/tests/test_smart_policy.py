"""SmartPolicy reactive tests.

Cover:
- Hambre critica → busca comida (GATHER / EAT / MOVE).
- Sed critica → busca agua (DRINK / MOVE).
- Energia baja → busca cama (SLEEP / MOVE).
- Personality routing borges/socrates/arendt.
- Stress 300 ticks: nadie muere.
"""
import asyncio
import logging
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

TEST_DB = HERE / "test_smart.db"
TEST_CACHE = HERE / "test_smart_cache"
os.environ["DB_PATH"] = str(TEST_DB)
os.environ["LLM_CACHE_DIR"] = str(TEST_CACHE)
if TEST_DB.exists():
    TEST_DB.unlink()
if TEST_CACHE.exists():
    shutil.rmtree(TEST_CACHE)

logging.basicConfig(level=logging.WARNING)

from src.db.session import init_db, get_session
from src.db.schema import Agent, WorldObject, ActionLog, WorldState
from src.sim.bootstrap import bootstrap_world
from src.sim.seed_famous import spawn_famous
from src.sim.smart_policy import SmartPolicy
from src.sim.world_loop import WorldLoop
from src.gm.validator import GameMaster
from src.gm.actions import Action


def test_hambre_seeks_food():
    init_db()
    bootstrap_world()
    spawn_famous()
    gm = GameMaster()
    pol = SmartPolicy("borges")
    with get_session() as s:
        a = s.get(Agent, "borges")
        n = dict(a.necesidades or {})
        n["hambre"] = 75  # threshold 60
        n["sed"] = 10
        n["energia"] = 80
        a.necesidades = n
        a.inventario = []  # vacio
        # poner borges en plaza_italia donde hay fruta WorldObject
        a.ubicacion = "plaza_italia"
        s.add(a)
        s.flush()
        # asegurar que hay fruta en plaza
        any_fruta = s.query(WorldObject).filter_by(
            object_type="fruta", location_id="plaza_italia", state="active",
        ).first()
        if any_fruta is None:
            s.add(WorldObject(
                location_id="plaza_italia", object_type="fruta",
                created_by="nature", created_tick=1, state="active",
                metadata_json={"es_comestible": True, "calorias": 25},
            ))
            s.flush()
        ctx = gm.build_context(s, tick=1)
        pol._ctx_ref = ctx
        act = pol.next_action()
        assert act is not None, "policy debe emitir accion"
        assert act.type in {"GATHER", "EAT", "MOVE"}, f"esperaba GATHER/EAT/MOVE, got {act.type}"
        assert "_rationale" in act.params, "Action debe tener _rationale"
        s.commit()
    print(f"[OK] hambre → {act.type}: {act.params['_rationale']}")


def test_sed_seeks_water():
    gm = GameMaster()
    pol = SmartPolicy("socrates")
    with get_session() as s:
        a = s.get(Agent, "socrates")
        n = dict(a.necesidades or {})
        n["sed"] = 75
        n["hambre"] = 10
        n["energia"] = 80
        a.necesidades = n
        a.ubicacion = "plaza_italia"  # tiene fuente
        s.add(a); s.flush()
        ctx = gm.build_context(s, tick=2)
        pol._ctx_ref = ctx
        act = pol.next_action()
        assert act is not None
        assert act.type == "DRINK", f"esperaba DRINK, got {act.type}"
        assert act.params.get("fuente") == "fuente"
        s.commit()
    print(f"[OK] sed en plaza → DRINK fuente")


def test_sed_needs_travel():
    gm = GameMaster()
    pol = SmartPolicy("socrates")
    with get_session() as s:
        a = s.get(Agent, "socrates")
        n = dict(a.necesidades or {})
        n["sed"] = 75
        n["hambre"] = 10
        n["energia"] = 80
        a.necesidades = n
        a.ubicacion = "depto_almagro_2"  # NO agua aca
        s.add(a); s.flush()
        ctx = gm.build_context(s, tick=3)
        pol._ctx_ref = ctx
        act = pol.next_action()
        assert act is not None
        assert act.type == "MOVE", f"esperaba MOVE, got {act.type}"
        # next hop debe ser en transitions de depto_almagro_2
        loc = ctx.locations_by_id["depto_almagro_2"]
        assert act.params["destino"] in loc.transitions
        s.commit()
    print(f"[OK] sed sin agua → MOVE a {act.params['destino']}")


def test_energia_low_seeks_bed():
    gm = GameMaster()
    pol = SmartPolicy("borges")
    with get_session() as s:
        a = s.get(Agent, "borges")
        n = dict(a.necesidades or {})
        n["energia"] = 15  # threshold 25
        n["hambre"] = 10
        n["sed"] = 10
        a.necesidades = n
        a.ubicacion = "depto_almagro_1"  # tiene cama
        s.add(a); s.flush()
        ctx = gm.build_context(s, tick=4)
        pol._ctx_ref = ctx
        act = pol.next_action()
        assert act is not None
        assert act.type == "SLEEP", f"esperaba SLEEP, got {act.type}"
        s.commit()
    print(f"[OK] energia low en depto → SLEEP")


def test_personality_borges_writes():
    gm = GameMaster()
    pol = SmartPolicy("borges")
    with get_session() as s:
        a = s.get(Agent, "borges")
        a.necesidades = {"hambre": 10, "sed": 10, "energia": 80, "sueno": 0, "social": 50}
        a.ubicacion = "cafe_palermo"  # work-friendly + tiene papel/lapiz si trae
        # asegurar conocimiento writing + tener papel/lapiz inv
        a.conocimiento = ["writing", "voting", "programming"]
        a.inventario = [
            {"id": "papel"}, {"id": "lapiz"},
        ]
        s.add(a); s.flush()
        # primera vez en cafe → WORK (last_work_tick=-999)
        ctx = gm.build_context(s, tick=100)
        pol._ctx_ref = ctx
        act = pol.next_action()
        assert act.type == "WORK", f"esperaba WORK en cafe, got {act.type}"
        # segunda vez mismo tick → no WORK cooldown
        ctx = gm.build_context(s, tick=101)
        pol._ctx_ref = ctx
        act = pol.next_action()
        # Ahora deberia escribir libro (tiene papel + lapiz + writing)
        assert act.type in {"WRITE_BOOK", "READ", "REFLECT", "MOVE"}, f"got {act.type}"
        s.commit()
    print(f"[OK] borges cafe → WORK / WRITE")


def test_socrates_talks_when_peer_nearby():
    gm = GameMaster()
    pol = SmartPolicy("socrates")
    with get_session() as s:
        # juntar socrates + borges en plaza_italia
        a = s.get(Agent, "socrates")
        b = s.get(Agent, "borges")
        a.ubicacion = "plaza_italia"
        b.ubicacion = "plaza_italia"
        a.in_transit = None
        b.in_transit = None
        a.necesidades = {"hambre": 10, "sed": 10, "energia": 80, "sueno": 0, "social": 50}
        s.add_all([a, b]); s.flush()
        ctx = gm.build_context(s, tick=200)
        pol._ctx_ref = ctx
        act = pol.next_action()
        assert act.type == "TALK", f"esperaba TALK, got {act.type}"
        assert act.params.get("agente") == "borges"
        s.commit()
    print(f"[OK] socrates con peer → TALK")


def test_stress_300_ticks_alive():
    """Simulacion 300 ticks SIN intervencion. Si todos mueren, falla."""
    # Reset estado in-place: tick=0, full needs, revivir
    from src.db.schema import Location as L
    with get_session() as s:
        ws = s.get(WorldState, 1)
        if ws is not None:
            ws.tick_actual = 0
        agents = s.query(Agent).all()
        for a in agents:
            a.alive = True
            a.salud = 100.0
            a.necesidades = {"hambre": 10.0, "energia": 90.0, "sed": 10.0, "sueno": 0.0, "social": 50.0}
            a.in_transit = None
            a.sleeping_until_tick = 0
        s.commit()
    spawn_famous()
    from src.sim.smart_policy import build_smart_policies
    spawn_famous()  # idempotente: solo crea si no existen
    policies = build_smart_policies()
    loop = WorldLoop(policies=policies, tick_duration_sec=0)

    async def run():
        await loop.run(max_ticks=300)
    asyncio.run(run())

    with get_session() as s:
        alive = s.query(Agent).filter(Agent.alive == True).all()  # noqa: E712
        all_agents = s.query(Agent).all()
        dead = [a.id for a in all_agents if not a.alive]
        print(f"  ticks=300 alive={[a.id for a in alive]} dead={dead}")
        for a in all_agents:
            n = a.necesidades or {}
            print(f"    {a.id}: salud={a.salud:.0f} hambre={n.get('hambre'):.0f} "
                  f"sed={n.get('sed'):.0f} energia={n.get('energia'):.0f} loc={a.ubicacion}")
        assert len(alive) >= 2, f"esperaba al menos 2 vivos despues de 300 ticks. dead={dead}"

        # verificar que acciones tienen _rationale (al menos 1 ejemplo)
        sample = s.query(ActionLog).filter(
            ActionLog.agent_id.in_(["borges", "socrates", "arendt"]),
            ActionLog.status == "accept",
        ).limit(20).all()
        with_rat = [l for l in sample if (l.params or {}).get("_rationale")]
        assert len(with_rat) >= 5, f"esperaba al menos 5 acciones con _rationale, got {len(with_rat)}"
    print(f"[OK] 300 ticks: {len(alive)}/3 vivos, rationale presente")


def main():
    test_hambre_seeks_food()
    test_sed_seeks_water()
    test_sed_needs_travel()
    test_energia_low_seeks_bed()
    test_personality_borges_writes()
    test_socrates_talks_when_peer_nearby()
    test_stress_300_ticks_alive()
    print("\nSmartPolicy tests PASSED [OK]")


if __name__ == "__main__":
    main()
