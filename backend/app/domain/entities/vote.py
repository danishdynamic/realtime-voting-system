from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

@dataclass
class Vote:
    poll_id: Any  # Changed to Any to allow int or str
    option_id: Any # Changed to Any to allow int or str
    user_id: str
    created_at: Optional[datetime] = None
    id: Optional[Any] = None  # id is now optional and can be any type

    def __post_init__(self):
        # We use str() here so .strip() doesn't crash if we pass an int
        if self.id is not None and not str(self.id).strip():
            raise ValueError("Vote Id cannot be empty")

        if not str(self.poll_id).strip():
            raise ValueError("Poll Id cannot be empty")
        
        if not str(self.option_id).strip():
            raise ValueError("Option Id cannot be empty")
        
        if not self.user_id.strip():
            raise ValueError("User Id cannot be empty")