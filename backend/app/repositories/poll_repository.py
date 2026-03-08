from abc import ABC, abstractmethod
from ..domain.entities.poll import Poll
from typing import Optional, List


class PollRepository(ABC):

    @abstractmethod
    def get_by_public_id(self, public_id:str) -> Optional[Poll]:
        # -> either get a Poll object or None.
        """Retreive a poll using its public ID"""
        pass

    @abstractmethod
    def save(self, poll:Poll)-> None:
        """Persist a poll."""
        pass
    
    @abstractmethod
    def list_active_polls(self) -> List[Poll]:
        """Return all currently active polls."""
        pass
    
    @abstractmethod
    def exists(self, public_id: str) -> bool:
        """Check if a poll exists."""
        pass


    