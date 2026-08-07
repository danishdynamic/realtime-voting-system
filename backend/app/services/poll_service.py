# app/services/poll_service.py
from datetime import datetime, timezone
import uuid
from typing import List, Optional, Dict

from backend.app.domain.entities.poll import Poll
from backend.app.domain.entities.option import Option
from backend.app.repositories.poll_repository import PollRepository
from backend.infrastructure.redis.redis_client import redis_client

class PollService:
    
    def __init__(self, poll_repository: PollRepository):
        self.poll_repository = poll_repository

    def create_poll(
        self,
        question: str,
        options: List[str],
        created_by: str,
        start_time: datetime,
        end_time: datetime
    ) -> Poll:
    
        # Use UUID int IDs for internal entities and string public_id
        poll_id = uuid.uuid4().int
        public_id = str(uuid.uuid4())

        option_entities = []

        for text in options:
            option_entities.append(
                Option(
                    id=str(uuid.uuid4()),
                    poll_id=str(poll_id),
                    text=text
                )
            )

        poll = Poll(
            id=str(poll_id),
            public_id=public_id,
            question=question,
            created_by=created_by,
            options=option_entities,
            start_time=start_time,
            end_time=end_time,
            created_at=datetime.now(timezone.utc).replace(tzinfo=None)
        )

        self.poll_repository.save(poll)

        return poll

    def get_poll(self, public_id: str) -> Optional[Poll]:
        """Fetch a single poll by its public ID."""
        return self.poll_repository.get_by_public_id(public_id)

    def get_poll_with_status(self, public_id: str) -> Optional[Dict]:
        """
        Fetch poll with computed status and time remaining.
        Returns a dict ready for JSON serialization.
        """
        poll = self.poll_repository.get_by_public_id(public_id)
        if not poll:
            return None

        now = datetime.now(timezone.utc).replace(tzinfo=None)  # UTC now

        start = poll.start_time.replace(tzinfo=None) if poll.start_time.tzinfo else poll.start_time
        end = poll.end_time.replace(tzinfo=None) if poll.end_time.tzinfo else poll.end_time
        now = now.replace(tzinfo=None) if now.tzinfo else now
        
        # Determine status
        if now < start:
            status = "upcoming"
        elif start <= now <= end:
            status = "active"
        else:
            status = "ended"

        # Calculate time remaining (only for active polls)
        time_remaining = None
        if status == "active":
            diff = poll.end_time - now
            time_remaining = {
                "hours": diff.seconds // 3600,
                "minutes": (diff.seconds % 3600) // 60,
                "seconds": diff.seconds % 60,
                "total_seconds": int(diff.total_seconds())
            }

        return {
            "poll_id": poll.public_id,
            "question": poll.question,
            "options": [{"id": o.id, "text": o.text} for o in poll.options],
            "start_time": poll.start_time.isoformat() +"Z",
            "end_time": poll.end_time.isoformat() +"Z",
            "created_by": poll.created_by,
            "status": status,
            "time_remaining": time_remaining,
            "is_active": status == "active"
        }

    def list_active_polls(self) -> List[Poll]:
        """Return polls that are currently active (between start and end time)."""
        all_polls = self.poll_repository.list_all_polls()
        now = datetime.now(timezone.utc).replace(tzinfo=None)  # UTC now
        return [p for p in all_polls if p.start_time <= now <= p.end_time]

    def get_active_polls(self) -> List[Poll]:
        """Alias for list_active_polls."""
        return self.list_active_polls()

    def list_all_polls_with_status(self) -> List[Dict]:
        """
        Return ALL polls (not just active) with status for the table view.
        Needed so users can see upcoming and ended polls too.
        """
        all_polls = self.poll_repository.list_all_polls()
        now = datetime.now(timezone.utc).replace(tzinfo=None)  # UTC now
        result = []

        for poll in all_polls:

            key = f"poll:{poll.public_id}"
            redis_results = redis_client.hgetall(key) or {}
            total_votes = sum(int(v) for v in redis_results.values())

            if now < poll.start_time:
                status = "upcoming"
                time_until_start = poll.start_time - now
                badge_text = f"Starts in {self._format_duration(time_until_start)}"
            elif poll.start_time <= now <= poll.end_time:
                status = "active"
                time_until_end = poll.end_time - now
                badge_text = f"Ends in {self._format_duration(time_until_end)}"
            else:
                status = "ended"
                badge_text = "Closed"

            result.append({
                "poll_id": poll.public_id,
                "question": poll.question,
                "status": status,
                "badge_text": badge_text,
                "start_time": poll.start_time.isoformat(),
                "end_time": poll.end_time.isoformat(),
                "total_options": len(poll.options),
                "total_votes": total_votes
            })

        return result

    def _format_duration(self, duration) -> str:
        """Helper to format timedelta into human-readable string."""
        total_seconds = int(duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"