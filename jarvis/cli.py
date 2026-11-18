"""Command line interface: `jarvis chat | ask | voice | serve | doctor | guide | about`."""

from __future__ import annotations

import argparse
import sys

import httpx

from . import __version__
from .about import TAGLINE, about_text
from .assistant import Jarvis
from .config import Settings
from .guide import GUIDE

BANNER = r"""
     _   _    ______     _____ ____
    | | / \  |  _ \ \   / /_ _/ ___|
 _  | |/ _ \ | |_) \ \ / / | |\___ \
| |_| / ___ \|  _ < \ V /  | | ___) |
 \___/_/   \_\_| \_\ \_/  |___|____/
"""


def cmd_chat(args: argparse.Namespace) -> int:
    jarvis = Jarvis()
    print(BANNER)
    print(f"v{__version__} - {TAGLINE}")
    print(f"Engine: {jarvis.settings.provider} ({jarvis.settings.model}). Type /guide for help, /exit to quit.\n")
    while True:
        try:
            text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return 0
        if not text:
            continue
        if text in {"/exit", "/quit", "exit", "quit"}:
            print("Goodbye!")
            return 0
        if text == "/clear":
            jarvis.clear()
            print("Jarvis: Conversation cleared.\n")
            continue
        if text == "/guide":
            print(GUIDE)
            continue
        if text == "/provider":
            print(f"Jarvis: {jarvis.settings.provider} ({jarvis.settings.model})\n")
            continue
        print(f"Jarvis: {jarvis.ask(text)}\n")


def cmd_ask(args: argparse.Namespace) -> int:
    print(Jarvis().ask(" ".join(args.question)))
    return 0


def cmd_voice(args: argparse.Namespace) -> int:
    from .voice import run_voice

    run_voice(Jarvis())
    return 0


def cmd_serve(args: argparse.Namespace) -> int:
    try:
        import uvicorn
    except ImportError:
        print("Web mode needs extra packages. Run: pip install \"jarvis-ai[web]\"")
        return 1
    settings = Settings.load()
    host = args.host or settings.host
    port = args.port or settings.port
    print(f"Jarvis web UI: http://{host}:{port}")
    uvicorn.run("jarvis.server:app", host=host, port=port)
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    s = Settings.load()
    ok = True
    print(f"Jarvis {__version__} doctor\n")
    print(f"Python:    {sys.version.split()[0]}")
    print(f"Provider:  {s.provider}")
    print(f"Model:     {s.model}")
    print(f"Data dir:  {s.home}")

    problems = s.validate()
    for p in problems:
        print(f"[FAIL] {p}")
        ok = False

    if s.provider == "ollama":
        try:
            r = httpx.get(f"{s.ollama_host}/api/tags", timeout=5)
            r.raise_for_status()
            names = [m["name"] for m in r.json().get("models", [])]
            print(f"[ OK ] Ollama is running. Installed models: {', '.join(names) or 'none'}")
            if not any(n.split(":")[0] == s.model.split(":")[0] for n in names):
                print(f"[FAIL] Model '{s.model}' is not installed. Run: ollama pull {s.model}")
                ok = False
        except httpx.HTTPError:
            print(f"[FAIL] Cannot reach Ollama at {s.ollama_host}. Install it from https://ollama.com and run `ollama serve`.")
            ok = False
    elif not problems:
        print("[ OK ] API key found.")

    for module, label in (("fastapi", "web UI"), ("speech_recognition", "voice input"), ("pyttsx3", "voice output")):
        try:
            __import__(module)
            print(f"[ OK ] {label} dependencies installed")
        except ImportError:
            print(f"[ -- ] {label} dependencies not installed (optional)")

    print("\nAll good!" if ok else "\nFix the items marked [FAIL] and run `jarvis doctor` again.")
    return 0 if ok else 1


def cmd_guide(args: argparse.Namespace) -> int:
    print(GUIDE)
    return 0


def cmd_about(args: argparse.Namespace) -> int:
    print(about_text())
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="jarvis", description="Jarvis AI - your free personal AI assistant.")
    parser.add_argument("--version", action="version", version=f"jarvis-ai {__version__}")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("chat", help="Interactive terminal chat (default)").set_defaults(func=cmd_chat)
    ask = sub.add_parser("ask", help="Ask one question and exit")
    ask.add_argument("question", nargs="+")
    ask.set_defaults(func=cmd_ask)
    sub.add_parser("voice", help="Voice assistant mode").set_defaults(func=cmd_voice)
    serve = sub.add_parser("serve", help="Start the web interface")
    serve.add_argument("--host")
    serve.add_argument("--port", type=int)
    serve.set_defaults(func=cmd_serve)
    sub.add_parser("doctor", help="Check your setup").set_defaults(func=cmd_doctor)
    sub.add_parser("guide", help="Show the user guide").set_defaults(func=cmd_guide)
    sub.add_parser("about", help="About the creator").set_defaults(func=cmd_about)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        args.func = cmd_chat
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
