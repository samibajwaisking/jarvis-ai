# Getting Started

This guide takes you from zero to a working Jarvis. No prior experience needed.

## 1. What you need

- A computer with **Windows, macOS or Linux**
- **Python 3.10 or newer** ([download](https://www.python.org/downloads/)). Check with `python --version`.
- **Git** ([download](https://git-scm.com/downloads))
- One AI engine: free local Ollama, or an API key from Anthropic, OpenAI or Google

## 2. Install

```bash
git clone https://github.com/samibajwaisking/jarvis-ai.git
cd jarvis-ai
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[web]"
cp .env.example .env             # Windows: copy .env.example .env
```

## 3. Choose your AI engine

Open `.env` in any text editor.

**Free and offline:** install [Ollama](https://ollama.com), then run `ollama pull llama3.1`. Leave `JARVIS_PROVIDER=ollama`.

**Cloud:** set `JARVIS_PROVIDER` to `anthropic`, `openai` or `gemini` and paste the matching key. See [providers.md](providers.md).

## 4. Check your setup

```bash
jarvis doctor
```

Every line should say `[ OK ]`. If you see `[FAIL]`, the message tells you what to fix.

## 5. Start Jarvis

```bash
jarvis chat
```

Try these:

```text
You: help
You: what time is it
You: calc 0.15 * 200
You: note: finish my project
You: notes
You: search python programming language
You: Explain how the internet works in simple words
```

## 6. All commands

### Terminal commands

| Command | What it does |
|---|---|
| `jarvis chat` | Interactive chat (also runs when you type just `jarvis`) |
| `jarvis ask "question"` | Ask one question and exit |
| `jarvis voice` | Voice assistant |
| `jarvis serve` | Web interface on port 8000 |
| `jarvis doctor` | Check your setup |
| `jarvis guide` | Print the user guide |
| `jarvis about` | Creator information |
| `jarvis --version` | Show the version |

### Commands inside chat

| You type | Result |
|---|---|
| `/clear` | Forget the current conversation |
| `/guide` | Show the guide |
| `/provider` | Show the active AI engine |
| `/exit` | Quit |

### Instant skills (no AI call, work offline except search)

| You type | Result |
|---|---|
| `time` or `what time is it` | Current time and date |
| `calc 2 * (3 + 4)` | Calculator. Supports `+ - * / // % ** ( )` |
| `note: text` | Save a note |
| `notes` | List notes |
| `delete note 3` | Delete note 3 |
| `search topic` | Quick DuckDuckGo answer |
| `system info` | OS, Python and engine details |
| `about` | About the creator |
| `help` | Show the guide |

Anything else is sent to your AI engine, with your recent conversation as context.

## 7. Next steps

- Try the web interface: `jarvis serve`, then open <http://127.0.0.1:8000>.
- Set up [voice mode](voice.md).
- Write your own command: [plugins.md](plugins.md).
