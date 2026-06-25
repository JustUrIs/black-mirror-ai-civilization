"""Dynamics del mundo no-cognitivo: árboles que crecen, fruta que aparece.

Corre cada tick antes de las decisiones de agentes. Sealed-world: estos
spawns tienen created_by='nature' (no es ni agente ni creator).
"""
import logging
from ..db.schema import WorldObject, ActionLog


log = logging.getLogger("world_dynamics")


FRUIT_GROW_INTERVAL_TICKS = 20      # cada N ticks, arbol frutal produce 1 fruta
MAX_FRUITS_PER_TREE = 3              # cap para evitar runaway


def grow_fruit_trees(session, tick: int) -> int:
    """For cada arbol_frutal active, si han pasado N ticks desde la ultima
    spawn (o desde creacion), genera 1 fruta hijo. Returns count generated.
    """
    trees = (
        session.query(WorldObject)
        .filter(WorldObject.object_type == "arbol_frutal",
                WorldObject.state == "active")
        .all()
    )
    generated = 0
    for tree in trees:
        meta = dict(tree.metadata_json or {})
        last_spawn = meta.get("last_fruit_tick", tree.created_tick)
        fruits_total = meta.get("fruits_total", 0)
        if fruits_total >= MAX_FRUITS_PER_TREE:
            continue
        if tick - last_spawn < FRUIT_GROW_INTERVAL_TICKS:
            continue

        fruta = WorldObject(
            location_id=tree.location_id,
            object_type="fruta",
            created_by="nature",
            created_tick=tick,
            state="active",
            metadata_json={
                "parent_tree": tree.id,
                "es_comestible": True,
                "calorias": 25,
            },
        )
        session.add(fruta)
        meta["last_fruit_tick"] = tick
        meta["fruits_total"] = fruits_total + 1
        tree.metadata_json = meta
        session.add(tree)

        session.add(ActionLog(
            tick=tick, agent_id="nature", action_type="GROW_FRUIT",
            params={"tree_id": tree.id, "location": tree.location_id},
            status="accept",
            side_effect_summary=f"arbol {tree.id} produjo fruta en {tree.location_id}",
        ))
        generated += 1
    return generated
