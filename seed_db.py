
from backend.infrastructure.db.database import SessionLocal, engine, Base # Adjust based on your init
from backend.infrastructure.models.option_model import OptionModel as Option
from backend.infrastructure.models.poll_model import PollModel as Poll
from datetime import datetime, timedelta


def seed():
    # 1. Create the tables first
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # 2. Check if the poll already exists to avoid duplicates
        existing_poll = db.query(Poll).filter_by(public_id="test-poll-1").first()
        if not existing_poll:
            new_poll = Poll(public_id="test-poll-1", question="Favorite Stack?", 
                            created_by = 'admin', created_at = datetime.now(), start_time = datetime.now(), end_time= datetime.now() + timedelta(days=7))
            db.add(new_poll)
            db.commit()
            
            # 3. Add options
            opts = [Option(poll_id=new_poll.id, text="Python/React"), 
                    Option(poll_id=new_poll.id, text="Go/Vue")]
            db.add_all(opts)
            db.commit()
            print("✅ Successfully seeded the database!")
        else:
            print("⚠️ Poll already exists.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()

