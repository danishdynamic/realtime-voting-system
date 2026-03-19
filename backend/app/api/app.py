from flask import Flask
from backend.app.api.extensions import socketio
from backend.app.api.routes import api_blueprint

socketio_instance = socketio

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