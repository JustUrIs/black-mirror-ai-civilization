"""Derive 'when' from a tick.

Day/night cycle: tick % dia_noche_cycle_ticks -> 4 buckets (each cycle/4 ticks):
  - amanecer    : 0   .. C/4
  - mediodia    : C/4 .. C/2
  - atardecer   : C/2 .. 3C/4
  - noche       : 3C/4.. C

Moon phase: tick % luna_cycle_ticks -> 4 buckets:
  - luna_nueva, luna_creciente, luna_llena, luna_menguante.
"""
from dataclasses import dataclass


@dataclass
class WorldTime:
    tick: int
    dia_cycle: int
    luna_cycle: int

    @property
    def time_of_day(self) -> str:
        phase = self.tick % self.dia_cycle
        q = self.dia_cycle / 4
        if phase < q: return "amanecer"
        if phase < 2 * q: return "mediodia"
        if phase < 3 * q: return "atardecer"
        return "noche"

    @property
    def is_night(self) -> bool:
        return self.time_of_day == "noche"

    @property
    def luna_phase(self) -> str:
        phase = self.tick % self.luna_cycle
        q = self.luna_cycle / 4
        if phase < q: return "luna_nueva"
        if phase < 2 * q: return "luna_creciente"
        if phase < 3 * q: return "luna_llena"
        return "luna_menguante"

    @property
    def dia_num(self) -> int:
        """Calendar day number from tick 0."""
        return self.tick // self.dia_cycle

    def describe(self) -> str:
        return f"dia {self.dia_num}, {self.time_of_day} ({self.luna_phase})"


def from_world_state(world_state) -> WorldTime:
    return WorldTime(
        tick=int(world_state.tick_actual or 0),
        dia_cycle=int(world_state.dia_noche_cycle_ticks or 2880),
        luna_cycle=int(world_state.luna_cycle_ticks or 80640),
    )
