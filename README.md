# MMSU Medical Dashboard

A health records management system for MMSU personnel — built with Flask and PostgreSQL.

---

## Features

- Personnel records with medical conditions, visit history, and department tracking
- Dashboard with KPI cards and charts
- CSV import/export, per-personnel PDF export, medicine inventory Excel report
- Audit log for all admin actions
- CSRF protection, rate-limited login, and hashed passwords

---

## Local Setup

### 1. Clone and install dependencies

```bash
git clone <your-repo-url>
cd mmsu-medical
pip install -r requirements.txt
```

### 2. Create your environment file

```bash
cp .env.example .env
# Edit .env and fill in your DATABASE_URL, SECRET_KEY, and admin credentials
```

### 3. Start PostgreSQL and run the app

The app creates its tables automatically on first run.

```bash
# Load env vars (Linux/macOS)
export $(cat .env | xargs)

# Run locally
python app.py
```

Visit `http://localhost:5000` and log in with your `ADMIN_USERNAME` / `ADMIN_PASSWORD`.

---

## Deploying to Heroku / Railway / Render

### Required environment variables

Set these in your platform's dashboard (never hardcode them):

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string (provided automatically by most platforms) |
| `SECRET_KEY` | Random 32-byte hex string — generate with `python -c "import secrets; print(secrets.token_hex(32))"` |
| `FLASK_ENV` | Set to `production` |
| `ADMIN_USERNAME` | Login username |
| `ADMIN_PASSWORD` | Login password — use a strong password in production |

### Heroku

```bash
heroku create your-app-name
heroku addons:create heroku-postgresql:essential-0
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
heroku config:set FLASK_ENV=production
heroku config:set ADMIN_USERNAME=admin
heroku config:set ADMIN_PASSWORD=your_strong_password
git push heroku main
```

### Railway / Render

1. Connect your GitHub repository.
2. Add a PostgreSQL plugin/database — the platform sets `DATABASE_URL` automatically.
3. Add the remaining environment variables listed above.
4. The `Procfile` tells the platform to run Gunicorn automatically.

---

## Project Structure

```
├── app.py              # Flask application and all routes
├── index.html          # Main dashboard (served as a Jinja2 template)
├── login.html          # Login page
├── requirements.txt    # Python dependencies
├── Procfile            # Production server command (Gunicorn)
└── .env.example        # Template for environment variables
```

---

## Security Notes

- Change `ADMIN_PASSWORD` before deploying — the default `mmsu2024` is insecure.
- `SECRET_KEY` must be set to a long random value in production.
- The app enforces HTTPS-only cookies when `FLASK_ENV=production`.
- All write operations require a valid CSRF token.
- Login is rate-limited to 10 attempts per 5 minutes per IP.