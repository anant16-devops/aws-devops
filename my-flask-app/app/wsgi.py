# Gunicorn entry point for the Flask application
# This file is used to run the Flask app with Gunicorn.
# It imports the Flask app instance from main.py and runs it.
# Gunicorn will use this file to start the application server.

from main import app

if __name__ == "__main__":
    app.run()