# app/producers/vote_producer.py
from kafka import KafkaProducer
import json

class VoteProducer():
    
    # Initialize the Kafka producer, this connects to the Kafka broker and sets up the serializer for the messages
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers='localhost:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    # this method send vote events to the Kafka topic 'vote_events'
    def publish_vote(self, event:dict):
        self.producer.send('vote_events', event)
        self.producer.flush()  # Ensure the message is sent immediately

    def send_vote(self, vote_data:dict):
        '''Send a vote message to the message broker (kafka)'''
        self.producer.send('vote_events', vote_data)
        self.producer.flush() 
        print(f"DEBUG: Sent vote to Kafka: {vote_data}")