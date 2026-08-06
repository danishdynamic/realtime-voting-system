from datetime import datetime
from ..domain.entities.vote import Vote
from ..repositories.poll_repository import PollRepository
from ..repositories.vote_repository import VoteRepository
from ..producers.vote_producer import VoteProducer
from backend.infrastructure.redis.redis_client import redis_client
import uuid
from typing import Any


class VoteService:
      
    def __init__(self, poll_repository: PollRepository, vote_repository: VoteRepository, vote_producer: VoteProducer):
        self.poll_repository = poll_repository
        self.vote_repository = vote_repository
        self.vote_producer = vote_producer


    def vote(self, poll_public_id: str, option_id: str, user_id: str, option_text: str) -> Vote:
        # 1. Fetch the poll using public_id
        poll = self.poll_repository.get_by_public_id(poll_public_id)
        if not poll:
            raise ValueError("Poll not found")

        if not poll.is_active():
            raise ValueError("Poll is not active")

        # 2. Match the option - Crucial for getting the correct DB ID
        selected_option = next(
            (o for o in poll.options if str(o.id) == str(option_id) or o.text == option_text), 
            None
        )

        final_kafka_text = selected_option.text if selected_option else option_text

        if not final_kafka_text:
            raise ValueError("Option not found in the poll")

        # 3. ATOMIC check using Redis SETNX — prevents race condition
        # This is the single source of truth for "has this user voted?"
        user_vote_key = f"user_vote:{poll_public_id}:{user_id}"
        was_set = redis_client.set(user_vote_key, final_kafka_text, nx=True, ex=86400)  # 24h expiry

        if not was_set:
            raise ValueError("User has already voted in this poll")

        # 4. Create and save the vote to SQLite
        try:
            db_option_id = int(selected_option.id) if selected_option else int(option_id)
            db_poll_id = int(poll.id) if hasattr(poll, 'id') else int(poll_public_id)
        except (ValueError, TypeError):
            db_option_id = selected_option.id if selected_option else option_id
            db_poll_id = poll.id if hasattr(poll, 'id') else poll_public_id

        vote_entry = Vote(
            poll_id=db_poll_id,
            option_id=db_option_id,
            user_id=str(user_id),
            created_at=datetime.now()
        )

        # 5. Save to database — if this fails, we MUST rollback Redis
        try:
            self.vote_repository.save(vote_entry)
        except Exception as e:
            # CRITICAL: Rollback Redis lock so user can retry
            redis_client.delete(user_vote_key)
            raise ValueError(f"Failed to save vote: {str(e)}")

        # 6. Send to Kafka — include event_id for consumer deduplication
        try:
            self.vote_producer.send_vote({
                "poll_id": poll_public_id, 
                "option_text": final_kafka_text, 
                "user_id": user_id,
                "event_id": f"{poll_public_id}:{user_id}:{datetime.now().isoformat()}"
            })
        except Exception as e:
            # If Kafka fails, we keep the DB vote but log the error
            # The vote is valid, just real-time update may lag
            print(f"Warning: Kafka publish failed: {e}")

        return vote_entry