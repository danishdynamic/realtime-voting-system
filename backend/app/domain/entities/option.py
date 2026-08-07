# app/domain/entities/option.py
from dataclasses import dataclass

#Define dataclass for Option entity
@dataclass
class Option:
    id: str
    poll_id: str
    text: str

    def __post_init__(self):
        # Validate that the option text is not empty
        if not self.text.strip():
            raise ValueError("Option text cannot be empty.")
        

