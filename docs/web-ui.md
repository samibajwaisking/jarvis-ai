# Web Interface and API

## Start

```bash
pip install -e ".[web]"
jarvis serve
```

Open <http://127.0.0.1:8000>. Use `--host` and `--port` to change the address.

The page has a chat window, a **Guide** button (shows the tutorial) and a **Clear** button.

## Security

By default Jarvis only listens on your own computer. If you make it reachable from other devices:

1. Set `JARVIS_API_TOKEN` to a long random value.
2. Put it behind HTTPS (for example with Caddy or Nginx).
3. Never expose it without a token, because anyone could spend your API credits.

The web page asks for the token when the server requires one and stores it only for that browser tab.

## REST API

Interactive docs are available at <http://127.0.0.1:8000/docs>.

| Method | Path | Description |
|---|---|---|
| GET | `/api/health` | Status, version, provider |
| POST | `/api/chat` | Send a message |
| POST | `/api/clear?session=web` | Clear a conversation |
| GET | `/api/guide` | Tutorial text |
| GET | `/api/about` | Creator info |

### Example

```bash
curl -X POST http://127.0.0.1:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "X-Jarvis-Token: your-token" \
  -d '{"message": "calc 2 + 2", "session": "demo"}'
```

Response:

```json
{"reply": "2 + 2 = 4"}
```

Each `session` value keeps its own conversation history.
