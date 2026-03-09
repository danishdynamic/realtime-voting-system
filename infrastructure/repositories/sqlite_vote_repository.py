from sqlalchemy.orm import Session
from typing import List

from ...backend.app.repositories.vote_repository import VoteRepository
from ...backend.app.repositories.vote_repository import Vote

from ..models.vote_model import VoteModel


class SQLiteVoteRepository(VoteRepository):

    def __init__(self, db: Session):
        self.db = db