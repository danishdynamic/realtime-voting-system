from sqlalchemy.orm import Session
from ...backend.app.repositories.poll_repository import PollRepository
from ...backend.app.repositories.poll_repository import Poll
from ..models.poll_model import PollModel
from datetime import datetime



class SqlitePollRepository(PollRepository):

     def __init__(self, db: Session):
          self.db = db

    # implementing get_by_public_id() method from PollRepository interface

     def get_by_public_id(self, public_id:str):
          
          poll_model = (
               self.db.query(PollModel)
               .filter(PollModel.public_id == public_id)
               .first()
          )


          if not poll_model:
               return None
          
          return Poll(
                id=str(poll_model.id),
                public_id=str(poll_model.public_id),
                question=str(poll_model.question),
                created_by=str(poll_model.created_by),
                options=[],
                start_time=poll_model.start_time.isoformat(),
                end_time=poll_model.end_time.isoformat(),
                created_at=poll_model.created_at.isoformat()
                    )
     
    # implementing exists() method from PollRepository interface

     def exists(self, public_id: str) -> bool:
               poll = (
                 self.db.query(PollModel).filter(PollModel.public_id == public_id).first()
    )

               return poll is not None
     
     # implementing save() method from PollRepository interface

     def save(self, poll: Poll):

            poll_model = PollModel(
            id=poll.id,
            public_id=poll.public_id,
            question=poll.question,
            created_by=poll.created_by,
            start_time=poll.start_time,
            end_time=poll.end_time,
            created_at=poll.created_at
            )

            self.db.add(poll_model)
            self.db.commit()

    # implementing list_active_polls() method from PollRepository interface

     def list_active_polls(self):

            now = datetime.now()

            polls = (
                self.db.query(PollModel)
                .filter(PollModel.start_time <= now)
                .filter(PollModel.end_time >= now)
                .all()
            )

            return [
                Poll(
                    id=str(p.id),
                    public_id=str(p.public_id),
                    question=str(p.question),
                    created_by=str(p.created_by),
                    options=[],
                    start_time=p.start_time.isoformat(),
                    end_time=p.end_time.isoformat(),
                    created_at=p.created_at.isoformat()
                )
                for p in polls
            ]