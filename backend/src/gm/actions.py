"""Action definitions: dataclass + base Handler protocol.

PLAN_v4.md §5: 18 action types MVP. Day 1 implements 3 (MOVE, TALK, EAT).
Days 2-4 add the remaining 15.
"""
from dataclasses import dataclass, field
from typing import Any, Protocol, Tuple

from ..db.schema import Agent, Location


@dataclass
class Action:
    type: str
    params: dict = field(default_factory=dict)


@dataclass
class Accept:
    side_effect_summary: str


@dataclass
class Reject:
    error_nl: str


Result = Accept | Reject


class Handler(Protocol):
    """Action handler protocol.

    check_prereqs: pure function (Python), no side effects. Returns (ok, error_nl).
    apply: executes side-effects (DB writes, state changes). Raises if it fails.
    """

    def check_prereqs(self, agent: Agent, params: dict, world_ctx: "WorldContext") -> Tuple[bool, str]: ...

    def apply(self, agent: Agent, params: dict, world_ctx: "WorldContext") -> str: ...


@dataclass
class WorldContext:
    """Snapshot view passed to handlers. Includes session for DB writes."""
    session: Any
    tick: int
    locations_by_id: dict[str, Location]
    agents_by_id: dict[str, Agent]
    world_state: Any
