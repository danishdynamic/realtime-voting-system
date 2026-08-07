# infrastructure/repositories/sqlite_poll_repository.py

from sqlalchemy.orm import Session, joinedload 
from backend.app.repositories.poll_repository import PollRepository
from backend.app.repositories.vote_repository import VoteRepository
from backend.infrastructure.models.poll_model import PollModel
from datetime import datetime
from backend.app.domain.entities.poll import Poll
from backend.infrastructure.models.option_model import OptionModel
from backend.app.domain.entities.option import Option
from typing import List

class SqlitePollRepository(PollRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_public_id(self, public_id: str):
        # Using joinedload here too for efficiency
        poll_model = (
            self.db.query(PollModel)
            .options(joinedload(PollModel.options))
            .filter(PollModel.public_id == public_id)
            .first()
        )

        if not poll_model:
            return None
        
        options = [
            Option(id=str(o.id), poll_id=str(o.poll_id), text=o.text)
            for o in poll_model.options
        ]

        try:
            return Poll(
                id=str(poll_model.id),
                public_id=str(poll_model.public_id),
                question=str(poll_model.question),
                created_by=str(poll_model.created_by),
                options=options,
                start_time=poll_model.start_time,
                end_time=poll_model.end_time,
                created_at=poll_model.created_at
            )
        except ValueError as e:
                print(f"Error converting poll_model to Poll: {e}")
                return None

    def list_active_polls(self) -> List[Poll]:
        now = datetime.now()

        # Eager load options to avoid N+1 problem
        polls = (
            self.db.query(PollModel)
            .options(joinedload(PollModel.options))
            .filter(PollModel.start_time <= now)
            .filter(PollModel.end_time >= now)
            .all()
        )

        result = []
        for p in polls:
            # Map DB options to Domain options
            domain_options = [
                Option(id=str(o.id), poll_id=str(o.poll_id), text=o.text)
                for o in p.options
            ]

            # Append to list INSIDE the loop
            #result.append(
            try:
                valid_poll =Poll(
                        id=str(p.id),
                        public_id=str(p.public_id),
                        question=str(p.question),
                        created_by=str(p.created_by),
                        options=domain_options,
                        start_time=p.start_time,
                        end_time=p.end_time,
                        created_at=p.created_at
                    )
                result.append(valid_poll)
            except ValueError as e:
                print(f"Error converting poll_model to Poll:{p.id} : {e}")

        # Return OUTSIDE the loop
        return result


    def list_all_polls(self) -> List[Poll]:
        """Return all polls regardless of status, ordered by newest first."""
        poll_models = self.db.query(PollModel).order_by(PollModel.created_at.desc()).all()
        return [self._to_entity(m) for m in poll_models]

    def _to_entity(self, model: PollModel) -> Poll:
        """Helper to convert SQLAlchemy model to domain entity."""
        return Poll(
            id=str(model.id),
            public_id = model.public_id,
            question = model.question,
            created_by = model.created_by,
            options=[
                Option(
                    id=str(o.id),
                    poll_id=str(o.poll_id),
                    text=o.text
                ) for o in model.options
            ],
            start_time = model.start_time,  
            end_time = model.end_time,       
            created_at = model.created_at
        )
    

    # implenting save() method from PollRepository interface

    def save(self, poll: Poll):
        poll_model = PollModel(
            # id=poll.id,
            public_id=poll.public_id,
            question=poll.question,
            created_by=poll.created_by,
            start_time=poll.start_time,
            end_time=poll.end_time,
            created_at=poll.created_at
        )
        self.db.add(poll_model)
        self.db.flush()

        for option in poll.options:
            option_model = OptionModel(
                # id=option.id,
                poll_id=poll_model.id,
                text=option.text
            )
            self.db.add(option_model)
            
            
        self.db.commit()

    # implementing exists() method from PollRepository interface
    def exists(self, public_id: str) -> bool:
        poll = (
            self.db.query(PollModel)
            .filter(PollModel.public_id == public_id)
            .first()
        )
        return poll is not None