# Contributing to Jarvis AI

Thank you for helping make Jarvis better! Everyone is welcome, including first-time contributors.

## Ways to help

- Report bugs and suggest features through [Issues](https://github.com/samibajwaisking/jarvis-ai/issues).
- Improve the documentation or fix typos.
- Add a new skill (see [docs/plugins.md](docs/plugins.md)).
- Add a new AI provider in `jarvis/brain.py`.
- Translate the guide into your language.

## Development setup

```bash
git clone https://github.com/samibajwaisking/jarvis-ai.git
cd jarvis-ai
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
ruff check .
```

## Pull request checklist

1. Create a branch: `git checkout -b feature/my-change`.
2. Keep changes focused. One feature or fix per pull request.
3. Add or update tests in `tests/`.
4. Run `pytest` and `ruff check .`. Both must pass.
5. Update the docs and `CHANGELOG.md` if behaviour changes.
6. Open the pull request and fill in the template.

## Code style

- Python 3.10+, type hints where helpful, line length 110.
- Keep the core dependency list small: `httpx` and `python-dotenv` only.
- Never add code that sends user data anywhere except the AI provider the user chose.
- Never use `eval` or `exec` on user input.

## Commit messages

Use short, clear messages in the present tense, for example: `Add Gemini provider` or `Fix note deletion`.

## Code of Conduct

By participating you agree to follow our [Code of Conduct](CODE_OF_CONDUCT.md).
