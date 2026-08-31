import json
import queue
import threading
from pathlib import Path


class VoiceRecognizer:
    def __init__(self, model_path: Path, callback):
        self.model_path = model_path
        self.callback = callback
        self.running = False
        self.available = False
        self._thread = None

    def start(self):
        try:
            import pyaudio
            from vosk import KaldiRecognizer, Model
        except ImportError:
            return False
        if not self.model_path.exists():
            return False
        self.running = True
        self.available = True

        def listen():
            audio = pyaudio.PyAudio()
            stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000,
                                input=True, frames_per_buffer=8000)
            recognizer = KaldiRecognizer(Model(str(self.model_path)), 16000)
            while self.running:
                data = stream.read(4000, exception_on_overflow=False)
                if recognizer.AcceptWaveform(data):
                    text = json.loads(recognizer.Result()).get("text", "").strip()
                    if text:
                        self.callback(text)
            stream.stop_stream(); stream.close(); audio.terminate()

        self._thread = threading.Thread(target=listen, daemon=True)
        self._thread.start()
        return True

    def stop(self):
        self.running = False
