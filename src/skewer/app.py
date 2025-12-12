from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from .config import load_config


def create_app(config=None):
    app = Flask(__name__)
    bootstrap = Bootstrap5(app)

    # Load configuration
    td_config = load_config()
    app.config["TERADATA_CONFIG"] = td_config

    from . import db

    db.init_app(app)

    @app.route("/")
    def index():
        conn_status = (
            "Config Loaded" if app.config.get("TERADATA_CONFIG") else "Config Missing"
        )

        db_info = []
        try:
            conn = db.get_db()
            with conn.cursor() as cur:
                cur.execute("select * from dbc.dbcinfo")
                rows = cur.fetchall()
                # Keep rows as list of tuples/rows for template iteration
                db_info = rows
        except Exception as e:
            # We'll handle errors gracefully in the template or pass as flash/context
            conn_status = f"Error: {e}"

        return render_template("index.html", conn_status=conn_status, db_info=db_info)

    return app
