from flask import Flask
from flask_socketio import SocketIO
from app.api.routes import api_blueprint

socketio_instance = SocketIO(cors_allowed_origins="*")


def create_app():
    app = Flask(__name__)

    socketio_instance.init_app(app)

    app.register_blueprint(api_blueprint)

    return app


@socketio_instance.on("connect")
def handle_connect():
    print("Client connected")


if __name__ == "__main__":
    app = create_app()
    socketio_instance.run(app, debug=True)