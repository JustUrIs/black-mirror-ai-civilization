"""Day 2.2 economy test: WORK + TRADE polimorfo + sink."""
import asyncio
import logging
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

TEST_DB = HERE / "test_eco.db"
TEST_CACHE = HERE / "test_eco_cache"
os.environ["DB_PATH"] = str(TEST_DB)
os.environ["LLM_CACHE_DIR"] = str(TEST_CACHE)

if TEST_DB.exists():
    TEST_DB.unlink()
if TEST_CACHE.exists():
    shutil.rmtree(TEST_CACHE)

logging.basicConfig(level=logging.INFO, format="%(name)s %(levelname)s %(message)s")

from src.db.session import init_db, get_session
from src.db.schema import Agent, Location, ActionLog, WorldState
from src.sim.bootstrap import bootstrap_world
from src.sim.world_loop import WorldLoop, ScriptedAgentPolicy
from src.gm.actions import Action


def spawn_two_agents():
    with get_session() as s:
        cafe = s.get(Location, "cafe_palermo")
        a = Agent(
            id="alice", nombre="Alice", clase="citizen",
            ubicacion="cafe_palermo", x=cafe.x, y=cafe.y, in_transit=None,
            inventario=[{"id": "manzana", "es_comestible": True, "calorias": 20}],
            necesidades={"hambre": 30.0, "energia": 80.0, "sed": 10.0, "sueno": 5.0, "social": 50.0},
            salud=100.0, gleam=5.0, moral_lines=[], primary_conflict="",
            relaciones={}, conocimiento=[], memoria_recent=[], welfare_birch={},
        )
        b = Agent(
            id="bob", nombre="Bob", clase="citizen",
            ubicacion="cafe_palermo", x=cafe.x, y=cafe.y, in_transit=None,
            inventario=[],
            necesidades={"hambre": 50.0, "energia": 80.0, "sed": 10.0, "sueno": 5.0, "social": 50.0},
            salud=100.0, gleam=20.0, moral_lines=[], primary_conflict="",
            relaciones={}, conocimiento=[], memoria_recent=[], welfare_birch={},
        )
        s.add_all([a, b])
        s.commit()


async def main():
    init_db()
    bootstrap_world(map_id="moderno")
    spawn_two_agents()

    alice_policy = ScriptedAgentPolicy(agent_id="alice", queue=[
        # Alice works (cafe permite_trabajo=True). +1 gleam, -10 energia.
        Action(type="WORK", params={}),
        # Alice trades: ofrece manzana, pide 3 gleam de Bob (Bob tiene 20).
        Action(type="TRADE", params={
            "agente": "bob",
            "ofrezco": {"item": "manzana"},
            "pido": {"gleam": 3.0},
        }),
        # Alice intenta TRADE invalido: oferta ya no tenia (vendida).
        Action(type="TRADE", params={
            "agente": "bob",
            "ofrezco": {"item": "manzana"},
            "pido": {"gleam": 1.0},
        }),
        # Alice WORK otra vez.
        Action(type="WORK", params={}),
        # Alice WORK reject: energia <10 quizas no... 80-10=70-10=60. Aun OK.
        Action(type="WORK", params={}),
    ])

    bob_policy = ScriptedAgentPolicy(agent_id="bob", queue=[
        # Bob WORK
        Action(type="WORK", params={}),
        # Bob trade reject: en plaza_italia no permite_trabajo... wait Bob esta en cafe.
        # Bob TRADE inverso: pide manzana, ofrece 2 gleam. Alice ya no tiene manzana despues T2.
        # T3 Bob: skip
        Action(type="WORK", params={}),
        Action(type="WORK", params={}),
        Action(type="WORK", params={}),
        Action(type="WORK", params={}),
    ])

    loop = WorldLoop(
        policies={"alice": alice_policy, "bob": bob_policy},
        tick_duration_sec=0.01,
    )
    await loop.run(max_ticks=5)

    with get_session() as s:
        alice = s.get(Agent, "alice")
        bob = s.get(Agent, "bob")
        logs = s.query(ActionLog).order_by(ActionLog.id).all()

        print("\n=== LOG ===")
        for l in logs:
            tag = "OK" if l.status == "accept" else "RJ"
            msg = l.side_effect_summary if l.status == "accept" else l.error_nl
            print(f"  t{l.tick} {l.agent_id:6} {l.action_type:6} [{tag}] {msg[:90]}")

        print(f"\nAlice gleam: 5.0 -> {alice.gleam:.2f}, inventario: {alice.inventario}")
        print(f"Bob   gleam: 20.0 -> {bob.gleam:.2f}, inventario: {bob.inventario}")
        ws = s.get(WorldState, 1)
        print(f"Tax sink: {ws.sink}")

        accepts = sum(1 for l in logs if l.status == "accept")
        rejects = sum(1 for l in logs if l.status == "reject")
        assert accepts >= 6, f"expected >=6 accepts, got {accepts}"
        assert rejects >= 1, f"expected >=1 reject, got {rejects}"

        # Alice's gleam after T1 WORK (+1 - 0.1 tax). T2 TRADE (+3 - 0.1). T3 reject (no side). T4 WORK +1 -0.1.
        # Approx: 5 +1 -0.1 +3 -0.1 -0.1 +1 -0.1 +1 -0.1 = 10.5. Bob: 20 -3 +many gleam +(-0.5 tax).
        assert alice.gleam > 5.0, f"alice gleam should have grown, got {alice.gleam}"
        assert bob.gleam > 20.0, "bob did many WORK, gleam should grow despite trade"
        assert any(it.get("id") == "manzana" for it in (bob.inventario or [])), \
            "bob should now own the manzana from trade"
        assert not any(it.get("id") == "manzana" for it in (alice.inventario or [])), \
            "alice should no longer have the manzana"

    print("\nDay 2.2 economy test PASSED [OK]")


if __name__ == "__main__":
    asyncio.run(main())
