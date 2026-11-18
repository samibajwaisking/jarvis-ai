# Voice Mode

Talk to Jarvis hands-free.

## Install

```bash
pip install -e ".[voice]"
```

### Extra system packages

- **Windows:** usually works as is. If PyAudio fails, run `pip install pipwin` then `pipwin install pyaudio`.
- **macOS:** `brew install portaudio`
- **Linux (Debian/Ubuntu):** `sudo apt install portaudio19-dev espeak python3-dev`

## Run

```bash
jarvis voice
```

Wait for "Listening...", then speak. Examples:

- "Jarvis, what time is it?"
- "Calculate 25 times 4" (Jarvis hears text, so say "calc 25 times 4" or ask the AI directly)
- "Explain gravity in one sentence"
- "Goodbye" to stop

## Language

Set `JARVIS_VOICE_LANGUAGE` in `.env`: `en-US`, `en-GB`, `ur-PK`, `hi-IN` and so on.

## Notes

- Speech-to-text uses Google's free web speech service through the `SpeechRecognition` library, so it needs internet. Your audio is sent to that service.
- Text-to-speech (`pyttsx3`) runs offline using your system's voices.
- If nothing is heard, check your microphone permission and default input device.
