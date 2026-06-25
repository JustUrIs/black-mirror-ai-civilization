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

    def validate_and_apply(self, action: Action, ctx: WorldContext) -> Result:
        agent = ctx.agents_by_id.get(action.agent_id)
        if agent is None:
            return self._record(ctx, action, Reject(f"agente '{action.agent_id}' no existe o no esta vivo."))

        handler = self.handlers.get(action.type)
        if handler is None:
            return self._record(ctx, action, Reject(f"accion '{action.type}' no implementada (handlers: {list(self.handlers.keys())})."))

        ok, err = handler.check_prereqs(agent, action.params, ctx)
        if not ok:
            return self._record(ctx, action, Reject(err))

        try:
            summary = handler.apply(agent, action.params, ctx)
        except Exception as e:
            log.exception("apply failed: %s", e)
            return self._record(ctx, action, Reject(f"declaraste '{action.type}' pero la aplicacion fallo: {e}"))

        return self._record(ctx, action, Accept(summary))

    def _record(self, ctx: WorldContext, action: Action, result: Result) -> Result:
        ctx.session.add(ActionLog(
            tick=ctx.tick,
            agent_id=action.agent_id,
            action_type=action.type,
            params=action.params,
            status="accept" if isinstance(result, Accept) else "reject",
            error_nl=result.error_nl if isinstance(result, Reject) else "",
            side_effect_summary=result.side_effect_summary if isinstance(result, Accept) else "",
            timestamp=datetime.utcnow(),
        ))
        return result
