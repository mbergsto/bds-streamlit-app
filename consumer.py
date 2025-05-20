import json
from confluent_kafka import Consumer

def consume_latest_processed_data(broker, topic, max_messages=20):
    consumer_conf = {
        'bootstrap.servers': broker,
        'group.id': 'streamlit-consumer-group',
        'auto.offset.reset': 'latest'
    }
    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])

    messages = []
    try:
        while len(messages) < max_messages:
            msg = consumer.poll(1.0)
            if msg is None:
                break
            if msg.error():
                continue
            data = json.loads(msg.value().decode('utf-8'))
            messages.append(data)
    finally:
        consumer.close()
    return messages
