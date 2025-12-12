from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5  # type: ignore
from typing import Optional, Dict, Any, Union
from .config import load_config


def create_app(
    config: Optional[Dict[str, Any]] = None,
) -> Flask:
    """
    Create and configure the Flask application.

    :param config: Optional dictionary to override default configuration.
    :return: Configured Flask application instance.
    """
    app = Flask(__name__)
    bootstrap = Bootstrap5(app)

    # Load configuration
    td_config = load_config()
    app.config["TERADATA_CONFIG"] = td_config

    from . import db

    db.init_app(app)

    @app.route("/")
    def index() -> str:
        """
        Render the index page with connection status and DBC info.

        :return: HTML content for the home page.
        """
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

    @app.route("/databases")
    def database_list() -> str:
        """
        Render the list of all databases.

        :return: HTML content for the database list page.
        """
        from . import schema

        try:
            dbs = schema.get_databases()
            return render_template("databases.html", databases=dbs)
        except Exception as e:
            # For now, just show error on index or specific page
            return render_template("databases.html", databases=[], error=str(e))

    @app.route("/tables/<database_name>")
    def table_list(database_name: str) -> str:
        """
        Render the list of tables for a specific database.

        :param database_name: Name of the database to list tables for.
        :return: HTML content for the table list page.
        """
        from . import schema

        try:
            tables = schema.get_tables(database_name)
            return render_template(
                "tables.html", database_name=database_name, tables=tables
            )
        except Exception as e:
            return render_template(
                "tables.html", database_name=database_name, tables=[], error=str(e)
            )

    @app.route("/sample/<database_name>/<table_name>")
    def table_sample(
        database_name: str,
        table_name: str,
    ) -> str:
        """
        Render a sample of data from a table.

        :param database_name: Name of the database.
        :param table_name: Name of the table.
        :return: HTML content for the table sample page.
        """
        from . import schema

        page = request.args.get("page", 1, type=int)
        limit = 100
        offset = (page - 1) * limit

        try:
            columns, rows = schema.get_table_sample(
                database_name, table_name, limit=limit, offset=offset
            )
            return render_template(
                "sample.html",
                database_name=database_name,
                table_name=table_name,
                columns=columns,
                rows=rows,
                page=page,
                next_page=page + 1,
                prev_page=page - 1 if page > 1 else None,
            )
        except Exception as e:
            return render_template(
                "sample.html",
                database_name=database_name,
                table_name=table_name,
                columns=[],
                rows=[],
                page=page,
                error=str(e),
            )

    @app.route("/detail/<database_name>/<table_name>")
    def record_detail(database_name: str, table_name: str) -> str:
        """
        Render the record detail page with a search form.

        :param database_name: Name of the database.
        :param table_name: Name of the table.
        :return: HTML content for the detail page.
        """
        from . import schema

        key_column = request.args.get("key_column", "")
        key_value = request.args.get("key_value", "")

        columns = []
        record = None
        error = None

        if key_column and key_value:
            try:
                columns, record = schema.get_record(
                    database_name, table_name, key_column, key_value
                )
                if not record:
                    error = f"No record found for {key_column}={key_value}"
            except Exception as e:
                error = str(e)

        return render_template(
            "detail.html",
            database_name=database_name,
            table_name=table_name,
            key_column=key_column,
            key_value=key_value,
            columns=columns,
            record=record,
            error=error,
        )

    return app
