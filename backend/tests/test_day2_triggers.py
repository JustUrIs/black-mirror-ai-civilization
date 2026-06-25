"""Day 2.5 triggers test."""
import logging
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

TEST_DB = HERE / "test_trig.db"
TEST_CACHE = HERE / "test_trig_cache"
os.environ["DB_PATH"] = str(TEST_DB)
os.environ["LLM_CACHE_DIR"] = str(TEST_CACHE)

if TEST_DB.exists(): TEST_DB.unlink()
if TEST_CACHE.exists(): shutil.rmtree(TEST_CACHE)

logging.basicConfig(level=logging.WARNING)

from src.db.session import init_db, get_session
from src.db.schema import Agent, Location, Dilema, ActionLog
from src.sim.bootstrap import bootstrap_world
from src.sim.triggers import classify_trigger


def make_agent(s, id, hambre=20.0, sed=10.0, energia=80.0, salud=100.0):
    loc = s.get(Location, "cafe_palermo")
    a = Agent(
        id=id, nombre=id, clase="citizen", ubicacion="cafe_palermo",
        x=loc.x, y=loc.y, in_transit=None,
        inventario=[], necesidades={"hambre": hambre, "sed": sed, "energia": energia, "sueno": 0.0, "social": 50.0},
        salud=salud, gleam=10.0, conocimiento=[], relaciones={}, memoria_recent=[],
        moral_lines=[], primary_conflict="", welfare_birch={},
    )
    s.add(a)
    s.flush()
    return a


def main():
    init_db()
    bootstrap_world()
    with get_session() as s:
        # 1. Crit need: hambre
        a = make_agent(s, "hungry", hambre=90.0)
        t = classify_trigger(a, s, tick=5)
        assert t.kind == "crit_need" and t.context_extra["urgency"] == "hambre", t

        # 2. Crit need: energia
        b = make_agent(s, "tired", energia=15.0)
        t = classify_trigger(b, s, tick=5)
        assert t.kind == "crit_need" and t.context_extra["urgency"] == "energia", t

        # 3. Crit event: active dilema
        d = Dilema(texto="quien come?", launched_tick=4, active=True)
        s.add(d); s.flush()
        c = make_agent(s, "normal_dude")
        t = classify_trigger(c, s, tick=5)
        assert t.kind == "crit_event" and "dilema_id" in t.context_extra, t

        # 4. Inactivate dilema, normal vs skip
        d.active = False; s.add(d); s.flush()
        t = classify_trigger(c, s, tick=6)  # 6 % 3 == 0 → normal
        assert t.kind == "normal", t
        t = classify_trigger(c, s, tick=7)  # 7 % 3 != 0 → skip
        assert t.kind == "skip", t

        # 5. Observation: someone else wrote a book this tick
        s.add(ActionLog(tick=10, agent_id="hungry", action_type="WRITE_BOOK",
                        params={"titulo":"x"}, status="accept", side_effect_summary="..."))
        s.flush()
        t = classify_trigger(c, s, tick=10)
        # tick 10 % 3 != 0 → would be skip, but observation overrides at tick 10
        assert t.kind == "observation", f"expected observation, got {t.kind} ({t.reason})"

        # 6. Recent ATTACK against c
        s.add(ActionLog(tick=11, agent_id="hungry", action_type="ATTACK",
                        params={"agente":"normal_dude"}, status="accept", side_effect_summary="x"))
        s.flush()
        t = classify_trigger(c, s, tick=12)
        assert t.kind == "crit_event" and t.context_extra.get("attacker") == "hungry", t

        s.commit()

    print("Day 2.5 trigger classification PASSED [OK]")


if __name__ == "__main__":
    main()
