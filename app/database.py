from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker

engine = None
SessionLocal = None


class Base(DeclarativeBase):
    pass


def init_engine(database_url: str):
    global engine, SessionLocal

    engine_kwargs = {"echo": False}
    if database_url.startswith("sqlite"):
        # Tests only — in-memory SQLite for pytest without a real database.
        engine_kwargs["connect_args"] = {"check_same_thread": False}

    engine = create_engine(database_url, **engine_kwargs)
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
