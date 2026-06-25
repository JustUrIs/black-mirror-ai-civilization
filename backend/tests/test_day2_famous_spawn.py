"""Day 2.7 famous spawn test: load 3 famous from JSON, verify schema integrity."""
import logging
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

TEST_DB = HERE / "test_fam.db"
TEST_CACHE = HERE / "test_fam_cache"
os.environ["DB_PATH"] = str(TEST_DB)
os.environ["LLM_CACHE_DIR"] = str(TEST_CACHE)

if TEST_DB.exists(): TEST_DB.unlink()
if TEST_CACHE.exists(): shutil.rmtree(TEST_CACHE)

logging.basicConfig(level=logging.INFO)

from src.db.session import init_db, get_session
from src.db.schema import Agent
from src.sim.bootstrap import bootstrap_world
from src.sim.seed_famous import spawn_famous


def main():
    init_db()
    bootstrap_world(map_id="moderno")
    spawned = spawn_famous()
    print(f"\nSpawned: {spawned}")

    assert set(spawned) == {"borges", "socrates", "arendt"}, spawned

    with get_session() as s:
        for fid in ("borges", "socrates", "arendt"):
            a = s.get(Agent, fid)
            assert a is not None, f"missing {fid}"
            assert a.nombre
            assert len(a.moral_lines) == 3
            assert a.primary_conflict
            assert a.ubicacion in {"plaza_italia", "cafe_palermo", "biblioteca_nacional"}
            print(f"  {a.nombre:20} @ {a.ubicacion:20} conocimiento={a.conocimiento} gleam={a.gleam}")

        # Idempotency: re-spawn should not duplicate
        spawned_2 = spawn_famous()
        assert spawned_2 == [], "re-spawn should skip existing agents"

    print("\nDay 2.7 famous spawn PASSED [OK]")


if __name__ == "__main__":
    main()
