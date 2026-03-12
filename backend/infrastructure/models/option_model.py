from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from ..db.database import Base


class OptionModel(Base):

    __tablename__ = "options"

    id = Column(String, primary_key=True, index=True)
    poll_id = Column(String, ForeignKey("polls.id"), nullable=False)
    text = Column(String, nullable=False)
    # This allows an Option to know about its parent Poll
    poll = relationship("PollModel", back_populates="options")