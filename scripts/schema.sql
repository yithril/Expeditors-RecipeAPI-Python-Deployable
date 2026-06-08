-- =============================================================================
-- Recipe API — full database setup
-- File: scripts/schema.sql
-- =============================================================================
--
-- Creates the PostgreSQL database "recipes" (if needed) and the "recipe" table.
--
-- AZURE DATA STUDIO (recommended for students)
--   Step 1: Connect to the "postgres" database on your server.
--           Highlight and run SECTION 1 only.
--   Step 2: Connect to the "recipes" database (refresh if it was just created).
--           Highlight and run SECTION 2 only.
--
-- psql (one command from the project root — runs both sections automatically)
--   psql "host=YOUR_HOST.postgres.database.azure.com port=5432 dbname=postgres user=YOUR_USER@YOUR_SERVER sslmode=require" -f scripts/schema.sql
--
-- After this script, deploy the app or run "python -m scripts.init_db" to load
-- 18 sample recipes (the app also seeds on startup when the table is empty).
-- =============================================================================

-- SECTION 1 — run while connected to database "postgres"
-- If you see "already exists", the database is fine — continue to Section 2.

CREATE DATABASE recipes;

-- SECTION 2 — run while connected to database "recipes"
-- psql only: the line below switches to the recipes database automatically.

\connect recipes

CREATE TABLE IF NOT EXISTS recipe (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  ingredients TEXT NOT NULL,
  instructions TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
