"""LLM providers. Every provider is a thin HTTP client so there are no heavy SDKs to install."""

from __future__ import annotations

from collections.abc import Callable

import httpx

from .config import Settings

Message = dict  # {"role": "user" | "assistant", "content": str}


class ProviderError(RuntimeError):
    """Raised when an LLM provider call fails."""


def _post(url: str, payload: dict, headers: dict | None, timeout: float) -> dict:
    try:
        response = httpx.post(url, json=payload, headers=headers or {}, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as exc:
        raise ProviderError(f"Provider returned {exc.response.status_code}: {exc.response.text[:300]}") from exc
    except httpx.HTTPError as exc:
        raise ProviderError(f"Could not reach the provider: {exc}") from exc


def _anthropic(s: Settings, system: str, messages: list[Message]) -> str:
    data = _post(
        "https://api.anthropic.com/v1/messages",
        {
            "model": s.model,
            "max_tokens": s.max_tokens,
            "temperature": s.temperature,
            "system": system,
            "messages": messages,
        },
        {
            "x-api-key": s.anthropic_api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        s.timeout,
    )
    return "".join(block.get("text", "") for block in data.get("content", [])).strip()


def _openai(s: Settings, system: str, messages: list[Message]) -> str:
    data = _post(
        "https://api.openai.com/v1/chat/completions",
        {
            "model": s.model,
            "max_tokens": s.max_tokens,
            "temperature": s.temperature,
            "messages": [{"role": "system", "content": system}, *messages],
        },
        {"Authorization": f"Bearer {s.openai_api_key}"},
        s.timeout,
    )
    return data["choices"][0]["message"]["content"].strip()


def _gemini(s: Settings, system: str, messages: list[Message]) -> str:
    contents = [
        {"role": "user" if m["role"] == "user" else "model", "parts": [{"text": m["content"]}]}
        for m in messages
    ]
    data = _post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{s.model}:generateContent",
        {
            "system_instruction": {"parts": [{"text": system}]},
            "contents": contents,
            "generationConfig": {"maxOutputTokens": s.max_tokens, "temperature": s.temperature},
        },
        {"x-goog-api-key": s.gemini_api_key},
        s.timeout,
    )
    parts = data["candidates"][0]["content"]["parts"]
    return "".join(p.get("text", "") for p in parts).strip()


def _ollama(s: Settings, system: str, messages: list[Message]) -> str:
    data = _post(
        f"{s.ollama_host}/api/chat",
        {
            "model": s.model,
            "stream": False,
            "options": {"temperature": s.temperature, "num_predict": s.max_tokens},
            "messages": [{"role": "system", "content": system}, *messages],
        },
        None,
        s.timeout,
    )
    return data["message"]["content"].strip()


_PROVIDERS: dict[str, Callable[[Settings, str, list[Message]], str]] = {
    "anthropic": _anthropic,
    "openai": _openai,
    "gemini": _gemini,
    "ollama": _ollama,
}


class Brain:
    """Routes a conversation to whichever provider is configured."""

    def __init__(self, settings: Settings):
        self.settings = settings

    def chat(self, messages: list[Message], system: str | None = None) -> str:
        problems = self.settings.validate()
        if problems:
            raise ProviderError(" ".join(problems))
        fn = _PROVIDERS[self.settings.provider]
        try:
            return fn(self.settings, system or self.settings.system_prompt, messages)
        except (KeyError, IndexError) as exc:
            raise ProviderError(f"Unexpected response format from {self.settings.provider}.") from exc
