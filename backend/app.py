from flask import Flask
from extensions import socketio
from backend.app.api.routes import api_blueprint
from flask_cors import CORS

socketio_instance = socketio

def create_app():
    app = Flask(__name__)

    # ✅ 2. Enable CORS for Axios/HTTP requests
    CORS(app, resources={r"/*": {"origins": "*"}})

    socketio_instance.init_app(app, cors_allowed_origins="*")

    app.register_blueprint(api_blueprint)

    return app


@socketio_instance.on("connect")
def handle_connect():
    print("Client connected")


if __name__ == "__main__":
    app = create_app()
    socketio_instance.run(app, debug=True, host="127.0.0.1", port=5000)