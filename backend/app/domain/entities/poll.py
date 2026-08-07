# app/domain/entities/poll.py

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List
from .option import Option


@dataclass
class Poll:
    id: str
    public_id: str
    question: str
    created_by: str
    options: List[Option]
    start_time: datetime
    end_time: datetime
    created_at: datetime

    def __post_init__(self):
        if len(self.options) < 2:
            raise ValueError("A poll must have at least two options.")
        if not self.question.strip():
            raise ValueError("Poll question cannot be empty")
        if self.start_time >= self.end_time:
            raise ValueError("Start time must be before end time.")

    def is_active(self) -> bool:
        """Check if the poll is currently active."""
        now = datetime.now(timezone.utc).replace(tzinfo=None)  # ← UTC now, not local
        start = self.start_time.replace(tzinfo=None) if self.start_time.tzinfo else self.start_time
        end = self.end_time.replace(tzinfo=None) if self.end_time.tzinfo else self.end_time
        return start <= now <= end

    def has_option(self, option_id: str) -> bool:
        for options in self.options:
            if options.id == option_id:
                return True
        return False
