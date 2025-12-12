import teradatasql  # type: ignore
from flask import current_app, g, Flask
from typing import Any


def get_db() -> Any:
    """
    Get or create a Teradata connection for the current request context.

    :return: A teradatasql connection object.
    :raises RuntimeError: If TERADATA_CONFIG is missing from app config.
    """
    if "db" not in g:
        config = current_app.config.get("TERADATA_CONFIG", {})
        if not config:
            raise RuntimeError("Teradata configuration not found.")

        # teradatasql.connect expects kwargs.
        # config should be a dict with keys matching teradatasql arguments: host, user, password, logmech, etc.
        # User has confirmed keys in toml will match teradatasql requirements.

        kwargs = {}
        kwargs.update(config)

        g.db = teradatasql.connect(**kwargs)

    return g.db


def close_db(e: Any = None) -> None:
    """
    Close the database connection if it exists.

    :param e: The exception that caused the teardown, if any.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
