<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,18,24&height=200&section=header&text=JARVIS%20AI&fontSize=70&fontColor=ffffff&animation=fadeIn&desc=Your%20free%20personal%20AI%20assistant&descAlignY=68&descSize=20" alt="Jarvis AI banner" width="100%"/>

### Chat in your terminal. Talk with your voice. Use it in your browser. 100% free.

[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![CI](https://img.shields.io/github/actions/workflow/status/samibajwaisking/jarvis-ai/ci.yml?style=for-the-badge&logo=githubactions&logoColor=white&label=CI)](https://github.com/samibajwaisking/jarvis-ai/actions)
[![Stars](https://img.shields.io/github/stars/samibajwaisking/jarvis-ai?style=for-the-badge&logo=github&color=f59e0b)](https://github.com/samibajwaisking/jarvis-ai/stargazers)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-ec4899?style=for-the-badge)](CONTRIBUTING.md)

![Ollama](https://img.shields.io/badge/Ollama-free%20%26%20local-0ea5e9?style=flat-square)
![Claude](https://img.shields.io/badge/Claude-supported-d97706?style=flat-square)
![OpenAI](https://img.shields.io/badge/OpenAI-supported-10a37f?style=flat-square)
![Gemini](https://img.shields.io/badge/Gemini-supported-8b5cf6?style=flat-square)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=flat-square&logo=docker&logoColor=white)

**[Quick Start](#-quick-start-5-minutes)** &nbsp;•&nbsp;
**[Features](#-features)** &nbsp;•&nbsp;
**[Docs](#-documentation)** &nbsp;•&nbsp;
**[Support](#-support-the-project)** &nbsp;•&nbsp;
**[Creator](#-about-the-creator)**

</div>

---

## ✨ Why Jarvis?

| | |
|---|---|
| 🆓 **Free forever** | MIT licensed. Run it with free local models (Ollama) or bring your own API key. |
| 🎙️ **Three ways to use it** | Terminal chat, hands-free voice mode and a clean web interface. |
| 🔒 **Private by design** | Conversations and notes are stored in a local SQLite file on your own machine. |
| 🎓 **Beginner friendly** | Built-in tutorial (`jarvis guide`), a setup checker (`jarvis doctor`) and step-by-step docs. |
| 🧩 **Easy to extend** | Add your own commands in about ten lines of Python. |
| 🪶 **Lightweight** | Core needs only two dependencies: `httpx` and `python-dotenv`. |

## 🚀 Features

| Feature | How to use it |
|---|---|
| 💬 AI chat with memory | `jarvis chat` |
| ⚡ One-shot questions | `jarvis ask "Explain APIs simply"` |
| 🎤 Voice assistant | `jarvis voice` |
| 🌐 Web interface and JSON API | `jarvis serve` |
| 🧮 Safe calculator (no `eval`) | `calc 12 * (3 + 4)` |
| 📝 Notes | `note: buy milk` · `notes` · `delete note 1` |
| 🔎 Quick web answers | `search what is python` |
| 🕒 Time and date | `what time is it` |
| 💻 System info | `system info` |
| 📖 Built-in tutorial | `help` or `jarvis guide` |
| 🩺 Setup checker | `jarvis doctor` |
| 🤖 Four AI engines | Ollama (free) · Claude · OpenAI · Gemini |

## ⚡ Quick Start (5 minutes)

You need **Python 3.10 or newer**. Check with `python --version`.

```bash
# 1. Get the code
git clone https://github.com/samibajwaisking/jarvis-ai.git
cd jarvis-ai

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 3. Install Jarvis (with the web interface)
pip install -e ".[web]"

# 4. Create your settings file
cp .env.example .env               # Windows: copy .env.example .env

# 5. Check everything, then start chatting
jarvis doctor
jarvis chat
```

### 🧠 Pick your AI engine (edit `.env`)

<details open>
<summary><b>Option A: 100% free and offline (recommended for beginners)</b></summary>

1. Install [Ollama](https://ollama.com).
2. Run `ollama pull llama3.1`.
3. Keep `JARVIS_PROVIDER=ollama` in `.env`.

</details>

<details>
<summary><b>Option B: Cloud engine with your own API key</b></summary>

```env
JARVIS_PROVIDER=anthropic        # or openai, or gemini
ANTHROPIC_API_KEY=your-key-here
```

Full details: [docs/providers.md](docs/providers.md)

</details>

## 🎮 The three modes

```bash
jarvis chat      # terminal chat (default)
jarvis voice     # voice assistant (needs: pip install -e ".[voice]")
jarvis serve     # web UI at http://127.0.0.1:8000
```

## 🎓 How to use Jarvis

Type `help` inside Jarvis at any time, or run `jarvis guide`.

```text
You: calc 25 * 4 + 10
Jarvis: 25 * 4 + 10 = 110

You: note: send invoice to client
Jarvis: Saved as note 1.

You: Explain machine learning like I am 12
Jarvis: (your chosen AI engine answers)
```

Read the full walkthrough in [docs/getting-started.md](docs/getting-started.md).

## 📚 Documentation

| Guide | What it covers |
|---|---|
| 🚀 [Getting started](docs/getting-started.md) | Install, first run, every command |
| ⚙️ [Configuration](docs/configuration.md) | All `.env` settings |
| 🤖 [AI providers](docs/providers.md) | Ollama, Claude, OpenAI, Gemini |
| 🎤 [Voice mode](docs/voice.md) | Microphone and speech setup |
| 🌐 [Web UI and API](docs/web-ui.md) | Web interface, REST API, security token |
| 🧩 [Writing skills](docs/plugins.md) | Add your own commands |
| 🏗️ [Architecture](docs/architecture.md) | How Jarvis works inside |
| 🐳 [Deployment](docs/deployment.md) | Run it on a server or with Docker |
| 🛠️ [Troubleshooting](docs/troubleshooting.md) | Fix common problems |
| ❓ [FAQ](docs/faq.md) | Quick answers |
| 🗺️ [Roadmap](docs/roadmap.md) | What is coming next |

## 🗂️ Project structure

```text
jarvis-ai/
├── jarvis/
│   ├── assistant.py     # core: skills first, AI second
│   ├── brain.py         # Ollama / Claude / OpenAI / Gemini clients
│   ├── cli.py           # `jarvis` command
│   ├── config.py        # settings from .env
│   ├── memory.py        # local SQLite history and notes
│   ├── server.py        # FastAPI web server
│   ├── voice.py         # voice mode
│   ├── guide.py         # built-in tutorial text
│   ├── about.py         # creator info
│   ├── skills/          # built-in commands
│   └── web/index.html   # web interface
├── tests/
├── docs/
├── .github/             # CI, issue and PR templates
├── Dockerfile
├── pyproject.toml
├── .env.example
└── LICENSE
```

## 💛 Support the project

Jarvis is and will stay **free**. If it helps you:

1. ⭐ **Star this repository.** It costs nothing and helps others find it.
2. 📣 Share it with friends and classmates.
3. ☕ Optional: a **$1 one-time donation** helps keep the project growing. Use the **Sponsor** button on this repository or visit [samioutic.com](https://samioutic.com).

[![Star this repo](https://img.shields.io/badge/⭐_Star_Jarvis_AI-f59e0b?style=for-the-badge)](https://github.com/samibajwaisking/jarvis-ai)

## 🤝 Contributing

Pull requests are welcome! Read [CONTRIBUTING.md](CONTRIBUTING.md) first and follow the [Code of Conduct](CODE_OF_CONDUCT.md). Report security problems privately as described in [SECURITY.md](SECURITY.md).

## 👨‍💻 About the creator

<div align="center">

### Sami Bajwa · Samioutic

**Full-Stack Developer · Technical Consultant · AI Educator · Content Creator**
📍 Lahore, Pakistan &nbsp;|&nbsp; Teaching AI and web development in English and Roman Urdu

[![Website](https://img.shields.io/badge/Website-samioutic.com-0ea5e9?style=for-the-badge&logo=googlechrome&logoColor=white)](https://samioutic.com)
[![Email](https://img.shields.io/badge/Email-samibajwa491@gmail.com-ea4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:samibajwa491@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-samibajwaisking-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/samibajwaisking)

[![Facebook](https://img.shields.io/badge/Facebook-samibajwaisking-1877F2?style=for-the-badge&logo=facebook&logoColor=white)](https://www.facebook.com/samibajwaisking)
[![Instagram](https://img.shields.io/badge/Instagram-samibajwaisking-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/samibajwaisking)
[![Threads](https://img.shields.io/badge/Threads-samibajwaisking-000000?style=for-the-badge&logo=threads&logoColor=white)](https://www.threads.net/@samibajwaisking)
[![TikTok](https://img.shields.io/badge/TikTok-samibajwaisking-000000?style=for-the-badge&logo=tiktok&logoColor=white)](https://www.tiktok.com/@samibajwaisking)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-samibajwa106-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/samibajwa106)

</div>

## 📄 License

Released under the [MIT License](LICENSE). Copyright © 2026 Sami Bajwa (Samioutic).

<div align="center">

**Made with ❤️ in Lahore by [Sami Bajwa](https://github.com/samibajwaisking)**

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,18,24&height=100&section=footer" alt="footer" width="100%"/>

</div>
