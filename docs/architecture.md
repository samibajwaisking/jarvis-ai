# Architecture

```text
 you ──► CLI / Voice / Web ──► Jarvis.ask()
                                  │
                     ┌────────────┴────────────┐
                     ▼                         ▼
              Skills (instant)          Memory (SQLite)
              first match wins          recent history
                     │                         │
                     └─ no match ──► Brain ◄───┘
                                       │
                         Ollama │ Claude │ OpenAI │ Gemini
```

## Modules

| Module | Role |
|---|---|
| `config.py` | Reads `.env`, validates settings |
| `assistant.py` | `Jarvis.ask()`: tries skills, then the AI |
| `brain.py` | One small HTTP client per provider (`httpx`) |
| `memory.py` | SQLite tables `messages` and `notes` |
| `skills/` | Local commands (calculator, notes, search...) |
| `cli.py` | `jarvis` command and sub-commands |
| `voice.py` | Microphone in, speaker out |
| `server.py` | FastAPI app and token check |
| `web/index.html` | Single-file web interface, no build step |

## Design choices

- **Few dependencies.** Core needs only `httpx` and `python-dotenv`.
- **Local first.** Data stays on the user's machine.
- **Skills before AI.** Fast, free and predictable for common tasks.
- **No `eval`.** The calculator parses an AST and allows only arithmetic.
