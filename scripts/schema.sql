-- Recipe API — create the recipe table
--
-- Location in this project: scripts/schema.sql
--
-- Run this script against your Azure PostgreSQL database (e.g. "recipes")
-- after Exercise 2.1 and before deploying the Flask app.
--
-- Options:
--   • Azure Data Studio — connect to your server, open this file, run it
--   • psql — psql "host=... user=... dbname=recipes sslmode=require" -f scripts/schema.sql
--
-- This script only creates the table. To load the 18 sample recipes afterward, either:
--   • deploy and start the app (it seeds when the table is empty), or
--   • run: python -m scripts.init_db   (requires DB_URL in your environment)

CREATE TABLE IF NOT EXISTS recipe (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  ingredients TEXT NOT NULL,
  instructions TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
