import math
import random


class ParticleSystem:
    def __init__(self):
        self.items = []
        self.rng = random.Random(12)

    def burst(self, x, y, count=30):
        for _ in range(count):
            angle = self.rng.random() * math.tau
            speed = self.rng.uniform(70, 260)
            self.items.append([x, y, math.cos(angle) * speed, math.sin(angle) * speed, self.rng.uniform(.7, 1.4)])

    def update(self, dt):
        for item in self.items:
            item[0] += item[2] * dt; item[1] += item[3] * dt; item[3] += 180 * dt; item[4] -= dt
        self.items = [item for item in self.items if item[4] > 0]

    def draw(self, surface, pygame, colors):
        for index, (x, y, _, _, life) in enumerate(self.items):
            color = colors[index % len(colors)]
            pygame.draw.circle(surface, color, (int(x), int(y)), max(2, int(life * 5)))
