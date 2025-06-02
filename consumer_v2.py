import json
from confluent_kafka import Consumer
import uuid
import mysql.connector
from time import time

# _functions are private functions that are not intended to be used outside this module.

def _sort_by_avg_form_score(data):
    return sorted(data, key=lambda x: x['team_stats']['avg_form_score'], reverse=False)

def _sort_teams_players_by_form_score(data):
    for team in data:
        team['batters'] = sorted(team['batters'], key=lambda x: x['form_score'], reverse=True)
        team['pitchers'] = sorted(team['pitchers'], key=lambda x: x['form_score'], reverse=True)
    return data

def _get_from_MariaDB(db_config):
    connexion = mysql.connector.connect(**db_config)
    '''
        db_config should be a dictionary with the following keys:
        - host: Database host
        - user: Database user
        - password: Database password
        - database: Database name
    '''
    command = "SELECT snapshot FROM processed_team_stats "
    cursor = connexion.cursor()
    cursor.execute(command) 
    rows = cursor.fetchall() # fetch all rows from the executed query
    data= []
    for row in rows:
        data.append(json.loads(row))  # Assuming snapshot is stored as JSON string
    cursor.close()
    connexion.close()
    return rows

def consume_latest_processed_data(broker, topic, db_config, min_messages=1, idle_timeout=30.0):

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

    return _sort_teams_players_by_form_score(_sort_by_avg_form_score(messages))

def start_data(db_config):
    """
    Usage : On the start of the application, this function will be called to retrieve the latest processed data from MariaDB.

    Start the data retrieval process from MariaDB and Kafka.
    
    Args:
        db_config (dict): Configuration for connecting to the MariaDB database.
        The dictionary should contain:
        - host: Database host
        - user: Database user
        - password: Database password
        - database: Database name
        
    Returns:
        list: A list of formatted data retrieved from the database.
    """
    # Retrieve data from MariaDB
    raw_data = _get_from_MariaDB(db_config)
    
    return _sort_teams_players_by_form_score(_sort_by_avg_form_score(raw_data))
