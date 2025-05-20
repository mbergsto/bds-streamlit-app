from confluent_kafka import Producer

def send_trigger(broker, topic="trigger_scrape"):
    producer = Producer({'bootstrap.servers': broker})
    producer.produce(topic, key="trigger", value="scrape_now")
    producer.flush()