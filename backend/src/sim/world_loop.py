"""World loop: deterministic tick + GM application + agent decision.

Day 1: 1 hardcoded agent with scripted action list.
Day 2: replace scripted list with LLM-driven decisions.
"""
import asyncio
import logging
from dataclasses import dataclass, field
from typing import Callable

from ..db.session import get_session
from ..db.schema import Agent, WorldState
from ..gm.actions import Action
from ..gm.validator import GameMaster
from .triggers import classify_trigger, Trigger
from .emotions import update_agent_emotions
from .world_dynamics import grow_fruit_trees


log = logging.getLogger("world_loop")


NEED_DECAY_PER_TICK = {
    "hambre": 1.0,
    "energia": -0.5,   # negative = energy drops slower than hunger
    "sed": 1.5,
    "sueno": 0.8,
    "social": 0.3,
}


@dataclass
class ScriptedAgentPolicy:
    """Day 1 only: returns the next action from a hardcoded queue.

    Ignores trigger info (legacy). Useful for deterministic tests.
    """
    agent_id: str
    queue: list[Action] = field(default_factory=list)
    ignore_triggers: bool = True

    def next_action(self, trigger: Trigger | None = None) -> Action | None:
        if not self.queue:
            return None
        return self.queue.pop(0)


def advance_transit(agent: Agent, locations_by_id: dict) -> str | None:
    """If agent is in_transit, decrement ticks_restantes. On arrival,
    set ubicacion + x/y to destino and clear in_transit.

    Returns a human-readable progress line (logged), or None if not in transit.
    """
    if not agent.in_transit:
        return None
    it = dict(agent.in_transit)
    it["ticks_restantes"] = max(0, it.get("ticks_restantes", 0) - 1)
    if it["ticks_restantes"] <= 0:
        dest = it["destino"]
        loc = locations_by_id.get(dest)
        agent.ubicacion = dest
        if loc is not None:
            agent.x = loc.x
            agent.y = loc.y
        agent.in_transit = None
        return f"llegada: {dest}"
    agent.in_transit = it
    return f"viajando a {it['destino']} ({it['ticks_restantes']} ticks restantes)"


def decay_needs(agent: Agent) -> None:
    necesidades = dict(agent.necesidades or {})
    for key, delta in NEED_DECAY_PER_TICK.items():
        cur = necesidades.get(key, 0.0)
        # 'energia' is special: decay reduces value (not raise it)
        if key == "energia":
            necesidades[key] = max(0.0, cur + delta)
        else:
            necesidades[key] = min(100.0, cur + delta)
    agent.necesidades = necesidades
    # health drop if extreme hunger
    if necesidades.get("hambre", 0) >= 95:
        agent.salud = max(0.0, agent.salud - 5)
    if agent.salud <= 0:
        agent.alive = False


def apply_economy_sink(agent: Agent, sink: dict) -> None:
    """Per-tick automatic sink (tax). Drains gleam, can go to 0 (not negative)."""
    tax = float(sink.get("tax_per_tick", 0.0))
    if tax <= 0:
        return
    agent.gleam = max(0.0, (agent.gleam or 0.0) - tax)


class WorldLoop:
    def __init__(self, policies: dict[str, ScriptedAgentPolicy] | None = None,
                 tick_duration_sec: float = 1.0):
        self.gm = GameMaster()
        self.policies = policies or {}
        self.tick_duration_sec = tick_duration_sec
        self.stopped = False

    async def run(self, max_ticks: int | None = None):
        n = 0
        while not self.stopped:
            await self.run_one_tick()
            n += 1
            if max_ticks is not None and n >= max_ticks:
                log.info("WorldLoop stopped at tick %d (max reached)", n)
                return
            await asyncio.sleep(self.tick_duration_sec)

    async def run_one_tick(self):
        with get_session() as s:
            ws = s.get(WorldState, 1)
            ws.tick_actual = (ws.tick_actual or 0) + 1
            tick = ws.tick_actual
            s.add(ws)

            # Mundo no-cognitivo: arboles dan fruta, etc.
            grow_fruit_trees(s, tick)

            agents = s.query(Agent).filter(Agent.alive == True).all()  # noqa: E712

            ctx = self.gm.build_context(s, tick=tick)
            sink_cfg = (ctx.world_state.sink or {}) if ctx.world_state else {}

            for agent in agents:
                decay_needs(agent)
                apply_economy_sink(agent, sink_cfg)
                transit_msg = advance_transit(agent, ctx.locations_by_id)
                if transit_msg:
                    log.info("tick=%d agent=%s %s", tick, agent.id, transit_msg)
                s.add(agent)

            # Rebuild context (agents may have arrived this tick)
            ctx = self.gm.build_context(s, tick=tick)

            for agent in agents:
                if agent.in_transit:
                    continue  # cannot act while traveling
                if agent.sleeping_until_tick and tick < agent.sleeping_until_tick:
                    continue  # still sleeping
                policy = self.policies.get(agent.id)
                if policy is None:
                    continue
                trigger = classify_trigger(agent, s, tick)
                # Apply emotional updates based on observations (heuristica determinista)
                observations = (
                    trigger.context_extra.get("events", [])
                    if trigger.kind == "observation" else []
                )
                update_agent_emotions(agent, observations, tick)
                s.add(agent)

                if (not getattr(policy, "ignore_triggers", False)) and trigger.kind == "skip":
                    log.debug("tick=%d agent=%s SKIP (%s)", tick, agent.id, trigger.reason)
                    continue
                # LLM policies need ctx to build prompts
                if hasattr(policy, "_ctx_ref"):
                    policy._ctx_ref = ctx
                action = policy.next_action(trigger=trigger)
                if action is None:
                    continue
                result = self.gm.validate_and_apply(agent, action, ctx)
                log.info("tick=%d agent=%s trigger=%s action=%s result=%s",
                         tick, agent.id, trigger.kind, action.type, type(result).__name__)

            s.commit()
