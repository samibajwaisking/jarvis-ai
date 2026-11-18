# Deployment

## Docker

```bash
docker build -t jarvis-ai .
docker run -d --name jarvis -p 8000:8000 \
  -e JARVIS_PROVIDER=anthropic \
  -e ANTHROPIC_API_KEY=your-key \
  -e JARVIS_API_TOKEN=a-long-random-token \
  -v jarvis-data:/data \
  jarvis-ai
```

Open <http://localhost:8000>. The container listens on `0.0.0.0`, so **always set `JARVIS_API_TOKEN`**.

To use Ollama running on your host machine, add `-e OLLAMA_HOST=http://host.docker.internal:11434`.

## Linux server (systemd)

```ini
# /etc/systemd/system/jarvis.service
[Unit]
Description=Jarvis AI
After=network.target

[Service]
User=jarvis
WorkingDirectory=/opt/jarvis-ai
EnvironmentFile=/opt/jarvis-ai/.env
ExecStart=/opt/jarvis-ai/.venv/bin/jarvis serve --host 127.0.0.1 --port 8000
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Put Nginx or Caddy in front for HTTPS and forward traffic to `127.0.0.1:8000`.

## Checklist before going public

- [ ] `JARVIS_API_TOKEN` is set
- [ ] HTTPS is enabled
- [ ] `.env` is not in version control
- [ ] You understand that your API key pays for every request
