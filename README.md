# Streamlit + LangChain (Groq) Chatbot

A minimal chatbot that streams responses from Groq models using LangChain, with a Streamlit UI and a Procfile ready for one‑click deploy on Heroku.

## Features

- Streamed AI responses via `langchain-groq`
- Simple, modern Streamlit chat interface
- Easy model and system prompt customization
- Ready for Heroku deployment (Procfile included)

## Project structure

- `Agent.py` — Defines the Groq LLM client and the `respond_stream` generator. Customize `SYSTEM_PROMPT` and model.
- `Front.py` — Streamlit UI (chat history, layout, styling).
- `Procfile` — Process definition for Heroku (runs Streamlit on the platform port).
- `requirements.txt` — Python dependencies.
- `README.md` — This documentation.

## Prerequisites

- Python 3.9+ (3.10/3.11 recommended)
- Groq API Key: create one at https://console.groq.com/keys
- Heroku account (GitHub Student Pack can include credits)

## Quick start (Windows PowerShell)

```powershell
# 1) Create and activate a virtual environment
py -m venv env
env/Scripts/activate
# 2) Install dependencies
py -m pip install --upgrade pip
py -m pip install -r requirements.txt

# 3) Create a .env file in the project root
# .env
# GROQ_API_KEY=your_key_here

# 4) Run locally (for testing)
streamlit run Front.py
```

If Streamlit opens in a browser tab, you’re all set. If it doesn’t auto‑open, copy the shown local URL into your browser.

## Configuration

Environment variables (recommended):

- `GROQ_API_KEY` — your Groq api key 
- `MODEL` — the Groq model name (see https://console.groq.com/docs/models)

Notes:

- In `Agent.py` you’ll see a hard‑coded `api_key` and the `load_dotenv()` call commented. For security, remove the hard‑coded key, enable `load_dotenv()`, and read the key from `os.environ['GROQ_API_KEY']`. Don’t commit your `.env` file.
- Mind model limits (requests/minute, context window, tokens). Pick a model that fits your use case and quota.

## Customization

- System prompt: edit `SYSTEM_PROMPT` in `Agent.py` to control tone, style, or language.
- Model: set via the `model` parameter in `ChatGroq` (and/or the `MODEL` env var).
- UI: in `Front.py`
  - `st.set_page_config(page_title=..., page_icon=...)` to change the tab title/icon.
  - Update the CSS block in `st.markdown("""<style>...</style>""", unsafe_allow_html=True)` to restyle the page.

## Deploying to Heroku (GitHub integration)

1) Push your code to GitHub (ensure `.env` is ignored and not committed).

2) Create a new Heroku app at https://dashboard.heroku.com/apps

3) In the Deploy tab, choose “GitHub” as the deployment method and connect your repo.

4) In the Settings tab → Config Vars, add:

   - `GROQ_API_KEY` → your key

5) Back in the Deploy tab, deploy the branch. Once done, click “View app”.


## Troubleshooting

- Invalid API key / 401: Check `GROQ_API_KEY` is set in your environment (local) or Heroku Config Vars (prod).
- Model errors: Ensure the `MODEL` name matches Groq docs and your account has access/quota.
- Nothing renders on Heroku: Confirm the `Procfile` exists in the repo root and you didn’t modify it. Logs can be viewed in the Heroku dashboard.
- Rate limits: Pick a lighter model or reduce requests. Add simple retries/backoff as needed.

## Dependencies

Listed in `requirements.txt`:

- streamlit
- python-dotenv
- langchain-core
- langchain-groq
- groq

## Notes

- Do not commit secrets. Keep `.env` local only; use Heroku Config Vars in production.
- If you forked this repo, review `Agent.py` and remove any hard‑coded keys.

---

Happy hacking! Customize the prompt, tweak the UI, and share your chatbot.