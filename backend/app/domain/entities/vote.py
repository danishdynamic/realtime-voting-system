from dataclasses import dataclass
from datetime import datetime

#Define dataclass for voe entitiy 

@dataclass
class Vote:
    id : str
    poll_id: str
    option_id: str
    user_id: str
    created_at: datetime

    def __post_init__(self):
        
        if not self.id.strip():
            raise ValueError("Vote Id cannot be empty")

        if not self.poll_id.strip():
            raise ValueError ("Poll Id cannot be empty")
        
        if not self.option_id.strip():
            raise ValueError("Option Id cannot be empty")
        
        if not self.user_id.strip():
            raise ValueError("User Id cannot be empty")
        

