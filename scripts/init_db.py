import sys

from app.config import Config
from app.database import SessionLocal, create_tables, dispose_engine, init_engine
from scripts.seed_data import seed_if_empty


def main() -> int:
    database_url = Config.get_database_url()
    print(f"Connecting to database: {database_url}")

    try:
        database.ensure_database_exists(database_url)
        init_engine(database_url)
        create_tables()
        db = SessionLocal()
        try:
            inserted = seed_if_empty(db)
            if inserted:
                print(f"Seeded {inserted} recipes.")
            else:
                print("Database already contains recipes; no seed data added.")
        finally:
            db.close()

        print("Database initialization completed successfully.")
        return 0
    except Exception as exc:
        print(f"Database initialization failed: {exc}", file=sys.stderr)
        return 1
    finally:
        dispose_engine()


if __name__ == "__main__":
    raise SystemExit(main())
