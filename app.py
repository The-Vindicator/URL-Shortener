
import os
import sqlite3
import string
import random
from datetime import datetime
from urllib.parse import urlparse

from flask import (
    Flask, request, redirect, render_template, url_for, flash, jsonify, abort
)

DB_PATH = os.environ.get("DB_PATH", "urls.db")
BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:5000")
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE NOT NULL,
            original_url TEXT NOT NULL,
            clicks INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
        '''
    )
    conn.commit()
    conn.close()

def code_exists(code: str) -> bool:
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT 1 FROM urls WHERE short_code = ?", (code,))
    exists = c.fetchone() is not None
    conn.close()
    return exists

def save_mapping(code: str, original_url: str):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO urls (short_code, original_url, clicks, created_at) VALUES (?, ?, 0, ?)",
        (code, original_url, datetime.utcnow().isoformat() + "Z"),
    )
    conn.commit()
    conn.close()

def get_original(code: str):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT original_url, clicks, created_at FROM urls WHERE short_code = ?", (code,))
    row = c.fetchone()
    conn.close()
    return row

def increment_click(code: str):
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?", (code,))
    conn.commit()
    conn.close()

ALPHABET = string.ascii_letters + string.digits

def generate_code(length: int = 6) -> str:
    for _ in range(10):
        code = ''.join(random.choices(ALPHABET, k=length))
        if not code_exists(code):
            return code
    while True:
        length += 1
        code = ''.join(random.choices(ALPHABET, k=length))
        if not code_exists(code):
            return code

def normalize_url(url: str) -> str:
    url = url.strip()
    if not url:
        return url
    parsed = urlparse(url)
    if not parsed.scheme:
        url = 'http://' + url
    return url

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form.get('url', '').strip()
    custom = request.form.get('custom', '').strip()

    long_url = normalize_url(long_url)

    if not long_url or '.' not in urlparse(long_url).netloc:
        flash('Please enter a valid URL.', 'danger')
        return redirect(url_for('index'))

    if custom:
        if not all(ch.isalnum() or ch in '-_' for ch in custom):
            flash("Custom alias may contain letters, digits, '-' and '_' only.", 'warning')
            return redirect(url_for('index'))
        if code_exists(custom):
            flash('That custom alias is taken. Try another.', 'warning')
            return redirect(url_for('index'))
        code = custom
    else:
        code = generate_code()

    save_mapping(code, long_url)
    short_url = f"{BASE_URL.rstrip('/')}/{code}"
    return render_template('result.html', short_url=short_url, long_url=long_url)

@app.route('/<code>', methods=['GET'])
def follow(code):
    row = get_original(code)
    if not row:
        return render_template('404.html'), 404
    increment_click(code)
    return redirect(row['original_url'], code=302)

@app.route('/info/<code>', methods=['GET'])
def info(code):
    row = get_original(code)
    if not row:
        abort(404)
    data = {
        'code': code,
        'original_url': row['original_url'],
        'clicks': row['clicks'],
        'created_at': row['created_at'],
        'short_url': f"{BASE_URL.rstrip('/')}/{code}",
    }
    return render_template('info.html', **data)

@app.route('/api/shorten', methods=['POST'])
def api_shorten():
    payload = request.get_json(force=True, silent=True) or {}
    long_url = normalize_url(payload.get('url', ''))
    custom = (payload.get('custom') or '').strip()

    if not long_url or '.' not in urlparse(long_url).netloc:
        return jsonify({'error': 'invalid_url'}), 400

    if custom:
        if not all(ch.isalnum() or ch in '-_' for ch in custom):
            return jsonify({'error': 'invalid_custom'}), 400
        if code_exists(custom):
            return jsonify({'error': 'custom_taken'}), 409
        code = custom
    else:
        code = generate_code()

    save_mapping(code, long_url)
    return jsonify({
        'code': code,
        'short_url': f"{BASE_URL.rstrip('/')}/{code}",
        'original_url': long_url,
    }), 201

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
