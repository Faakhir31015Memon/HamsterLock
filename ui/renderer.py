import math

from config import COLORS
from hamster.states import HamsterState
from .elements import lock_icon, rounded_label
from .particles import ParticleSystem


class Renderer:
    def __init__(self, pygame, surface):
        self.pg, self.surface = pygame, surface
        self.w, self.h = surface.get_size()
        self.title = pygame.font.SysFont("trebuchetms", 48, bold=True)
        self.heading = pygame.font.SysFont("trebuchetms", 24, bold=True)
        self.body = pygame.font.SysFont("trebuchetms", 18)
        self.small = pygame.font.SysFont("trebuchetms", 14)
        self.particles = ParticleSystem()

    def background(self):
        for y in range(self.h):
            ratio = y / max(1, self.h - 1)
            color = tuple(int(COLORS["ink"][i] * (1 - ratio) + (29, 22, 66)[i] * ratio) for i in range(3))
            self.pg.draw.line(self.surface, color, (0, y), (self.w, y))
        for x, y, r in ((self.w * .15, self.h * .25, 180), (self.w * .82, self.h * .78, 240)):
            glow = self.pg.Surface((r * 2, r * 2), self.pg.SRCALPHA)
            self.pg.draw.circle(glow, (*COLORS["cyan"], 16), (r, r), r)
            self.surface.blit(glow, (x - r, y - r))

    def draw_hamster(self, hamster, center):
        pg = self.pg; x, y = center; pose = hamster.pose(); y += pose["bob"]
        body = (196, 137, 106); dark = (113, 69, 65); belly = (245, 203, 164)
        pg.draw.ellipse((x - 104, y - 112, 56, 56), dark); pg.draw.ellipse((x + 48, y - 112, 56, 56), dark)
        pg.draw.ellipse((x - 96, y - 104, 40, 40), (235, 157, 125)); pg.draw.ellipse((x + 56, y - 104, 40, 40), (235, 157, 125))
        pg.draw.ellipse((x - 120, y - 95, 240, 190), body)
        pg.draw.ellipse((x - 76, y - 28, 152, 110), belly)
        pg.draw.circle(self.surface, COLORS["cream"], (x - 44, y - 38), 14); pg.draw.circle(self.surface, COLORS["cream"], (x + 44, y - 38), 14)
        if hamster.eyes_closed:
            pg.draw.line(self.surface, dark, (x - 51, y - 38), (x - 37, y - 38), 4); pg.draw.line(self.surface, dark, (x + 37, y - 38), (x + 51, y - 38), 4)
        else:
            pg.draw.circle(self.surface, dark, (x - 44, y - 36), 6); pg.draw.circle(self.surface, dark, (x + 44, y - 36), 6)
        pg.draw.circle(self.surface, COLORS["pink"], (x, y - 5), 13); pg.draw.arc(self.surface, dark, (x - 22, y + 1, x + 22, y + 27), 0, math.pi, 3)
        arm = pose["arm"]
        if hamster.state in (HamsterState.BOXING, HamsterState.ANGRY):
            pg.draw.line(self.surface, body, (x - 78, y + 18), (x - 126, y - arm), 18); pg.draw.circle(self.surface, pose["accent"], (x - 132, int(y - arm)), 16)
            pg.draw.line(self.surface, body, (x + 78, y + 18), (x + 126, y + arm), 18); pg.draw.circle(self.surface, pose["accent"], (x + 132, int(y + arm)), 16)
        else:
            pg.draw.line(self.surface, body, (x - 76, y + 20), (x - 120, y + 62), 18); pg.draw.line(self.surface, body, (x + 76, y + 20), (x + 120, y + 62), 18)
        if hamster.state == HamsterState.SLEEP:
            self._text("Z z z", (x + 100, y - 130), self.heading, COLORS["cyan"])
        elif hamster.state == HamsterState.MAGIC:
            pg.draw.line(self.surface, COLORS["gold"], (x + 100, y - 25), (x + 165, y - 90), 5); pg.draw.circle(self.surface, COLORS["gold"], (x + 175, y - 100), 9)

    def _text(self, text, pos, font, color, center=True):
        image = font.render(text, True, color); rect = image.get_rect(center=pos) if center else image.get_rect(topleft=pos); self.surface.blit(image, rect)

    def draw(self, hamster, recognized, listening, unlocked):
        pg = self.pg; self.background(); accent = COLORS["green"] if unlocked else (COLORS["cyan"] if listening else COLORS["red"])
        lock_icon(self.surface, pg, (42, 44), not unlocked, accent)
        self._text("HAMSTER LOCK", (82, 39), self.heading, COLORS["cream"], False)
        self._text("SECURE DESKTOP GATEWAY", (82, 66), self.small, COLORS["muted"], False)
        self._text("WELCOME BACK, BOSS" if unlocked else "YOUR DESKTOP IS PROTECTED", (self.w // 2, 105), self.title, COLORS["cream"])
        state_name = hamster.state.name.title()
        rounded_label(self.surface, pg, self.body, state_name.upper(), (self.w // 2, 160), COLORS["ink"], hamster.pose()["accent"])
        self.draw_hamster(hamster, (self.w // 2, self.h // 2 + 35))
        status = "UNLOCKED" if unlocked else ("LISTENING..." if listening else "LOCKED")
        self._text(status, (self.w // 2, self.h - 126), self.heading, accent)
        self._text(f"FAILED ATTEMPTS  {hamster.attempts} / 5", (self.w // 2, self.h - 88), self.body, COLORS["muted"])
        self._text(f'HEARD: "{recognized or "waiting for a voice command"}"', (self.w // 2, self.h - 47), self.body, COLORS["cream"])
        self._text("ENTER unlocks demo  |  D dance  B box  R run  M magic  H hello  S sleep  |  ESC quit", (self.w // 2, self.h - 17), self.small, COLORS["muted"])
        self.particles.draw(self.surface, pg, [COLORS["gold"], COLORS["pink"], COLORS["cyan"], COLORS["green"]])
