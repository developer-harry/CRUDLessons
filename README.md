# CRUD Lessons

A small Flask and SQLite task app for practicing Create, Read, Update, and Delete.

## Requirements

- Python 3.10 or newer
- pip

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000/ in your browser.

The SQLite database (`tasks.db`) is created automatically the first time the app
runs. It is local data and is intentionally excluded from Git.
