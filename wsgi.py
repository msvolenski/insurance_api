"""Application Entry Point."""

from application import create_app


app = create_app()


# Start Application
if __name__ == "__main__":
    app.run()
