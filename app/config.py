import os


class DatabaseConfigurationError(Exception):
    """Raised when required database environment variables are missing."""


class Config:
    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"
    TESTING = False
    SQLALCHEMY_ECHO = DEBUG

    @staticmethod
    def get_database_url() -> str:
        url = os.environ.get("DB_URL", "").strip()
        if url:
            return url

        host = os.environ.get("DB_HOST", "").strip()
        if host:
            username = os.environ.get("DB_USERNAME", "")
            password = os.environ.get("DB_PASSWORD", "")
            database = os.environ.get("DB_NAME", "recipes")
            port = os.environ.get("DB_PORT", "5432")
            return f"postgresql://{username}:{password}@{host}:{port}/{database}"

        raise DatabaseConfigurationError(
            "Database not configured. Set DB_URL to a PostgreSQL connection string, "
            "or set DB_HOST with DB_USERNAME and DB_PASSWORD. "
            "Azure example: postgresql://user:pass@host.postgres.database.azure.com:5432/recipes?sslmode=require"
        )


class TestConfig(Config):
    TESTING = True

    @staticmethod
    def get_database_url() -> str:
        return "sqlite:///:memory:"
