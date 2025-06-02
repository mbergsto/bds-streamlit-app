import json
from confluent_kafka import Consumer
import uuid

def consume_latest_processed_data(broker, topic, expected_messages=10):
    # Kafka consumer configuration
    consumer_conf = {
        'bootstrap.servers': broker,
        'group.id': f"streamlit-{uuid.uuid4()}",  # Unique group id for each session
        'auto.offset.reset': 'latest',            # Start from latest messages
        'enable.auto.commit': False               # Disable auto commit of offsets
    }

    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])  # Subscribe to the given topic

    messages = []

    try:
        # Poll messages until expected number is reached
        while len(messages) < expected_messages:
            msg = consumer.poll(1.0)  # Poll for a message (timeout 1s)
            if msg is None or msg.error():
                continue  # Skip if no message or error
            data = json.loads(msg.value().decode('utf-8'))  # Decode and parse JSON
            messages.append(data)
    finally:
        consumer.close()  # Always close the consumer

    return messages  # Return the list of messages
