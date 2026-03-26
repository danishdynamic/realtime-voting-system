from backend.app.api.app import create_app
from backend.app.api.extensions import socketio
from backend.infrastructure.db.database import engine, Base

app = create_app()

if __name__ == "__main__":
    # ✅ Add this line to create tables if they don't exist
    with app.app_context():
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")

    socketio.run(app, debug=True, port=5000)