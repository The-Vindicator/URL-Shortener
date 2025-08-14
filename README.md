
# URL Shortener

A simple, clean URL shortener with a web UI and a tiny JSON API. Uses Flask + SQLite.

## Features
- Create short links with a random code or a **custom alias**
- Redirects to the original URL
- Tracks **click count** and **creation time**
- Lightweight Bootstrap UI
- JSON API: `POST /api/shorten` with `{ "url": "...", "custom": "optional" }`

---

## Run Locally (Python)

> Works on Windows, macOS, and Linux. Python 3.10+ recommended.

```
# 1) Get the code
# (if you downloaded a zip, unzip it and cd into the folder)
cd url-shortener-flask

# 2) Create a virtual environment
python -m venv .venv
# Activate it
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3) Install deps
pip install -r requirements.txt

# 4) Set optional env (for nicer short URLs in the UI)
# Windows PowerShell:
$env:BASE_URL="http://127.0.0.1:5000"
# macOS/Linux bash:
export BASE_URL="http://127.0.0.1:5000"

# 5) Start
python app.py
```

Open http://127.0.0.1:5000 — create a link. Click **Open** to test.  
Stats page: `http://127.0.0.1:5000/info/<code>`

---
