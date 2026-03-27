import os
from backend.app.api.app import create_app
from backend.app.api.extensions import socketio
from backend.infrastructure.db.database import engine, Base

# 1. Create the Flask Application instance
app = create_app()

# 2. Configure the Socket.IO Message Queue
# This is CRITICAL for the Kafka Consumer to talk to the Flask App.
# If running in Docker, replace 'localhost' with 'redis'
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

if __name__ == "__main__":
    # ✅ Initialize Database Tables
    # This ensures SQLite has the 'votes', 'polls', and 'options' tables ready
    with app.app_context():
        try:
            Base.metadata.create_all(bind=engine)
            print("✅ Database tables verified/created successfully!")
        except Exception as e:
            print(f"❌ Database initialization failed: {e}")

    # ✅ Configure Socket.IO for External Process Communication
    # By setting the message_queue here, the app listens to Redis for 
    # events emitted by your background Kafka Consumer.
    socketio.init_app(app, message_queue=REDIS_URL, cors_allowed_origins="*")

    print(f"🚀 Real-time Voting Backend starting on http://127.0.0.1:5000")
    
    # ✅ Run the Server
    # Using socketio.run instead of app.run is required for WebSockets
    socketio.run(
        app, 
        debug=True, 
        port=5000, 
        allow_unsafe_werkzeug=True  # Useful for local development
    )