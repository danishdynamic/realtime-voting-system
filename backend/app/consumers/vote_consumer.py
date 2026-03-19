from kafka import KafkaConsumer
import json
from backend.infrastructure.redis.redis_client import redis_client
from backend.app.api.app import socketio_instance

# Initialize the Kafka consumer, this connects to the Kafka broker and sets up the deserializer for the messages

consumer = KafkaConsumer(
    "votes",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

print("Kafka vote consumer started...")

# Listen for messages on the "votes" topic and print them as they arrive
# value is the deserialized message content, which should be a dictionary representing the vote event

for message in consumer:
    vote_event = message.value
    print("Vote received:", vote_event)

    poll_id = vote_event["poll_id"]
    option_id = vote_event["option_id"]

    key = f"poll:{poll_id}"

    redis_client.hincrby(key, option_id, 1)

    results = redis_client.hgetall(key) or {}
    results = {k.decode() if isinstance(k, bytes) else k: int(v) for k, v in results.items()}


    socketio_instance.emit("vote_update", {"poll_id": poll_id, "results": results})