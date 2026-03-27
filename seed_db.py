import sys
import os
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.infrastructure.db.database import SessionLocal, engine, Base
from backend.infrastructure.models.option_model import OptionModel as Option
from backend.infrastructure.models.poll_model import PollModel as Poll

def seed():
    # 1. Create the tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        print("Cleaning up existing test data...")
        # 2. Find and delete the existing test poll to ensure a fresh start
        existing_poll = db.query(Poll).filter_by(public_id="test-poll-1").first()
        if existing_poll:
            # Delete associated options first to avoid foreign key constraints
            db.query(Option).filter_by(poll_id=existing_poll.id).delete()
            db.delete(existing_poll)
            db.commit()
            print("Successfully removed old 'test-poll-1' and its options.")

        # 3. Create the New Poll
        print("Creating new poll...")
        new_poll = Poll(
            public_id="test-poll-1", 
            question="Favorite Stack?", 
            created_by='admin', 
            created_at=datetime.now(), 
            start_time=datetime.now(), 
            end_time=datetime.now() + timedelta(days=7)
        )
        db.add(new_poll)
        db.commit()
        db.refresh(new_poll) # Refresh to get the generated ID from the DB

        # 4. Add the Options
        # Note: Changed 'option_text' to 'text' based on your Error Message
        print(f"Adding options for Poll ID: {new_poll.id}")
        opts = [
            Option(poll_id=new_poll.id, text="Python/React"), 
            Option(poll_id=new_poll.id, text="Go/Vue"),
            Option(poll_id=new_poll.id, text="Node/NextJS")
        ]
        db.add_all(opts)
        db.commit()
        
        print("✅ Successfully seeded the database with Poll and Options!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()