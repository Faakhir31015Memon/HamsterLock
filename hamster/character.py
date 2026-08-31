import math
import random

from config import COLORS, IDLE_SLEEP_SECONDS
from .states import HamsterState


class Hamster:
    def __init__(self):
        self.state = HamsterState.IDLE
        self.previous_state = self.state
        self.state_time = 0.0
        self.since_activity = 0.0
        self.attempts = 0
        self._rng = random.Random(7)
        self._blink_at = 2.5
        self._blink_time = 0.0

    def set_state(self, state: HamsterState):
        self.previous_state = self.state
        self.state = state
        self.state_time = 0.0
        self.since_activity = 0.0

    def wrong_attempt(self):
        self.attempts = min(self.attempts + 1, 5)
        self.set_state(HamsterState.ANGRY if self.attempts >= 3 else HamsterState.BOXING)

    def correct_attempt(self):
        self.set_state(HamsterState.HAPPY)

    def update(self, dt: float):
        self.state_time += dt
        self.since_activity += dt
        self._blink_time += dt
        if self._blink_time > self._blink_at:
            self._blink_time = 0.0
            self._blink_at = self._rng.uniform(1.8, 4.5)
        if self.state == HamsterState.IDLE and self.since_activity >= IDLE_SLEEP_SECONDS:
            self.set_state(HamsterState.SLEEP)
        if self.state in (HamsterState.BOXING, HamsterState.ANGRY, HamsterState.HAPPY,
                          HamsterState.DANCE, HamsterState.WHEEL, HamsterState.MAGIC,
                          HamsterState.ATTENTION):
            durations = {HamsterState.BOXING: 2.1, HamsterState.ANGRY: 2.8, HamsterState.HAPPY: 3.0,
                         HamsterState.DANCE: 4.0, HamsterState.WHEEL: 4.0, HamsterState.MAGIC: 4.0,
                         HamsterState.ATTENTION: 1.7}
            if self.state_time >= durations[self.state]:
                self.set_state(HamsterState.IDLE)

    @property
    def eyes_closed(self):
        return self._blink_time < 0.14

    def pose(self) -> dict:
        t = self.state_time
        bob = math.sin(t * 3.2) * 5
        tilt = 0.0
        arm = 0.0
        accent = COLORS["pink"]
        if self.state == HamsterState.SLEEP:
            bob, tilt = 6, -0.08
        elif self.state in (HamsterState.BOXING, HamsterState.ANGRY):
            bob = math.sin(t * 14) * 3
            arm = math.sin(t * 12) * 22
            accent = COLORS["red"]
        elif self.state == HamsterState.HAPPY:
            bob = abs(math.sin(t * 8)) * -28
            accent = COLORS["gold"]
        elif self.state == HamsterState.DANCE:
            bob, tilt = math.sin(t * 9) * 12, math.sin(t * 6) * 0.2
            accent = COLORS["cyan"]
        elif self.state == HamsterState.WHEEL:
            bob = math.sin(t * 13) * 4
            accent = COLORS["green"]
        elif self.state == HamsterState.MAGIC:
            bob, accent = math.sin(t * 5) * 8, COLORS["gold"]
        elif self.state == HamsterState.LISTENING:
            tilt, accent = math.sin(t * 3) * 0.05, COLORS["cyan"]
        return {"bob": bob, "tilt": tilt, "arm": arm, "accent": accent}
