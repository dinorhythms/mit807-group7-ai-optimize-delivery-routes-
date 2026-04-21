# WSGI entry point for Render deployment
from web_app import application

# This makes the Flask app available as 'app' for gunicorn
app = application