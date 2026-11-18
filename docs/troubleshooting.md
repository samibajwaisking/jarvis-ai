# Troubleshooting

Start with `jarvis doctor`. It checks Python, your provider, keys and optional packages.

| Problem | Fix |
|---|---|
| `jarvis: command not found` | Activate your virtual environment, or run `python -m jarvis`. |
| `API_KEY is missing` | Add the key to `.env` and make sure you run `jarvis` from the folder that contains `.env`. |
| `Cannot reach Ollama` | Install Ollama and run `ollama serve`. Check `OLLAMA_HOST`. |
| `Model 'x' is not installed` | Run `ollama pull x`. |
| `401` or `403` from a provider | The API key is wrong, expired or has no credit. |
| `429` from a provider | Rate limit reached. Wait and retry. |
| Replies are slow | Use a smaller local model or a faster cloud model. Lower `JARVIS_MAX_TOKENS`. |
| `Web mode needs extra packages` | `pip install -e ".[web]"` |
| `Voice mode needs extra packages` | `pip install -e ".[voice]"` and see [voice.md](voice.md). |
| PyAudio fails to install | Install PortAudio first (see [voice.md](voice.md)). |
| Search says "could not reach" | Check your internet connection. |
| Port 8000 already in use | `jarvis serve --port 8001` |
| Want to erase all data | Delete `~/.jarvis/jarvis.db`. |

Still stuck? Open an [issue](https://github.com/samibajwaisking/jarvis-ai/issues) and include your `jarvis doctor` output (remove API keys).
