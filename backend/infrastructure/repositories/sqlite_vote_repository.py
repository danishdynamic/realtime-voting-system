from sqlalchemy.orm import Session
from typing import List

from backend.app.repositories.vote_repository import VoteRepository
from backend.app.repositories.vote_repository import Vote

from ..models.vote_model import VoteModel
from sqlalchemy.exc import SQLAlchemyError


class SQLiteVoteRepository(VoteRepository):

    def __init__(self, db: Session):
        self.db = db

    # implementing save() method from VoteRepository interface

    def save(self, vote: Vote) -> None:
        try: 
            vote_model = VoteModel(
                id = vote.id,
                poll_id = vote.poll_id, 
                option_id = vote.option_id,
                user_id = vote.user_id,
                created_at = vote.created_at
            )

            self.db.add(vote_model)
            self.db.commit()

        except SQLAlchemyError as e:
            #if anything fails undo the staging area
            self.db.rollback()
            print ("Database error: {e}")
            # raise the error to caller knows it failed 
            raise e

            

    # implementing has_user_voted() method from VoteRepository interface

    def has_user_voted(self, poll_id: str, user_id: str) -> bool:

        vote = ( 
            self.db.query(VoteModel)
            .filter(VoteModel.poll_id == poll_id, VoteModel.user_id == user_id)
            .first()
            )
        return vote is not None 
    
    # implementing get_votes_by_poll() method from VoteRepository interface

    def get_votes_by_poll(self, poll_id : str) -> List[Vote]:

        vote_models = (
        self.db.query(VoteModel)
        .filter(VoteModel.poll_id == poll_id)
        .all()
          )

        votes = []

        for v in vote_models:
           votes.append(
              Vote(
                id=str(v.id),
                poll_id=str(v.poll_id),
                option_id=str(v.option_id),
                user_id=str(v.user_id),
                created_at=v.created_at
                )
            )

        return votes