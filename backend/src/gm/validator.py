"""GameMaster validator: deterministic prereq check + side-effect apply.

Single source of truth for whether an action happened.
Crónica/diary code MUST read ActionLog (status='accept') only.
"""
import logging
from datetime import datetime

from ..db.schema import Agent, Location, WorldState, ActionLog
from .actions import Action, Accept, Reject, Result, WorldContext
from .handlers import default_handlers


log = logging.getLogger("gm")


class GameMaster:
    def __init__(self, handlers: dict | None = None):
        self.handlers = handlers or default_handlers()

    def build_context(self, session, tick: int) -> WorldContext:
        locs = {l.id: l for l in session.query(Location).all()}
        agents = {a.id: a for a in session.query(Agent).filter(Agent.alive == True).all()}  # noqa: E712
        ws = session.get(WorldState, 1)
        return WorldContext(
            session=session,
            tick=tick,
            locations_by_id=locs,
            agents_by_id=agents,
            world_state=ws,
        )

    def validate_and_apply(self, agent: Agent, action: Action, ctx: WorldContext) -> Result:
        if not agent.alive:
            return self._record(ctx, agent.id, action, Reject(f"agente '{agent.id}' no esta vivo."))

        handler = self.handlers.get(action.type)
        if handler is None:
            return self._record(ctx, agent.id, action, Reject(f"accion '{action.type}' no implementada (handlers: {list(self.handlers.keys())})."))

        ok, err = handler.check_prereqs(agent, action.params, ctx)
        if not ok:
            return self._record(ctx, agent.id, action, Reject(err))

        try:
            summary = handler.apply(agent, action.params, ctx)
        except Exception as e:
            log.exception("apply failed: %s", e)
            return self._record(ctx, agent.id, action, Reject(f"declaraste '{action.type}' pero la aplicacion fallo: {e}"))

        return self._record(ctx, agent.id, action, Accept(summary))

    def _record(self, ctx: WorldContext, agent_id: str, action: Action, result: Result) -> Result:
        ctx.session.add(ActionLog(
            tick=ctx.tick,
            agent_id=agent_id,
            action_type=action.type,
            params=action.params,
            status="accept" if isinstance(result, Accept) else "reject",
            error_nl=result.error_nl if isinstance(result, Reject) else "",
            side_effect_summary=result.side_effect_summary if isinstance(result, Accept) else "",
            timestamp=datetime.utcnow(),
        ))
        return result
