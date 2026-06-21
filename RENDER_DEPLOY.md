# Deploying This Portfolio on Render

## Option 1: Blueprint Deploy

1. Push this project to GitHub.
2. In Render, choose **New +** then **Blueprint**.
3. Connect the GitHub repository.
4. Render will read `render.yaml`.
5. Deploy.

Render will use:

```text
Build Command: pip install -r requirements.txt
Start Command: gunicorn Backend.app:app
```

## Option 2: Manual Web Service

1. Push this project to GitHub.
2. In Render, choose **New +** then **Web Service**.
3. Connect the GitHub repository.
4. Use these settings:

```text
Environment: Python
Build Command: pip install -r requirements.txt
Start Command: gunicorn Backend.app:app
```

## SQLite Note

The app can use either PostgreSQL or SQLite:

- On Render, `render.yaml` provisions a PostgreSQL database and passes `DATABASE_URL` to the app.
- Locally, if `DATABASE_URL` is not set, the app falls back to SQLite at `Backend/database.db`.

## SQLite Fallback

If you add a persistent disk later, set this environment variable in Render:

```text
DATABASE_PATH=/var/data/database.db
```

Then the app will store tickets there instead of `Backend/database.db`.

PostgreSQL is recommended for the deployed version.
