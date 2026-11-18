"""Optional voice mode. Install extras with: pip install "jarvis-ai[voice]"."""

from __future__ import annotations

import re

from .assistant import Jarvis

EXIT_WORDS = {"goodbye", "good bye", "exit", "quit", "stop listening", "bye jarvis"}


def run_voice(jarvis: Jarvis) -> None:
    try:
        import pyttsx3
        import speech_recognition as sr
    except ImportError as exc:
        raise SystemExit(
            "Voice mode needs extra packages. Run:\n"
            '  pip install "jarvis-ai[voice]"\n'
            "On Linux you may also need: sudo apt install portaudio19-dev espeak\n"
            f"({exc})"
        )

    engine = pyttsx3.init()
    recognizer = sr.Recognizer()

    def speak(text: str) -> None:
        print(f"Jarvis: {text}")
        engine.say(text)
        engine.runAndWait()

    speak("Jarvis online. How can I help?")
    with sr.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic, duration=1)
        while True:
            print("Listening...")
            try:
                audio = recognizer.listen(mic, timeout=10, phrase_time_limit=15)
                heard = recognizer.recognize_google(audio, language=jarvis.settings.voice_language)
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except sr.RequestError as exc:
                speak(f"The speech service is unavailable: {exc}")
                return

            print(f"You: {heard}")
            cleaned = re.sub(r"^(hey |ok |okay )?jarvis[, ]*", "", heard.strip(), flags=re.IGNORECASE)
            if cleaned.lower().strip() in EXIT_WORDS:
                speak("Goodbye!")
                return
            speak(jarvis.ask(cleaned or heard, session="voice"))
