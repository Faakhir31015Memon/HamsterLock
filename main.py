import sys
from pathlib import Path

import config
from hamster import Hamster
from hamster.states import HamsterState
from system.input_handler import InputHandler
from system.window_manager import WindowManager
from ui.renderer import Renderer
from voice.recognizer import VoiceRecognizer
from voice.speaker import Speaker

try:
    import pygame
except ImportError:
    print("Pygame is required. Install dependencies with: python -m pip install -r requirements.txt")
    raise SystemExit(1)


class HamsterLockApp:
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        size = (info.current_w or config.SCREEN_WIDTH, info.current_h or config.SCREEN_HEIGHT)
        self.window = WindowManager(pygame)
        self.surface = self.window.create(size)
        pygame.display.set_caption(config.APP_TITLE)
        self.renderer = Renderer(pygame, self.surface)
        self.input = InputHandler(pygame)
        self.hamster = Hamster()
        self.speaker = Speaker()
        self.recognized = ""
        self.listening = False
        self.unlocked = False
        self.running = True
        self.recognizer = VoiceRecognizer(config.MODEL_DIR, self.handle_command)
        self.voice_available = self.recognizer.start()
        self.window.keep_on_top()

    def handle_command(self, text):
        text = text.lower().strip()
        self.recognized = text
        self.listening = False
        if config.UNLOCK_PHRASE in text:
            self.unlocked = True
            self.hamster.correct_attempt()
            self.renderer.particles.burst(self.surface.get_width() // 2, self.surface.get_height() // 2)
            self.speaker.say("Welcome back, boss! Unlocked!")
        elif text in ("dance", "box", "run", "magic", "sleep", "hey hamster"):
            states = {"dance": HamsterState.DANCE, "box": HamsterState.BOXING, "run": HamsterState.WHEEL,
                      "magic": HamsterState.MAGIC, "sleep": HamsterState.SLEEP, "hey hamster": HamsterState.ATTENTION}
            self.hamster.set_state(states[text])
            self.speaker.say({"dance": "Dancing time!", "box": "Let's box!", "run": "Running!", "magic": "Abracadabra!", "sleep": "Good night!", "hey hamster": "Hmm?"}[text])
        elif text:
            self.hamster.wrong_attempt()
            self.speaker.say("You shall not pass!" if self.hamster.attempts >= 3 else "Access denied! Try again!")

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            dt = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False
                command = self.input.command_from_event(event)
                if command:
                    self.listening = False
                    self.handle_command(command)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.listening = True
                    self.hamster.set_state(HamsterState.LISTENING)
                    self.speaker.say("Hmm?")
            self.hamster.update(dt)
            self.renderer.particles.update(dt)
            self.renderer.draw(self.hamster, self.recognized, self.listening, self.unlocked)
            pygame.display.flip()
        self.recognizer.stop()
        pygame.quit()
        return 0


if __name__ == "__main__":
    sys.exit(HamsterLockApp().run())
