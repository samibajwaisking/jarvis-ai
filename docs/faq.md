# FAQ

**Is Jarvis really free?**
Yes. The code is MIT licensed. With Ollama there are no costs at all. With cloud engines you pay the provider directly for your own usage. A $1 donation is optional.

**Do I need to code to use it?**
No. Install, edit `.env`, run `jarvis chat`.

**Does it work offline?**
Yes with Ollama. Search and voice recognition need internet.

**Where are my conversations stored?**
In `~/.jarvis/jarvis.db` on your computer. Nothing is sent anywhere except to the AI provider you chose.

**Which engine should I pick?**
Beginners: Ollama (free). Best quality with little setup: a cloud provider with your own key.

**Can I change Jarvis's personality?**
Yes, set `JARVIS_SYSTEM_PROMPT` in `.env`.

**Can I use it in Urdu or Hindi?**
Chat in any language your AI model supports. For voice, set `JARVIS_VOICE_LANGUAGE=ur-PK` or `hi-IN`.

**Can I add my own commands?**
Yes. See [plugins.md](plugins.md).

**Can I use it commercially?**
Yes. The MIT license allows commercial use. Keep the license notice.

**How do I update?**
`git pull` then `pip install -e ".[web]"`.

**How do I contact the creator?**
Run `jarvis about` or see the README.
