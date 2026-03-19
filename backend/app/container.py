
from backend.infrastructure.db.database import SessionLocal

from backend.infrastructure.repositories.sqlite_poll_repository import SqlitePollRepository
from backend.infrastructure.repositories.sqlite_vote_repository import SQLiteVoteRepository

from backend.app.services.vote_service import Voteservice

from backend.app.services.poll_service import PollService

from backend.app.producers.vote_producer import VoteProducer



def get_vote_service():

    db = SessionLocal()

    poll_repo = SqlitePollRepository(db)
    vote_repo = SQLiteVoteRepository(db)

    vote_producer = VoteProducer()

    vote_service = Voteservice(poll_repo, vote_repo, vote_producer)
    
    return vote_service


def get_poll_service():

    db = SessionLocal()

    poll_repo = SqlitePollRepository(db)

    return PollService(poll_repo)

