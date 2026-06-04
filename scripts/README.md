# Database scripts

Scripts for setting up the PostgreSQL database used by the Recipe API.

## Create the `recipe` table — `schema.sql`

**File:** `scripts/schema.sql` (in this project folder)

Run this script against the **`recipes`** database on your Azure PostgreSQL Flexible Server from Exercise 2.1. It creates the `recipe` table the API expects.

### Option A — Azure Data Studio

1. Connect to your Azure PostgreSQL server.
2. Open the **`recipes`** database.
3. Open **`scripts/schema.sql`** from this project.
4. Run the script.

### Option B — psql (command line)

From the project root:

```bash
psql "host=YOUR_HOST.postgres.database.azure.com port=5432 dbname=recipes user=YOUR_USER@YOUR_SERVER sslmode=require" -f scripts/schema.sql
```

Replace the connection details with values from Exercise 2.1.

## Load sample data (optional)

`schema.sql` creates an empty table. The API needs rows before `GET /api/recipes` returns data.

**Option 1 — let the app seed on startup**

After you deploy and set `DB_URL` in App Service, the app inserts 18 recipes automatically when the table is empty.

**Option 2 — run the Python init script from your machine**

```bash
set DB_URL=postgresql://YOUR_USER:YOUR_PASSWORD@YOUR_HOST.postgres.database.azure.com:5432/recipes?sslmode=require
python -m scripts.init_db
```

## Files in this folder

| File | Purpose |
|------|---------|
| `schema.sql` | SQL to create the `recipe` table |
| `init_db.py` | Python script: create table + seed 18 recipes if empty |
| `seed_data.py` | Seed data used by the app and `init_db.py` |
