from flask import Flask
from flask_cors import CORS
from backend.app.api.routes import api_blueprint
from backend.extensions import socketio
from backend.infrastructure.db.database import init_db


def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Initialize database
    init_db()
    
    # Register blueprints
    app.register_blueprint(api_blueprint, url_prefix="/api")
    
    # Initialize SocketIO
    socketio.init_app(app, cors_allowed_origins="*")
    
    return app


def create_socketio_app():
    """For running WebSocket server standalone."""
    app = Flask(__name__)
    socketio.init_app(app, message_queue='redis://localhost:6379/0')
    return app