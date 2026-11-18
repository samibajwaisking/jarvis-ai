"""The built-in tutorial. Shown by `jarvis guide`, the `help` command and the web UI."""

GUIDE = """\
JARVIS AI - QUICK START GUIDE
=============================

Jarvis is your free personal AI assistant. You can talk to it in three ways:

  1. Terminal chat   ->  jarvis chat
  2. Voice mode      ->  jarvis voice
  3. Web interface   ->  jarvis serve   (then open http://127.0.0.1:8000)

ASK ANYTHING
  Just type a normal question: "Explain recursion simply", "Write an email to my client",
  "Translate this to Urdu". Jarvis remembers your recent conversation.

BUILT-IN COMMANDS (work instantly, no AI needed)
  time / date                 Show the current time and date
  calc 12 * (3 + 4) / 2       Safe calculator
  note: buy milk              Save a note
  notes                       List your notes
  delete note 2               Delete note number 2
  search python decorators    Quick web answer (DuckDuckGo)
  system info                 Show OS and Python details
  about                       Who made Jarvis and how to contact the creator
  help                        Show this guide

CHAT COMMANDS (terminal)
  /clear      Forget the current conversation
  /guide      Show this guide
  /provider   Show which AI engine is active
  /exit       Quit

CHOOSING YOUR AI ENGINE (all configured in the .env file)
  Free local:  JARVIS_PROVIDER=ollama      (no key, no cost, runs on your computer)
  Cloud:       JARVIS_PROVIDER=anthropic | openai | gemini  (bring your own API key)

VOICE MODE
  Install the extras once:  pip install "jarvis-ai[voice]"
  Run:  jarvis voice   - say "Jarvis, what time is it?" and say "goodbye" to stop.

TROUBLESHOOTING
  Run `jarvis doctor` - it checks your setup and tells you exactly what to fix.

Full documentation lives in the docs/ folder of the repository.
Made with care by Sami Bajwa (Samioutic).
"""
