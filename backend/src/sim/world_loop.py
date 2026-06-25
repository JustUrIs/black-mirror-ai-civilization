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
    """Day 1 only: returns the next action from a hardcoded queue."""
    agent_id: str
    queue: list[Action] = field(default_factory=list)

    def next_action(self) -> Action | None:
        if not self.queue:
            return None
        return self.queue.pop(0)


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

            agents = s.query(Agent).filter(Agent.alive == True).all()  # noqa: E712

            for agent in agents:
                decay_needs(agent)
                s.add(agent)

            ctx = self.gm.build_context(s, tick=tick)

            for agent in agents:
                policy = self.policies.get(agent.id)
                if policy is None:
                    continue
                action = policy.next_action()
                if action is None:
                    continue
                result = self.gm.validate_and_apply(agent, action, ctx)
                log.info("tick=%d agent=%s action=%s result=%s",
                         tick, agent.id, action.type, type(result).__name__)

            s.commit()
