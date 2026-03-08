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

class Voteservice:
      
      def __init__(self, poll_repository: PollRepository, vote_repository: VoteRepository):
          self.poll_repository = poll_repository
          self.vote_repository = vote_repository


      def vote(self):
           pass