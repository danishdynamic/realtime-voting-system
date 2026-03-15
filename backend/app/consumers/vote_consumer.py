from kafka import KafkaConsumer
import json

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
