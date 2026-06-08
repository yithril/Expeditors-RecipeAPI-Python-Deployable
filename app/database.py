from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker

engine = None
SessionLocal = None

_BUILTIN_DATABASES = frozenset({"postgres", "template0", "template1"})


class Base(DeclarativeBase):
    pass


def ensure_database_exists(database_url: str) -> None:
    """Create the target PostgreSQL database if it does not exist yet."""
    parsed = make_url(database_url)
    database_name = parsed.database

    if not database_name or database_name in _BUILTIN_DATABASES:
        return

    admin_url = parsed.set(database="postgres")
    admin_engine = create_engine(admin_url, echo=False, isolation_level="AUTOCOMMIT")

    try:
        with admin_engine.connect() as connection:
            exists = connection.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :name"),
                {"name": database_name},
            ).scalar()

            if not exists:
                connection.execute(text(f'CREATE DATABASE "{database_name}"'))
    finally:
        admin_engine.dispose()


def init_engine(database_url: str):
    global engine, SessionLocal

    engine = create_engine(database_url, echo=False)
    SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))


def create_tables():
    if engine is None:
        raise RuntimeError("Database engine is not initialized")
    Base.metadata.create_all(bind=engine)


def dispose_engine():
    global engine, SessionLocal
    if SessionLocal is not None:
        SessionLocal.remove()
        SessionLocal = None
    if engine is not None:
        engine.dispose()
        engine = None
