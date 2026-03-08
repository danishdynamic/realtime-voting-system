from abc import ABC, abstractmethod
from typing import List
from ..domain.entities.vote import Vote


class VoteRepository(ABC):

    @abstractmethod
    def save(self, vote: Vote) -> None:
        """Persist a vote."""
        pass


    @abstractmethod
    def has_user_voted(self, poll_id: str, user_id: str) -> bool:
        """
        Check if a user has already voted in a poll.
        Used to enforce one vote per user.
        """
        pass


    @abstractmethod
    def get_votes_by_poll(self, poll_id: str) -> List[Vote]:
        """Retrieve all votes for a poll."""
        pass