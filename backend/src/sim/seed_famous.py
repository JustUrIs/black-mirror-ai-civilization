"""Spawn pre-curated famous agents (Borges, Socrates, Arendt) from JSON.

Reads seeds/famous/*.json. Skips agents that already exist (idempotent).
Returns list of newly spawned ids.
"""
import json
import logging
from pathlib import Path

from ..db.session import get_session
from ..db.schema import Agent, Location


log = logging.getLogger("seed_famous")

SEEDS_DIR = Path(__file__).resolve().parents[3] / "seeds" / "famous"


DEFAULT_NEEDS = {
    "hambre": 25.0,
    "energia": 85.0,
    "sed": 15.0,
    "sueno": 5.0,
    "social": 50.0,
}


def _load_all_seeds() -> list[dict]:
    seeds = []
    if not SEEDS_DIR.exists():
        log.warning("seeds dir not found: %s", SEEDS_DIR)
        return seeds
    for p in sorted(SEEDS_DIR.glob("*.json")):
        try:
            seeds.append(json.loads(p.read_text(encoding="utf-8")))
        except Exception as e:
            log.exception("failed to load %s: %s", p, e)
    return seeds


def spawn_famous() -> list[str]:
    spawned: list[str] = []
    seeds = _load_all_seeds()
    with get_session() as s:
        for seed in seeds:
            sid = seed["id"]
            if s.get(Agent, sid) is not None:
                continue
            spawn_loc = seed.get("spawn_location", "plaza_italia")
            loc = s.get(Location, spawn_loc)
            x, y = (loc.x, loc.y) if loc else (0.0, 0.0)
            agent = Agent(
                id=sid,
                nombre=seed["nombre"],
                seed_json=seed,
                avatar_sprite=seed.get("avatar_sprite", "default"),
                clase="citizen",
                ubicacion=spawn_loc,
                x=x, y=y,
                in_transit=None,
                inventario=list(seed.get("starting_inventory", [])),
                necesidades=dict(DEFAULT_NEEDS),
                salud=100.0,
                gleam=float(seed.get("gleam_inicial", 10.0)),
                memoria_recent=[],
                memoria_summary="",
                conocimiento=list(seed.get("knowledge_inicial", [])),
                relaciones={},
                intencion_actual="",
                moral_lines=list(seed.get("moral_lines", [])),
                primary_conflict=seed.get("primary_conflict", ""),
                rol_emergente=None,
                welfare_birch={"frustracion": 0, "satisfaccion": 0},
                alive=True,
                last_reflect_tick=0,
                sleeping_until_tick=0,
            )
            s.add(agent)
            spawned.append(sid)
        s.commit()
    if spawned:
        log.info("spawned famous: %s", spawned)
    return spawned
