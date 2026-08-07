# infrastructure/db/init_db.py
from .database import engine, Base

# Import models so SQLAlchemy knows about them
from ..models.poll_model import PollModel
from ..models.option_model import OptionModel
from ..models.vote_model import VoteModel


def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()