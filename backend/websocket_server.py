from app import create_socketio_app
from backend.extensions import socketio
from backend.infrastructure.redis.redis_client import redis_client

app = create_socketio_app()

@socketio.on("connect")
def handle_connect():
    print("Client connected")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8000)