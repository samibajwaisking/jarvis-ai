# Security Policy

## Supported versions

| Version | Supported |
|---|---|
| 1.x | Yes |

## Reporting a vulnerability

Please do **not** open a public issue for security problems.

Email **samibajwa491@gmail.com** with the subject `Jarvis security report`. Include:

- A description of the problem and its impact
- Steps to reproduce
- Your Jarvis version and operating system

You will get a reply within 7 days. Fixes are released as soon as possible and you will be credited if you wish.

## Keeping your own install safe

- Never commit your `.env` file. It is listed in `.gitignore`.
- If you expose `jarvis serve` beyond your own computer, **always set `JARVIS_API_TOKEN`** and put it behind HTTPS.
- By default the server only listens on `127.0.0.1` (your own machine).
- Rotate any API key immediately if you think it leaked.
- Your conversations are stored locally in `~/.jarvis/jarvis.db`. Protect that folder like any other personal data.
