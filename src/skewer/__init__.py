from .app import create_app


def main():
    app = create_app()
    # Debug=True for development, but in production we'd want something else.
    # For now, this is fine for local dev.
    app.run(debug=True)
