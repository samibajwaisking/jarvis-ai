"""Configuration loaded from environment variables (and an optional .env file)."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

try:  # python-dotenv is optional but recommended
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # pragma: no cover
    pass

PROVIDERS = ("anthropic", "openai", "gemini", "ollama")

DEFAULT_MODELS = {
    "anthropic": "claude-sonnet-5-5",
    "openai": "gpt-4o-mini",
    "gemini": "gemini-2.0-flash",
    "ollama": "llama3.1",
}

DEFAULT_SYSTEM_PROMPT = (
    "You are Jarvis, a friendly, fast and capable personal AI assistant created by Sami Bajwa "
    "(Samioutic). Answer clearly and concisely. When the user asks how to use you, explain your "
    "features: chat, voice mode, notes, calculator, web search, date and time, system info, and "
    "the 'guide' command. Reply in the language the user writes in. Be honest when you are unsure."
)


def _home() -> Path:
    path = Path(os.getenv("JARVIS_HOME", str(Path.home() / ".jarvis"))).expanduser()
    path.mkdir(parents=True, exist_ok=True)
    return path


def _detect_provider() -> str:
    explicit = os.getenv("JARVIS_PROVIDER", "").strip().lower()
    if explicit:
        return explicit
    if os.getenv("ANTHROPIC_API_KEY"):
        return "anthropic"
    if os.getenv("OPENAI_API_KEY"):
        return "openai"
    if os.getenv("GEMINI_API_KEY"):
        return "gemini"
    return "ollama"  # free local default


@dataclass
class Settings:
    provider: str
    model: str
    system_prompt: str
    home: Path
    anthropic_api_key: str
    openai_api_key: str
    gemini_api_key: str
    ollama_host: str
    max_tokens: int
    temperature: float
    history_limit: int
    timeout: float
    api_token: str
    host: str
    port: int
    voice_language: str

    @classmethod
    def load(cls) -> Settings:
        provider = _detect_provider()
        model = os.getenv("JARVIS_MODEL", "").strip() or DEFAULT_MODELS.get(provider, "")
        return cls(
            provider=provider,
            model=model,
            system_prompt=os.getenv("JARVIS_SYSTEM_PROMPT", DEFAULT_SYSTEM_PROMPT),
            home=_home(),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
            ollama_host=os.getenv("OLLAMA_HOST", "http://localhost:11434").rstrip("/"),
            max_tokens=int(os.getenv("JARVIS_MAX_TOKENS", "1024")),
            temperature=float(os.getenv("JARVIS_TEMPERATURE", "0.7")),
            history_limit=int(os.getenv("JARVIS_HISTORY_LIMIT", "20")),
            timeout=float(os.getenv("JARVIS_TIMEOUT", "60")),
            api_token=os.getenv("JARVIS_API_TOKEN", ""),
            host=os.getenv("JARVIS_HOST", "127.0.0.1"),
            port=int(os.getenv("JARVIS_PORT", "8000")),
            voice_language=os.getenv("JARVIS_VOICE_LANGUAGE", "en-US"),
        )

    def validate(self) -> list[str]:
        """Return a list of human-readable problems (empty if everything looks fine)."""
        problems: list[str] = []
        if self.provider not in PROVIDERS:
            problems.append(f"Unknown JARVIS_PROVIDER '{self.provider}'. Use one of: {', '.join(PROVIDERS)}.")
            return problems
        keys = {
            "anthropic": self.anthropic_api_key,
            "openai": self.openai_api_key,
            "gemini": self.gemini_api_key,
        }
        if self.provider in keys and not keys[self.provider]:
            problems.append(f"{self.provider.upper()}_API_KEY is missing. Add it to your .env file.")
        return problems
