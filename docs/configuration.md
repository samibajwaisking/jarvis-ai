# Configuration

Jarvis reads settings from environment variables. The easiest way is the `.env` file in the folder where you run `jarvis`. Copy `.env.example` to `.env` to start.

| Variable | Default | Description |
|---|---|---|
| `JARVIS_PROVIDER` | auto | `ollama`, `anthropic`, `openai` or `gemini`. If unset, Jarvis picks the first API key it finds, otherwise Ollama. |
| `JARVIS_MODEL` | provider default | Model name. Defaults: `llama3.1` (Ollama), `claude-sonnet-5-5` (Anthropic), `gpt-4o-mini` (OpenAI), `gemini-2.0-flash` (Gemini). Model names change over time, so check your provider's documentation. |
| `ANTHROPIC_API_KEY` | empty | Key for Anthropic Claude |
| `OPENAI_API_KEY` | empty | Key for OpenAI |
| `GEMINI_API_KEY` | empty | Key for Google Gemini |
| `OLLAMA_HOST` | `http://localhost:11434` | Where Ollama is running |
| `JARVIS_MAX_TOKENS` | `1024` | Maximum reply length |
| `JARVIS_TEMPERATURE` | `0.7` | Creativity: `0` is precise, `1` is creative |
| `JARVIS_HISTORY_LIMIT` | `20` | Number of recent messages sent to the AI |
| `JARVIS_TIMEOUT` | `60` | Seconds to wait for the AI |
| `JARVIS_SYSTEM_PROMPT` | built-in | Change Jarvis's personality and rules |
| `JARVIS_HOME` | `~/.jarvis` | Folder for the database |
| `JARVIS_HOST` | `127.0.0.1` | Web server address |
| `JARVIS_PORT` | `8000` | Web server port |
| `JARVIS_API_TOKEN` | empty | If set, the web API requires this token |
| `JARVIS_VOICE_LANGUAGE` | `en-US` | Speech recognition language, for example `ur-PK` or `en-GB` |

## Custom personality example

```env
JARVIS_SYSTEM_PROMPT=You are Jarvis, a patient teacher. Explain step by step with simple examples.
```

## Where is my data?

Conversations and notes live in `~/.jarvis/jarvis.db` (SQLite). Delete that file to erase everything.
