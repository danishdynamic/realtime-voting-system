import json
from kafka import KafkaConsumer
from flask_socketio import SocketIO
from backend.infrastructure.redis.redis_client import redis_client

# 1. Create a STANDALONE Emitter
# This bypasses the need for the Flask app instance.
# It sends the message to Redis, and your 'run.py' app picks it up.
emitter = SocketIO(message_queue='redis://localhost:6379/0')

# 2. Configure Kafka Consumer
consumer = KafkaConsumer(
    'vote_events',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='latest', # Changed to 'latest' to avoid processing old test crashes
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("🚀 Kafka Consumer is LIVE and listening on 'vote_events'...")

for message in consumer:
    vote_event = message.value
    print(f"📥 Kafka Received: {vote_event}")

    poll_id = vote_event.get("poll_id")
    option_text = vote_event.get("option_text")

    if poll_id and option_text:
        key = f"poll:{poll_id}"
        
        # 3. Increment Redis
        # This keeps the live counts stored in memory
        redis_client.hincrby(key, option_text, 1)

        # 4. Get updated totals for the chart
        raw_results = redis_client.hgetall(key) or {}
        # Ensure we decode bytes from Redis to strings/ints
        results = {k.decode('utf-8') if isinstance(k, bytes) else k: 
                   int(v) for k, v in raw_results.items()}

        # 5. Broadcast to React via the Emitter
        # We use the 'emitter' variable we created at the top
        print(f"📢 Emitting update to frontend for poll: {poll_id}")
        emitter.emit("vote_update", {
            "poll_id": poll_id, 
            "results": results
        }, namespace='/') 
        
        print(f"✅ Redis Updated & Socket Emitted: {results}")