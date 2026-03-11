
from infrastructure.db.database import SessionLocal

from infrastructure.repositories.sqlite_poll_repository import SqlitePollRepository
from infrastructure.repositories.sqlite_vote_repository import SQLiteVoteRepository

from app.services.vote_service import Voteservice

from app.services.poll_service import PollService



def get_vote_service():

    db = SessionLocal()

    poll_repo = SqlitePollRepository(db)
    vote_repo = SQLiteVoteRepository(db)

    vote_service = Voteservice(poll_repo, vote_repo)
    return vote_service


def get_poll_service():

    db = SessionLocal()

    poll_repo = SqlitePollRepository(db)

    return PollService(poll_repo)