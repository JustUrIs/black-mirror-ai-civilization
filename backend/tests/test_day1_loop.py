"""Day 1 end-to-end test: bootstrap world, spawn agent, run 10 ticks,
verify ActionLog has expected accept/reject pattern.
"""
import asyncio
import logging
import os
import sys
import shutil
from pathlib import Path


# Make src importable
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

# Use isolated test DB + cache
TEST_DB = HERE / "test_eidolon.db"
TEST_CACHE = HERE / "test_cache"
os.environ["DB_PATH"] = str(TEST_DB)
os.environ["LLM_CACHE_DIR"] = str(TEST_CACHE)

if TEST_DB.exists():
    TEST_DB.unlink()
if TEST_CACHE.exists():
    shutil.rmtree(TEST_CACHE)

logging.basicConfig(level=logging.INFO, format="%(name)s %(levelname)s %(message)s")

from src.db.session import init_db, get_session
from src.db.schema import ActionLog, Agent, WorldState
from src.sim.bootstrap import bootstrap_world
from src.sim.seed_day1 import spawn_test_agent, build_test_policy
from src.sim.world_loop import WorldLoop


async def main():
    init_db()
    bootstrap_world(map_id="moderno")
    spawn_test_agent()

    policy = build_test_policy()
    loop = WorldLoop(
        policies={"test_agent_1": policy},
        tick_duration_sec=0.01,  # 10ms — fast test
    )

    await loop.run(max_ticks=10)

    # Assertions
    with get_session() as s:
        ws = s.get(WorldState, 1)
        assert ws.tick_actual == 10, f"expected tick_actual=10, got {ws.tick_actual}"

        logs = s.query(ActionLog).order_by(ActionLog.id).all()
        # With N-tick travel some ticks have no action (in_transit). Logs < 10.
        print(f"  total ActionLog entries: {len(logs)}")

        accepts = [l for l in logs if l.status == "accept"]
        rejects = [l for l in logs if l.status == "reject"]
        print(f"  accepts={len(accepts)}  rejects={len(rejects)}")

        assert len(rejects) >= 2, f"expected >=2 rejects (anti-bullshit working), got {len(rejects)}"
        assert len(accepts) >= 3, f"expected >=3 accepts, got {len(accepts)}"

        for r in rejects:
            assert r.error_nl, f"reject without error_nl on tick {r.tick}"
            print(f"  reject tick={r.tick} action={r.action_type}: {r.error_nl[:90]}")

        for a in accepts:
            assert a.side_effect_summary, f"accept without summary on tick {a.tick}"
            print(f"  accept tick={a.tick} action={a.action_type}: {a.side_effect_summary[:90]}")

        agent = s.get(Agent, "test_agent_1")
        print(f"  agent final location: {agent.ubicacion}")
        print(f"  agent (x,y): ({agent.x},{agent.y})")
        print(f"  agent in_transit: {agent.in_transit}")
        print(f"  agent necesidades: {agent.necesidades}")
        print(f"  agent inventario: {agent.inventario}")
        assert len(agent.inventario) == 0, "medialuna should have been eaten"
        assert agent.necesidades["hambre"] < 20.0, "EAT should have reduced hambre"

    print("\nDay 2.1 end-to-end test PASSED [OK]")


if __name__ == "__main__":
    asyncio.run(main())
