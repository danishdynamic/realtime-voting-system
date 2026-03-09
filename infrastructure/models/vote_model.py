from sqlalchemy import Column, String, DateTime
from ..db.database import Base


class VoteModel(Base):

    __tablename__ = "votes"

    id = Column(String, primary_key=True, index=True)
    poll_id = Column(String, nullable=False)
    option_id = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)