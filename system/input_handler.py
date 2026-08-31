class InputHandler:
    def __init__(self, pygame):
        self.pygame = pygame

    def command_from_event(self, event):
        if event.type != self.pygame.KEYDOWN:
            return None
        return {self.pygame.K_d: "dance", self.pygame.K_b: "box", self.pygame.K_r: "run",
                self.pygame.K_m: "magic", self.pygame.K_s: "sleep", self.pygame.K_h: "hey hamster",
                self.pygame.K_RETURN: "open sesame"}.get(event.key)
