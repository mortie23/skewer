import teradatasql
from flask import current_app, g


def get_db():
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


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
