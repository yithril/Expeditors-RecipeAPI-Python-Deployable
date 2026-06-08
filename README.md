# Recipe API (Python / Flask)

Educational REST API for teaching **Azure App Service deployment** and REST fundamentals. Built with **Python 3.11+**, **Flask**, **SQLAlchemy 2**, and **PostgreSQL** (Azure Database for PostgreSQL Flexible Server).

## What you get

- CRUD on `/api/recipes` with query filters (`name`, `ingredients`)
- Request validation and consistent error responses
- **18 seed recipes** loaded automatically when the database is empty
- Swagger UI at **`/apidocs`**
- CORS enabled for browser labs

## Prerequisites

- Python 3.11+
- A **PostgreSQL** database (Azure Flexible Server in production; local Postgres or your Azure server for dev)
- GitHub secrets for CI/CD deploy (see below)

## Quick start (local)

1. Create a PostgreSQL server in Azure (Exercise 2.1). The app expects a database named **`recipes`** — run **`scripts/schema.sql`** to create it, or let the app create it automatically on startup.

2. Copy environment variables:

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux

pip install -r requirements.txt
copy .env.example .env
```

3. Edit `.env` and set `DB_URL` to your PostgreSQL connection string. For Azure, include SSL:

```text
postgresql://user:password@your-server.postgres.database.azure.com:5432/recipes?sslmode=require
```

4. Run the app:

```bash
set FLASK_APP=app               # Windows cmd
flask run                       # http://127.0.0.1:5000
```

Open:

- API: `http://127.0.0.1:5000/api/recipes`
- Swagger: `http://127.0.0.1:5000/apidocs`

For the deployment lab, run **`scripts/schema.sql`** against PostgreSQL first. On startup the app **seeds 18 recipes** when the table is empty.

## API base URL (Insomnia / Postman)

| Resource | URL |
|----------|-----|
| API | `http://127.0.0.1:5000` |
| Recipes | `GET /api/recipes` (optional query: `name`, `ingredients`) |
| Swagger UI | `http://127.0.0.1:5000/apidocs` |

JSON fields use camelCase in responses (for example `createdAt`, `updatedAt`).

## Configuration

| Variable | Purpose |
|----------|---------|
| `DB_URL` | Full SQLAlchemy PostgreSQL URL (recommended for Azure) |
| `DB_HOST` | Server hostname; used with username/password if `DB_URL` is not set |
| `DB_USERNAME` | PostgreSQL username |
| `DB_PASSWORD` | PostgreSQL password |
| `DB_NAME` | Database name (default: `recipes`) |
| `DB_PORT` | Port (default: `5432`) |
| `FLASK_DEBUG` | Set to `1` for debug mode |

**Azure Flexible Server:** the server type does not matter to the app — PostgreSQL is PostgreSQL. Copy the connection string from the Azure portal, set it as `DB_URL` in App Settings, and ensure `?sslmode=require` is present.

Either `DB_URL` **or** `DB_HOST` + credentials must be set. The app will not start without a database configuration.

## Create the database and table (lab step)

**`scripts/schema.sql`** creates the **`recipes`** database and the **`recipe`** table. See **`scripts/README.md`** for Azure Data Studio and `psql` steps.

You can skip the manual SQL step if you prefer: on startup the app **creates the `recipes` database** (when missing) and the **`recipe`** table, then seeds 18 recipes when the table is empty.

Optional — same result from your machine:

```bash
set DB_URL=postgresql://user:pass@host:5432/recipes?sslmode=require
python -m scripts.init_db
```

Unlike Spring Boot with Flyway/Liquibase, Flask does **not** auto-run versioned migrations. If you later change the model, you would add **Alembic** (Flask-Migrate). That is not included in this demo.

## Running tests

```bash
pip install -r requirements-dev.txt
set TEST_DB_URL=postgresql://user:pass@host:5432/recipes_test?sslmode=require
pytest
```

Tests use the same PostgreSQL connection as the app (`DB_URL` or `TEST_DB_URL`). Use a separate test database if you do not want test data in your dev database.

## Production (Azure App Service)

1. Create **Azure Database for PostgreSQL Flexible Server** (Exercise 2.1).
2. Create a **Linux Web App** with **Python 3.11**.
3. Set startup command to `startup.sh` (or `gunicorn --bind=0.0.0.0:$PORT --workers=2 wsgi:app`).
4. In **Configuration → Application settings**, set:
   - `DB_URL` — full connection string with `?sslmode=require` (database name `recipes` at end of URL)
   - Or `DB_HOST`, `DB_USERNAME`, `DB_PASSWORD`, `DB_NAME`
5. Optional: run **`scripts/schema.sql`** (see `scripts/README.md`). Otherwise the app creates the database and table on first start.
6. Deploy the app. On first start it creates the `recipes` database if needed, creates the table, and seeds 18 recipes.
7. Verify: `GET https://<app-name>.azurewebsites.net/api/recipes` returns 18 recipes.

Allow the App Service outbound IP (or enable "Allow Azure services") in the PostgreSQL firewall so the web app can connect.

### GitHub Actions deploy

Push to `main` (or use workflow dispatch). Required secrets:

- `AZURE_WEBAPP_NAME`
- `AZURE_WEBAPP_PUBLISH_PROFILE`
- `DB_URL`
- `DB_USERNAME`
- `DB_PASSWORD`

The workflow runs tests, deploys the repo, and sets database App Settings.

## Project layout

```text
app/                  Flask application (models, routes, services, schemas)
scripts/              schema.sql (create table), init_db.py, seed_data.py — see scripts/README.md
tests/                pytest suite
wsgi.py               Gunicorn entry point
startup.sh            Azure startup command
```
