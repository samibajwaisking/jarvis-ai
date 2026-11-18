import pytest

from jarvis.assistant import Jarvis
from jarvis.config import Settings
from jarvis.skills import safe_eval


@pytest.fixture()
def jarvis(tmp_path, monkeypatch):
    monkeypatch.setenv("JARVIS_HOME", str(tmp_path))
    monkeypatch.setenv("JARVIS_PROVIDER", "ollama")
    return Jarvis(Settings.load())


def test_calculator():
    assert safe_eval("2 + 3 * 4") == 14
    assert safe_eval("(10 - 4) / 3") == 2
    assert safe_eval("2 ** 5") == 32


def test_calculator_rejects_unsafe_input():
    with pytest.raises(ValueError):
        safe_eval("__import__('os').system('echo hi')")
    with pytest.raises(ValueError):
        safe_eval("2 ** 1000")


def test_calc_skill(jarvis):
    assert jarvis.ask("calc 6 * 7") == "6 * 7 = 42"
    assert "divide by zero" in jarvis.ask("calc 1 / 0")


def test_notes_roundtrip(jarvis):
    assert "Saved as note 1" in jarvis.ask("note: buy milk")
    assert "buy milk" in jarvis.ask("notes")
    assert "deleted" in jarvis.ask("delete note 1")
    assert "no notes" in jarvis.ask("notes").lower()


def test_help_and_about(jarvis):
    assert "QUICK START" in jarvis.ask("help")
    assert "Sami Bajwa" in jarvis.ask("about")


def test_time(jarvis):
    assert "It is" in jarvis.ask("what time is it?")


def test_missing_key_is_reported(tmp_path, monkeypatch):
    monkeypatch.setenv("JARVIS_HOME", str(tmp_path))
    monkeypatch.setenv("JARVIS_PROVIDER", "openai")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    j = Jarvis(Settings.load())
    assert "OPENAI_API_KEY is missing" in j.ask("hello there")


def test_custom_skill(jarvis):
    from jarvis.skills import Skill

    class Ping(Skill):
        def match(self, text):
            return text == "ping"

        def run(self, text, j):
            return "pong"

    jarvis.register_skill(Ping())
    assert jarvis.ask("ping") == "pong"


def test_web_api(tmp_path, monkeypatch):
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient

    monkeypatch.setenv("JARVIS_HOME", str(tmp_path))
    monkeypatch.setenv("JARVIS_PROVIDER", "ollama")
    monkeypatch.setenv("JARVIS_API_TOKEN", "secret")
    from jarvis import server

    server._jarvis = None
    client = TestClient(server.app)
    assert client.get("/api/health").json()["status"] == "ok"
    assert client.post("/api/chat", json={"message": "calc 1+1"}).status_code == 401
    ok = client.post("/api/chat", json={"message": "calc 1+1"}, headers={"X-Jarvis-Token": "secret"})
    assert ok.json()["reply"] == "1+1 = 2"
    assert client.get("/").status_code == 200
    server._jarvis = None
