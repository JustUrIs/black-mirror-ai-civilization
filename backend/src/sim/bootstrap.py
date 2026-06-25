"""Bootstrap world state from JSON map + seeds.

Day 1: stub. Loads map JSON into Locations table + initializes WorldState row.
Day 2+: agent spawning from seeds.
"""
import json
import os
from pathlib import Path
from sqlalchemy import select

from ..db.session import get_session
from ..db.schema import WorldState, Location


MAPS_DIR = Path(__file__).resolve().parents[3] / "maps"


def bootstrap_world(map_id: str | None = None) -> None:
    map_id = map_id or os.getenv("MAP_ID", "moderno")
    with get_session() as s:
        ws = s.get(WorldState, 1)
        if ws is None:
            ws = WorldState(
                id=1,
                tick_actual=0,
                tick_duration_sec=int(os.getenv("TICK_DURATION_SEC", "30")),
                mapa_id=map_id,
                charter="rawls_maximin",
                tech_level="modern",
                faucet={"work_tick": 1.0, "sell_artifact_used": 5.0},
                sink={"tax_per_tick": 0.1, "llm_call": 0.5},
                recursos_base={"agua": 999999, "comida": 1000, "energia_electrica": 999999},
                conocimiento_publico=["writing", "programming", "money", "voting"],
            )
            s.add(ws)

        existing = {row.id for row in s.execute(select(Location)).scalars().all()}
        map_path = MAPS_DIR / f"{map_id}.json"
        if map_path.exists():
            data = json.loads(map_path.read_text(encoding="utf-8"))
            for loc in data.get("locations", []):
                if loc["id"] in existing:
                    continue
                s.add(Location(
                    id=loc["id"],
                    nombre_display=loc["nombre_display"],
                    tipo=loc["tipo"],
                    objetos=loc.get("objetos", []),
                    asiento_publico=loc.get("asiento_publico", False),
                    transitions=loc.get("transitions", []),
                    x=float(loc.get("x", 0.0)),
                    y=float(loc.get("y", 0.0)),
                    radius=float(loc.get("radius", 5.0)),
                    permite_trabajo=bool(loc.get("permite_trabajo", False)),
                ))

        s.commit()


def get_map_walk_speed(map_id: str | None = None) -> float:
    map_id = map_id or os.getenv("MAP_ID", "moderno")
    map_path = MAPS_DIR / f"{map_id}.json"
    if not map_path.exists():
        return 5.0
    data = json.loads(map_path.read_text(encoding="utf-8"))
    return float(data.get("walk_speed_per_tick", 5.0))
