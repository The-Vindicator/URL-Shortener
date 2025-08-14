
# Shorty — Flask URL Shortener

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

## Docker

```
# Build
docker build -t shorty .

# Run
docker run --rm -p 8000:8000 -e BASE_URL="http://localhost:8000" -v shorty_data:/data shorty
```

Then open http://localhost:8000

Or with **docker-compose**:
```
docker compose up --build
```

---

## Deploy (Render)

1. Push this folder to a GitHub repo.
2. Create a new **Web Service** on Render.
3. Runtime: **Docker** (use the included Dockerfile).
4. Add environment variable `BASE_URL` to your public domain from Render.
5. Optional: Use a persistent disk mounted to `/data` if you don’t want to lose the SQLite DB on redeploys.

---

## Project Structure

```
url-shortener-flask/
├─ app.py
├─ wsgi.py
├─ requirements.txt
├─ Dockerfile
├─ docker-compose.yml
├─ templates/
│  ├─ base.html
│  ├─ index.html
│  ├─ result.html
│  ├─ info.html
│  └─ 404.html
└─ static/
   └─ styles.css
```

---

## API Quick Test

```
# Create a short link
curl -X POST http://127.0.0.1:5000/api/shorten   -H "Content-Type: application/json"   -d '{ "url": "https://example.com" }'
```

**Response**:
```
{
  "code": "Ab12Xy",
  "short_url": "http://127.0.0.1:5000/Ab12Xy",
  "original_url": "https://example.com"
}
```

---

## Notes
- SQLite database file is `urls.db` by default (or `DB_PATH` env).
- Change `SECRET_KEY` in production.
- `BASE_URL` is only for rendering; redirects work regardless.
