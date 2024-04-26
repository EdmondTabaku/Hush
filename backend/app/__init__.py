from flask import Flask
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler
from .config import Config
import os

# Create Flask application instance
app = Flask(__name__)

# Enable CORS
CORS(app, resources={r'/*': {'origins': [config.Config.FRONTEND_URL]}}, supports_credentials=True)
app.config['CORS_HEADERS'] = ['Content-Type', 'Authorization']

# Load configuration settings
app.config.from_object(Config)

# Initialize logging
file_handler = RotatingFileHandler('app.log', maxBytes=1024 * 1024 * 10, backupCount=5)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
file_handler.setLevel(logging.INFO)

app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

# Initialize logger
logger = logging.getLogger(__name__)

# Import routes
from app.route.message import message_bp
app.register_blueprint(message_bp, url_prefix='/message')

from app.route.client import client_bp
app.register_blueprint(client_bp, url_prefix='/client')