# Hamster Lock Screen

A fullscreen Pygame desktop gate with a procedural cartoon hamster, offline voice adapters, and Windows kiosk support. It is inspired by the playful computer scene in *Sivaji: The Boss* without bundling copyrighted film assets.

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

For real voice input, download and extract the Vosk English model into `models/vosk-model-small-en-us-0.15/`. Without Vosk, PyAudio, or the model, keyboard demo controls still work:

- `Enter`: open sesame / unlock demo
- `D`, `B`, `R`, `M`, `H`, `S`: dance, box, run, magic, attention, sleep
- `Space`: listening state
- `Esc`: exit the demo

The supported unlock phrase is configured in `config.py`. Programmatic Windows unlocking is intentionally not attempted because Windows does not expose a supported API for bypassing the secure desktop; this app acts as a kiosk-style overlay and should be treated as a visual lock screen, not a security boundary.

## Layout

- `hamster/`: state machine and character pose data
- `voice/`: Vosk/PyAudio and pyttsx3 adapters
- `ui/`: rendering, status elements, and celebration particles
- `system/`: fullscreen/topmost behavior and Windows boundary notes
