from datetime import datetime
import uuid
from typing import List

from app.domain.entities.poll import Poll
from app.domain.entities.option import Option
from app.repositories.poll_repository import PollRepository

class PollService:
    
    def __init__(self,poll_repository: PollRepository):
        self.poll_repository = poll_repository

    # this service will handle create, get and list active polls

    # Creating a poll method

    def create_poll(
        self,
        question: str,
        options: List[str],
        created_by: str,
        start_time: datetime,
        end_time: datetime ) -> Poll:

    
        poll_id = str(uuid.uuid4())
        public_id = str(uuid.uuid4())

        option_entities = []


        for test in options:
            option_entities.append(
                Option(
                    id = str(uuid.uuid4()),
                    poll_id = poll_id,
                    text = text
                )
            )


        poll = Poll(
            id=poll_id,
            public_id=public_id,
            question=question,
            created_by=created_by,
            options=option_entities,
            start_time=start_time,
            end_time=end_time,
            created_at=datetime.now()
        )

        self.poll_repository.save(poll)

        return poll
    
    #Creating a get poll method 

    def get_poll(self, public_id : str):

        return self.poll_repository.get_by_public_id(public_id)
    
    #Creating list active polls method

    def list_active_polls(self):

        return self.poll_repository.list_active_polls()
    




   
            
