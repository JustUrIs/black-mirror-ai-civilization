"""Day 4 test: physics (THROW + death), fruit tree growth, observation triggers."""
import logging, os, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

TEST_DB = HERE / "test_day4.db"
TEST_CACHE = HERE / "test_day4_cache"
os.environ["DB_PATH"] = str(TEST_DB)
os.environ["LLM_CACHE_DIR"] = str(TEST_CACHE)
if TEST_DB.exists(): TEST_DB.unlink()
if TEST_CACHE.exists(): shutil.rmtree(TEST_CACHE)

logging.basicConfig(level=logging.WARNING)

from src.db.session import init_db, get_session
from src.db.schema import (
    Agent, Location, WorldObject, ActionLog, WorldState,
)
from src.sim.bootstrap import bootstrap_world
from src.sim.world_dynamics import grow_fruit_trees, FRUIT_GROW_INTERVAL_TICKS
from src.gm.validator import GameMaster
from src.gm.actions import Action


def spawn_agent(s, aid, loc_id):
    loc = s.get(Location, loc_id)
    a = Agent(
        id=aid, nombre=aid.capitalize(), clase="citizen",
        ubicacion=loc_id, x=loc.x, y=loc.y, in_transit=None,
        inventario=[], necesidades={"hambre": 20, "energia": 90, "sed": 10, "sueno": 5, "social": 50},
        salud=100.0, gleam=10.0, conocimiento=[], relaciones={}, memoria_recent=[],
        moral_lines=[], primary_conflict="", welfare_birch={},
        emotional_state={"animo": 50, "miedo": 0, "asombro": 30, "dignidad": 70,
                         "esperanza": 50, "soledad": 30, "verguenza": 0},
        personal_history=[],
    )
    s.add(a)
    s.flush()
    return a


def test_throw_kills():
    init_db()
    bootstrap_world()
    gm = GameMaster()
    with get_session() as s:
        a = spawn_agent(s, "thrower", "plaza_italia")
        b = spawn_agent(s, "victim", "plaza_italia")
        # Spawn piedra en location
        wo = WorldObject(
            location_id="plaza_italia", object_type="piedra",
            created_by="creator", created_tick=0, state="active",
            metadata_json={},
        )
        s.add(wo); s.flush()
        ws = s.get(WorldState, 1)
        # 3 piedrazos (damage=40 cada uno; victim arranca con salud=100)
        for i in range(3):
            ctx = gm.build_context(s, tick=i+1)
            r = gm.validate_and_apply(
                ctx.agents_by_id["thrower"],
                Action(type="THROW", params={"objeto_id": wo.id, "agente": "victim"}),
                ctx,
            )
            # solo 1er throw acepta (despues object esta thrown ya)
            if i == 0:
                assert hasattr(r, "side_effect_summary"), r.error_nl
            else:
                assert hasattr(r, "error_nl"), "object debe quedar 'thrown' state"
                break

        # victim deberia tener 60 salud (100 - 40)
        v = s.get(Agent, "victim")
        assert v.salud == 60.0, f"esperado 60, got {v.salud}"
        assert v.alive == True

        # Mas tiradas con NUEVAS piedras hasta matar
        for k in range(2):
            wo2 = WorldObject(
                location_id="plaza_italia", object_type="piedra",
                created_by="creator", created_tick=10+k, state="active",
                metadata_json={},
            )
            s.add(wo2); s.flush()
            ctx = gm.build_context(s, tick=10+k+1)
            r = gm.validate_and_apply(
                ctx.agents_by_id["thrower"],
                Action(type="THROW", params={"objeto_id": wo2.id, "agente": "victim"}),
                ctx,
            )
            assert hasattr(r, "side_effect_summary"), r.error_nl

        # victim muerta (60 - 40 - 40 = -20 → 0)
        v2 = s.get(Agent, "victim")
        assert v2.alive == False, f"victim debe estar muerta, alive={v2.alive} salud={v2.salud}"
        s.commit()
    print("[OK] THROW + death")


def test_fruit_grow():
    with get_session() as s:
        # Spawn arbol_frutal
        ws = s.get(WorldState, 1)
        tree = WorldObject(
            location_id="parque_centenario", object_type="arbol_frutal",
            created_by="creator", created_tick=100, state="active",
            metadata_json={},
        )
        s.add(tree); s.flush()
        tree_id = tree.id

        # Pasar tiempo (menos de N ticks → 0 fruta)
        n = grow_fruit_trees(s, tick=100 + FRUIT_GROW_INTERVAL_TICKS - 1)
        assert n == 0, f"esperaba 0 frutas antes de interval, got {n}"

        # Justo en interval → 1 fruta
        n = grow_fruit_trees(s, tick=100 + FRUIT_GROW_INTERVAL_TICKS)
        assert n == 1, f"esperaba 1 fruta a interval, got {n}"

        s.flush()
        # leer metadata sin refresh (refresh recargaria de DB sin commit)
        assert (tree.metadata_json or {}).get("fruits_total") == 1, \
            f"esperaba fruits_total=1, got {tree.metadata_json}"

        frutas = s.query(WorldObject).filter_by(object_type="fruta").all()
        assert len(frutas) == 1
        assert frutas[0].metadata_json.get("es_comestible") == True
        s.commit()
    print("[OK] fruit tree growth")


