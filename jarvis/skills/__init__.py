"""Built-in skills: instant commands that run locally without calling an AI model.

To add your own skill, see docs/plugins.md.
"""

from __future__ import annotations

import ast
import operator
import platform
import re
import sys
from datetime import datetime
from typing import TYPE_CHECKING

import httpx

from ..about import about_text
from ..guide import GUIDE

if TYPE_CHECKING:  # pragma: no cover
    from ..assistant import Jarvis


class Skill:
    """Base class for all skills."""

    name: str = "skill"
    description: str = ""

    def match(self, text: str) -> bool:
        raise NotImplementedError

    def run(self, text: str, jarvis: Jarvis) -> str:
        raise NotImplementedError


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower()).rstrip("?.! ")


class HelpSkill(Skill):
    name = "help"
    description = "Show the user guide"
    _words = {"help", "guide", "tutorial", "what can you do", "how to use you", "how do i use you", "how to use jarvis"}

    def match(self, text: str) -> bool:
        return _clean(text) in self._words

    def run(self, text: str, jarvis: Jarvis) -> str:
        return GUIDE


class AboutSkill(Skill):
    name = "about"
    description = "Creator information"
    _words = {"about", "who made you", "who created you", "who built you", "who is your creator", "creator"}

    def match(self, text: str) -> bool:
        return _clean(text) in self._words

    def run(self, text: str, jarvis: Jarvis) -> str:
        return about_text()


class TimeSkill(Skill):
    name = "time"
    description = "Current time and date"
    _pattern = re.compile(
        r"^(what('?s| is)? )?(the )?(current )?(time|date|day|time and date|date and time)( is it| today| now)?( right now)?$|^(time|date)$"
    )

    def match(self, text: str) -> bool:
        return bool(self._pattern.match(_clean(text)))

    def run(self, text: str, jarvis: Jarvis) -> str:
        now = datetime.now().astimezone()
        return now.strftime("It is %I:%M %p on %A, %d %B %Y (%Z).")


_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def safe_eval(expression: str) -> float:
    """Evaluate a basic arithmetic expression without using eval()."""

    def walk(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return walk(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
            left, right = walk(node.left), walk(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 100:
                raise ValueError("Exponent too large.")
            return _OPS[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
            return _OPS[type(node.op)](walk(node.operand))
        raise ValueError("Only numbers and + - * / // % ** ( ) are allowed.")

    if len(expression) > 200:
        raise ValueError("Expression too long.")
    return walk(ast.parse(expression, mode="eval"))


class CalcSkill(Skill):
    name = "calc"
    description = "Safe calculator"
    _pattern = re.compile(r"^(calc|calculate|math)\s+(.+)$", re.IGNORECASE)

    def match(self, text: str) -> bool:
        return bool(self._pattern.match(text.strip()))

    def run(self, text: str, jarvis: Jarvis) -> str:
        expr = self._pattern.match(text.strip()).group(2).replace("^", "**").replace("x", "*")
        try:
            result = safe_eval(expr)
        except ZeroDivisionError:
            return "Cannot divide by zero."
        except (ValueError, SyntaxError) as exc:
            return f"Could not calculate that: {exc}"
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        return f"{expr.strip()} = {result}"


class NotesSkill(Skill):
    name = "notes"
    description = "Save, list and delete notes"
    _add = re.compile(r"^(add note|note)\s*[:\-]?\s*(.+)$", re.IGNORECASE)
    _delete = re.compile(r"^delete note\s+(\d+)$", re.IGNORECASE)
    _list = {"notes", "list notes", "show notes", "my notes"}

    def match(self, text: str) -> bool:
        t = text.strip()
        return bool(self._add.match(t) or self._delete.match(t) or _clean(t) in self._list)

    def run(self, text: str, jarvis: Jarvis) -> str:
        t = text.strip()
        m = self._delete.match(t)
        if m:
            ok = jarvis.memory.delete_note(int(m.group(1)))
            return "Note deleted." if ok else "No note with that number."
        if _clean(t) in self._list:
            notes = jarvis.memory.list_notes()
            if not notes:
                return "You have no notes yet. Try: note: buy milk"
            return "\n".join(f"{nid}. {body}  ({created[:16]})" for nid, body, created in notes)
        body = self._add.match(t).group(2).strip()
        nid = jarvis.memory.add_note(body)
        return f"Saved as note {nid}."


class SearchSkill(Skill):
    name = "search"
    description = "Quick web answer via DuckDuckGo"
    _pattern = re.compile(r"^(search|google|look up|lookup)\s+(.+)$", re.IGNORECASE)

    def match(self, text: str) -> bool:
        return bool(self._pattern.match(text.strip()))

    def run(self, text: str, jarvis: Jarvis) -> str:
        query = self._pattern.match(text.strip()).group(2).strip()
        try:
            r = httpx.get(
                "https://api.duckduckgo.com/",
                params={"q": query, "format": "json", "no_html": 1, "skip_disambig": 1},
                timeout=10,
                follow_redirects=True,
            )
            r.raise_for_status()
            data = r.json()
        except (httpx.HTTPError, ValueError):
            return f"I could not reach the search service. Try: https://duckduckgo.com/?q={query.replace(' ', '+')}"
        answer = data.get("AbstractText") or data.get("Answer")
        if not answer:
            for topic in data.get("RelatedTopics", []):
                if isinstance(topic, dict) and topic.get("Text"):
                    answer = topic["Text"]
                    break
        link = data.get("AbstractURL") or f"https://duckduckgo.com/?q={query.replace(' ', '+')}"
        if answer:
            return f"{answer}\nSource: {link}"
        return f"No instant answer found. Full results: {link}"


class SystemSkill(Skill):
    name = "system"
    description = "System information"

    def match(self, text: str) -> bool:
        return _clean(text) in {"system info", "system information", "sysinfo"}

    def run(self, text: str, jarvis: Jarvis) -> str:
        s = jarvis.settings
        return (
            f"OS: {platform.system()} {platform.release()}\n"
            f"Python: {sys.version.split()[0]}\n"
            f"AI provider: {s.provider} ({s.model})\n"
            f"Data folder: {s.home}"
        )


def default_skills() -> list[Skill]:
    """Skills are checked in order; the first match wins."""
    return [
        HelpSkill(),
        AboutSkill(),
        TimeSkill(),
        CalcSkill(),
        NotesSkill(),
        SearchSkill(),
        SystemSkill(),
    ]
