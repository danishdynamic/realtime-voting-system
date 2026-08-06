from abc import ABC, abstractmethod
from typing import List, Optional
from ..domain.entities.vote import Vote

class VoteRepository(ABC):

    @abstractmethod
    def save(self, vote: Vote) -> None:
        """Persist a vote."""
        pass

    @abstractmethod
    def has_user_voted(self, poll_public_id: str, user_id: str) -> bool:  
        """
        Check if a user has already voted in a poll.
        poll_public_id is the UUID string (e.g., "test-poll-1").
        """
        pass

    @abstractmethod
    def get_votes_by_poll(self, poll_public_id: str) -> List[Vote]:  
        """Retrieve all votes for a poll."""
        pass

    @abstractmethod
    def get_user_vote(self, poll_public_id: str, user_id: str) -> Optional[Vote]:  
        """Get a specific user's vote in a specific poll."""
        pass