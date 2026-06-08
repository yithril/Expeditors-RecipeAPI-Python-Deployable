# Database scripts

Scripts for setting up the PostgreSQL database used by the Recipe API.

## Full setup — `schema.sql`

**File:** `scripts/schema.sql`

This script:

1. Creates the **`recipes`** database (Section 1)
2. Creates the **`recipe`** table inside it (Section 2)

### Azure Data Studio

1. Connect to your Azure PostgreSQL server using the **`postgres`** database.
2. Open **`scripts/schema.sql`**, highlight **SECTION 1** only, and run it.
3. Connect to the **`recipes`** database (refresh the server list if needed).
4. Highlight **SECTION 2** only and run it.

If Section 1 says the database already exists, skip to Section 2.

### psql (one command)

From the project root:

```bash
psql "host=YOUR_HOST.postgres.database.azure.com port=5432 dbname=postgres user=YOUR_USER@YOUR_SERVER sslmode=require" -f scripts/schema.sql
```

Replace the connection details with values from Exercise 2.1.

## Load sample data

The SQL script creates an empty table. To load 18 recipes:

**Option 1 — deploy and start the app**

Set `DB_URL` in App Service. The app creates the database/table if missing and seeds when the table is empty.

**Option 2 — run the Python init script from your machine**

```bash
set DB_URL=postgresql://YOUR_USER:YOUR_PASSWORD@YOUR_HOST.postgres.database.azure.com:5432/recipes?sslmode=require
python -m scripts.init_db
```

`init_db.py` creates the **`recipes`** database if needed, creates the table, and seeds 18 recipes.

## Files in this folder

| File | Purpose |
|------|---------|
| `schema.sql` | Create `recipes` database + `recipe` table |
| `init_db.py` | Python: create database, table, and seed if empty |
| `seed_data.py` | Seed data used by the app and `init_db.py` |
