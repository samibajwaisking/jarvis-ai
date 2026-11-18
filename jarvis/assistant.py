"""The Jarvis core: skills first, AI model second."""

from __future__ import annotations

from .brain import Brain, ProviderError
from .config import Settings
from .memory import Memory
from .skills import Skill, default_skills


class Jarvis:
    def __init__(self, settings: Settings | None = None, skills: list[Skill] | None = None):
        self.settings = settings or Settings.load()
        self.memory = Memory(self.settings.home / "jarvis.db")
        self.brain = Brain(self.settings)
        self.skills: list[Skill] = skills if skills is not None else default_skills()

    def register_skill(self, skill: Skill, first: bool = True) -> None:
        """Add a custom skill. By default it is checked before the built-in ones."""
        if first:
            self.skills.insert(0, skill)
        else:
            self.skills.append(skill)

    def ask(self, text: str, session: str = "default") -> str:
        """Return Jarvis's reply to `text`."""
        text = (text or "").strip()
        if not text:
            return "Say something and I will help."

        for skill in self.skills:
            if skill.match(text):
                return skill.run(text, self)

        self.memory.add(session, "user", text)
        history = self.memory.history(session, self.settings.history_limit)
        try:
            reply = self.brain.chat(history)
        except ProviderError as exc:
            return f"Sorry, my AI engine had a problem: {exc}\nRun `jarvis doctor` to check your setup."
        self.memory.add(session, "assistant", reply)
        return reply

    def clear(self, session: str = "default") -> None:
        self.memory.clear(session)
