import click
from .app import create_app


@click.command()
@click.option("--port", default=5000, help="Port to run the application on.", type=int)
@click.option("--host", default="127.0.0.1", help="Host to run the application on.")
@click.option("--debug/--no-debug", default=True, help="Enable or disable debug mode.")
def main(
    port: int,
    host: str,
    debug: bool,
) -> None:
    """Run the Skewer application."""
    app = create_app()
    app.run(debug=debug, host=host, port=port)
