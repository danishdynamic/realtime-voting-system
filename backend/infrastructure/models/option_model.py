from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..db.database import Base


class OptionModel(Base):

    __tablename__ = "options"

    id = Column(Integer, primary_key=True, index=True, autoincrement= True)
    poll_id = Column(Integer, ForeignKey("polls.id"), nullable=False)
    text = Column(String, nullable=False)
    # This allows an Option to know about its parent Poll
    poll = relationship("PollModel", back_populates="options")