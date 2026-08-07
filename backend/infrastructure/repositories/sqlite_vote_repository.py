# infrastructure/repositories/sqlite_vote_repository.py

from sqlalchemy.orm import Session
from typing import List, Optional, cast
from datetime import datetime

from backend.app.repositories.vote_repository import VoteRepository
from backend.app.domain.entities.vote import Vote
from backend.infrastructure.models.vote_model import VoteModel
from backend.infrastructure.models.poll_model import PollModel 
from sqlalchemy.exc import SQLAlchemyError


class SQLiteVoteRepository(VoteRepository):

    def __init__(self, db: Session):
        self.db = db

    def save(self, vote: Vote) -> None:
        try: 
            vote_model = VoteModel(
                id=vote.id,
                poll_id=vote.poll_id, 
                option_id=vote.option_id,
                user_id=vote.user_id,
                created_at=vote.created_at
            )
            self.db.add(vote_model)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"Database error: {e}")
            raise e

    def has_user_voted(self, poll_public_id: str, user_id: str) -> bool:
        """
        Check if user voted in a specific poll by joining VoteModel with PollModel.
        This correctly matches poll_public_id (UUID string) against the poll's public_id.
        """
        vote = (
            self.db.query(VoteModel)
            .join(PollModel, VoteModel.poll_id == PollModel.id)  
            .filter(PollModel.public_id == poll_public_id)       
            .filter(VoteModel.user_id == user_id)
            .first()
        )
        return vote is not None

    def get_votes_by_poll(self, poll_public_id: str) -> List[Vote]:
        """
        Get all votes for a poll by public_id.
        """
        vote_models = (
            self.db.query(VoteModel)
            .join(PollModel, VoteModel.poll_id == PollModel.id)
            .filter(PollModel.public_id == poll_public_id)
            .all()
        )

        return [
            Vote(
                id=str(v.id),
                poll_id=str(v.poll_id),
                option_id=str(v.option_id),
                user_id=str(v.user_id),
                created_at=cast(datetime, v.created_at)
            )
            for v in vote_models
        ]

    def get_user_vote(self, poll_public_id: str, user_id: str) -> Optional[Vote]:
        """
        Return the specific vote a user cast in a specific poll.
        """
        vote_model = (
            self.db.query(VoteModel)
            .join(PollModel, VoteModel.poll_id == PollModel.id)
            .filter(PollModel.public_id == poll_public_id)
            .filter(VoteModel.user_id == user_id)
            .first()
        )
        
        if vote_model:
            return Vote(
                id=str(vote_model.id),
                poll_id=str(vote_model.poll_id),
                option_id=str(vote_model.option_id),
                user_id=str(vote_model.user_id),
                created_at=cast(datetime, vote_model.created_at)
            )
        return None