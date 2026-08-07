# infrastructure/models/vote_model.py
from sqlalchemy import Column, ForeignKey, String, DateTime, Integer
from ..db.database import Base
from datetime import datetime


class VoteModel(Base):

    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True, autoincrement= True)
    poll_id = Column(Integer, ForeignKey("polls.id"), nullable=False)
    option_id = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    created_at = Column(DateTime, default= datetime.now , nullable=False)