def test_gather_world_object():
    gm = GameMaster()
    with get_session() as s:
        # Use existing thrower agent + fruta
        fruta = s.query(WorldObject).filter_by(object_type="fruta", state="active").first()
        assert fruta is not None
        # Spawn agent en mismo location que la fruta
        a = spawn_agent(s, "gatherer", fruta.location_id)
        ctx = gm.build_context(s, tick=200)
        fruta_id = fruta.id
        r = gm.validate_and_apply(
            ctx.agents_by_id["gatherer"],
            Action(type="GATHER", params={"world_object_id": fruta_id}),
            ctx,
        )
        msg = r.side_effect_summary if hasattr(r, "side_effect_summary") else r.error_nl
        print(f"  GATHER result: {msg}")
        assert hasattr(r, "side_effect_summary"), r.error_nl

        s.flush()
        fruta_after = s.get(WorldObject, fruta_id)
        print(f"  fruta state after flush: {fruta_after.state}")
        assert fruta_after.state == "consumed", f"expected consumed, got {fruta_after.state}"

        # Inventario contiene la fruta
        gatherer = s.get(Agent, "gatherer")
        ids = [it.get("id") for it in (gatherer.inventario or [])]
        assert any("fruta" in (i or "") for i in ids)

        # Ahora EAT con ANY debe funcionar
        r2 = gm.validate_and_apply(
            ctx.agents_by_id["gatherer"],
            Action(type="EAT", params={"item": "ANY"}),
            ctx,
        )
        assert hasattr(r2, "side_effect_summary"), r2.error_nl
        s.commit()
    print("[OK] GATHER world_object + EAT any")


def test_write_code_html():
    gm = GameMaster()
    with get_session() as s:
        # Agente en depto_almagro_1 (tiene computadora_1) con knowledge programming
        a = spawn_agent(s, "coder", "depto_almagro_1")
        a.conocimiento = ["programming", "writing"]
        s.add(a); s.flush()
        ctx = gm.build_context(s, tick=300)
        html = "<!doctype html><html><body><h1>hola</h1></body></html>"
        r = gm.validate_and_apply(
            ctx.agents_by_id["coder"],
            Action(type="WRITE_CODE", params={
                "spec": "una pagina html minima de demo para el sistema simple test mvp dia 4",
                "lenguaje": "html",
                "codigo_full": html,
            }),
            ctx,
        )
        assert hasattr(r, "side_effect_summary"), r.error_nl
        s.flush()
        from src.db.schema import CodeArtifact
        arts = s.query(CodeArtifact).all()
        assert any(a.lenguaje == "html" and "hola" in (a.codigo or "") for a in arts), \
            f"esperaba code artifact HTML con 'hola', got {[(a.lenguaje, a.codigo[:50]) for a in arts]}"
        s.commit()
    print("[OK] WRITE_CODE html stored")


def test_emotions_updates():
    from src.sim.emotions import update_agent_emotions
    with get_session() as s:
        a = spawn_agent(s, "observer", "plaza_italia")
        # Pre: defaults
        assert (a.emotional_state or {}).get("miedo", 0) == 0

        # Observa SPAWN_OBJECT del creator
        update_agent_emotions(a, [
            {"actor": "creator", "type": "SPAWN_OBJECT", "from_creator": True, "tick": 5}
        ], tick=5)
        assert a.emotional_state["asombro"] > 30, "asombro debio crecer"
        assert any(h["type"] == "intervencion_divina" for h in (a.personal_history or []))

        # Observa ATTACK
        update_agent_emotions(a, [
            {"actor": "x", "type": "ATTACK", "tick": 10}
        ], tick=10)
        assert a.emotional_state["miedo"] > 10, "miedo debio crecer post-ATTACK"
        s.add(a); s.commit()
    print("[OK] emotions update")


def main():
    test_throw_kills()
    test_fruit_grow()
    test_gather_world_object()
    test_write_code_html()
    test_emotions_updates()
    print("\nDay 4 dynamics test PASSED [OK]")


if __name__ == "__main__":
    main()
