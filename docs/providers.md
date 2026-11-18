# AI Providers

Jarvis works with four engines. You only need one.

## Ollama (free, local, private)

Runs on your own computer. No account, no key, no cost.

1. Install from <https://ollama.com>.
2. Download a model: `ollama pull llama3.1` (small machines can try `ollama pull llama3.2:3b`).
3. `.env`:
   ```env
   JARVIS_PROVIDER=ollama
   JARVIS_MODEL=llama3.1
   ```
4. Run `jarvis doctor`. It checks that Ollama is running and the model is installed.

Tip: 8 GB RAM is enough for small models. Bigger models need more memory.

## Anthropic Claude

1. Create a key in the [Anthropic Console](https://console.anthropic.com).
2. `.env`:
   ```env
   JARVIS_PROVIDER=anthropic
   ANTHROPIC_API_KEY=your-key
   ```
3. Change `JARVIS_MODEL` if you want a different Claude model.

## OpenAI

1. Create a key at <https://platform.openai.com/api-keys>.
2. `.env`:
   ```env
   JARVIS_PROVIDER=openai
   OPENAI_API_KEY=your-key
   JARVIS_MODEL=gpt-4o-mini
   ```

## Google Gemini

1. Create a key in [Google AI Studio](https://aistudio.google.com/apikey).
2. `.env`:
   ```env
   JARVIS_PROVIDER=gemini
   GEMINI_API_KEY=your-key
   JARVIS_MODEL=gemini-2.0-flash
   ```

## Costs

Jarvis itself is free. Cloud providers charge for usage on their side, according to their own pricing. Ollama has no usage cost.

## Adding another provider

Open `jarvis/brain.py`, write a function `(settings, system, messages) -> str`, and add it to the `_PROVIDERS` dictionary. Add the name to `PROVIDERS` and a default model in `jarvis/config.py`.
