"""
User vote request
      │
      ▼
VoteService.vote()
      │
      ├── PollRepository.get_by_public_id()
      ├── poll.is_active()
      ├── poll.has_option()
      ├── VoteRepository.has_user_voted()
      └── VoteRepository.save()
"""

from datetime import datetime
from ..domain.entities.vote import Vote
from ..repositories.poll_repository import PollRepository
from ..repositories.vote_repository import VoteRepository
from ..producers.vote_producer import VoteProducer

class Voteservice:
      
      def __init__(self, poll_repository: PollRepository, vote_repository: VoteRepository, vote_producer: VoteProducer):
          self.poll_repository = poll_repository
          self.vote_repository = vote_repository
          self.vote_producer = vote_producer


      def vote(self, poll_public_id: str, option_id: str, user_id: str) -> Vote:
           
            poll = self.poll_repository.get_by_public_id(poll_public_id)
            if not poll:
                raise ValueError("Poll not found")

            if not poll.is_active():
                raise ValueError("Poll is not active")

            if not poll.has_option(option_id):
                raise ValueError("Option not found in the poll")

            if self.vote_repository.has_user_voted(poll_public_id, user_id):
                raise ValueError("User has already voted in this poll")

            vote = Vote(
                id="generated_vote_id",
                poll_id=poll_public_id,
                option_id=option_id,
                user_id=user_id,
                created_at=datetime.now()
            )

            self.vote_repository.save(vote)
            self.vote_producer.send_vote({"poll_id": poll_public_id, "option_id": option_id})
            return vote