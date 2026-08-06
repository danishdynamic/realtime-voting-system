from flask_socketio import SocketIO

# Initialize without an app first
socketio = SocketIO(cors_allowed_origins="*")