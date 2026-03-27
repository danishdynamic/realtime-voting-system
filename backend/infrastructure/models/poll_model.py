from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from ..db.database import Base

class PollModel(Base):

    __tablename__ = "polls"

    id = Column(Integer , primary_key=True, index=True, autoincrement= True)
    public_id = Column(String, unique=True, index=True, nullable=False)
    question = Column(String, nullable=False)
    created_by = Column(String, nullable=False)

    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    created_at = Column(DateTime, nullable=False)
    options = relationship("OptionModel", back_populates="poll", cascade="all, delete-orphan")