import json
from confluent_kafka import Consumer
import uuid

def consume_latest_processed_data(broker, topic, min_messages=1, idle_timeout=30.0):
    from time import time

    # These settings makes the consumer only read messages that are produced after the consumer starts
    consumer_conf = { 
        'bootstrap.servers': broker,
        'group.id': f"streamlit-{uuid.uuid4()}",  # Use a unique group ID for each consumer instance
        'auto.offset.reset': 'latest',
        'enable.auto.commit': False
    }
    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])

    messages = []
    last_received = time()

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                # If we’ve already received enough, and idle long enough, break
                if len(messages) >= min_messages and (time() - last_received > idle_timeout):
                    break
                continue
            if msg.error():
                continue

            data = json.loads(msg.value().decode('utf-8'))
            messages.append(data)
            last_received = time()  # reset timeout
    finally:
        consumer.close()

    return messages

