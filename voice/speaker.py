import threading


class Speaker:
    def __init__(self):
        self.available = False
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.available = True
        except Exception:
            self.engine = None

    def say(self, text: str):
        if not self.available:
            return
        threading.Thread(target=self._speak, args=(text,), daemon=True).start()

    def _speak(self, text: str):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception:
            pass
