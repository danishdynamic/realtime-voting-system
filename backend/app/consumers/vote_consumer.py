# app/consumers/vote_consumer.py
import json
import asyncio
import inspect
from kafka import KafkaConsumer
from flask_socketio import SocketIO
from backend.infrastructure.redis.redis_client import redis_client

# 1. Create a STANDALONE Emitter
emitter = SocketIO(message_queue='redis://localhost:6379/0')

# 2. Configure Kafka Consumer
consumer = KafkaConsumer(
    'vote_events',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='latest',
    # guard against None values from Kafka; return None if message value is None
    value_deserializer=lambda m: json.loads(m.decode('utf-8')) if m is not None else None
)

print("🚀 Kafka Consumer is LIVE and listening on 'vote_events'...")

for message in consumer:
    vote_event = message.value
    if vote_event is None:
        print("⚠️ Skipping empty Kafka message (None value)")
        continue
    print(f"📥 Kafka Received: {vote_event}")

    poll_id = vote_event.get("poll_id")
    option_text = vote_event.get("option_text")
    user_id = vote_event.get("user_id")
    event_id = vote_event.get("event_id")

    if not poll_id or not option_text:
        print("⚠️ Skipping invalid event: missing poll_id or option_text")
        continue

    # 3. Deduplication: Only process this event once
    # Use event_id if present, otherwise construct from payload
    dedup_key = f"dedup:{event_id}" if event_id else f"dedup:{poll_id}:{user_id}:{option_text}"
    
    # SETNX returns True only if key didn't exist
    is_new = redis_client.set(dedup_key, "1", nx=True, ex=3600)  # 1 hour dedup window
    
    if not is_new:
        print(f"🔄 Duplicate event ignored: {dedup_key}")
        continue

    key = f"poll:{poll_id}"
    
    # 4. Increment Redis (safe now — deduped)
    redis_client.hincrby(key, option_text, 1)

    # 5. Get updated totals for the chart
    raw_results = redis_client.hgetall(key)
    # If redis client is async, hgetall may return an awaitable — handle both sync/async
    
    raw_results = raw_results or {}
    results = {k.decode('utf-8') if isinstance(k, bytes) else k: int(v) for k, v in raw_results.items()}

    # 6. Broadcast to React via the Emitter
    print(f"📢 Emitting update to frontend for poll: {poll_id}")
    emitter.emit("vote_update", {
        "poll_id": poll_id, 
        "results": results
    }, namespace='/') 
    
    print(f"✅ Redis Updated & Socket Emitted: {results}")