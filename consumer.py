import json
from confluent_kafka import Consumer
import uuid
import logging
from db_utils import fetch_latest_processed_team_stats
from sort_utils import sort_by_avg_form_score, sort_teams_by_form_score

# Configure logging
logging.basicConfig(level=logging.INFO)

def consume_latest_processed_data(broker, topics, expected_messages=10):
    # Kafka consumer configuration
    consumer_conf = {
        'bootstrap.servers': broker,
        'group.id': f"streamlit-{uuid.uuid4()}",  # Unique group id for each session
        'auto.offset.reset': 'latest',            # Start from latest messages
        'enable.auto.commit': False               # Disable auto commit of offsets
    }

    consumer = Consumer(consumer_conf)
    consumer.subscribe(topics)  # Subscribe to the given topics

    messages = []

    try:
        # Poll messages until expected number is reached
        while len(messages) < expected_messages:
            msg = consumer.poll(1.0)  # Poll for a message (timeout 1s)
            if msg is None or msg.error():
                continue  # Skip if no message or error
            data = json.loads(msg.value().decode('utf-8'))  # Decode and parse JSON
            topic = msg.topic()
            
            if topic == "processed_team_stats":  
                messages.append(data)
            elif topic == "frontend_control":
                if data.get("type") == "no_items_scraped":
                    logging.info("No items scraped, stopping consumer and informing user.")
                    return []
    finally:
        consumer.close()  # Always close the consumer
    
    teams_sorted_by_form_score = sort_teams_by_form_score(messages)  # Sort teams by form score
    sorted_messages = sort_by_avg_form_score(teams_sorted_by_form_score)  # Sort by average form score
    return sorted_messages if sorted_messages else []  # Return the list of messages

def start_data():
    data = fetch_latest_processed_team_stats()
    teams_sorted_by_form_score = sort_teams_by_form_score(data)  # Sort teams by form score
    sorted_data = sort_by_avg_form_score(teams_sorted_by_form_score)  # Sort by average form score
    return sorted_data if sorted_data else []


