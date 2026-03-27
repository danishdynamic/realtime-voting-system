
from datetime import datetime
from ..domain.entities.vote import Vote
from ..repositories.poll_repository import PollRepository
from ..repositories.vote_repository import VoteRepository
from ..producers.vote_producer import VoteProducer
import uuid
from typing import Any

class Voteservice:
      
      def __init__(self, poll_repository: PollRepository, vote_repository: VoteRepository, vote_producer: VoteProducer):
          self.poll_repository = poll_repository
          self.vote_repository = vote_repository
          self.vote_producer = vote_producer


      def vote(self, poll_public_id: str, option_id: str, user_id: str, option_text: str) -> Vote:
        # 1. Fetch the poll using public_id
        poll = self.poll_repository.get_by_public_id(poll_public_id)
        if not poll:
            raise ValueError("Poll not found")

        if not poll.is_active():
            raise ValueError("Poll is not active")

        # 2. Match the option - Crucial for getting the correct DB ID
        # We try to find the option object by its ID or its text name
        selected_option = next(
            (o for o in poll.options if str(o.id) == str(option_id) or o.text == option_text), 
            None
        )

        # Fallback: if we didn't find the object but have the text, we use that for Kafka
        final_kafka_text = selected_option.text if selected_option else option_text

        if not final_kafka_text:
            raise ValueError("Option not found in the poll")

        # 3. Check for double voting
        if self.vote_repository.has_user_voted(poll_public_id, user_id):
            raise ValueError("User has already voted in this poll")

        # 4. Create and save the vote to SQLite
        # Use poll.id and selected_option.id (the DB Primary Keys) to avoid 'datatype mismatch'
        try:
           db_option_id = int(selected_option.id) if selected_option else int(option_id)
           db_poll_id = int(poll.id) if hasattr(poll, 'id') else int(poll_public_id)
        except ( ValueError, TypeError):
           db_option_id = selected_option.id if selected_option else option_id
           db_poll_id = poll.id if hasattr(poll, 'id') else poll_public_id

        vote_entry = Vote(
            poll_id=db_poll_id,
            option_id=db_option_id,
            user_id=str(user_id),
            created_at=datetime.now()
        )

        # Attempt to save to the database
        self.vote_repository.save(vote_entry)

        # 5. Send to Kafka - We use 'option_text' so Redis can update the chart easily
        self.vote_producer.send_vote({
            "poll_id": poll_public_id, 
            "option_text": final_kafka_text, 
            "user_id": user_id
        })

        return vote_entry