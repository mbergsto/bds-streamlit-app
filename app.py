import streamlit as st
# from mock_consumer import mock_consume_latest_processed_data
from consumer import consume_latest_processed_data, start_data
from producer import send_trigger
import pandas as pd
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Page configuration
st.set_page_config(
    page_title="⚾ KBO Team Stats Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants from environment
BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVER")
KAFKA_TOPIC_IN_DATA = os.getenv("KAFKA_TOPIC_IN_DATA", "processed_team_stats")
KAFKA_TOPIC_IN_CONTROL = os.getenv("KAFKA_TOPIC_IN_CONTROL", "frontend_control")
KAFKA_TOPIC_OUT = os.getenv("KAFKA_TOPIC_OUT", "trigger_scrape")

# Title
st.title("⚾ KBO Team Stats Dashboard")

# Trigger Panel
st.sidebar.header("Controls") 

@st.cache_data
def load_data():
    logging.info("Loading data from database via fetch_latest_processed_team_stats...")
    data = start_data()
    logging.info(f"Fetched {len(data) if data else 0} records from database.")
    return data

data = load_data()

if st.sidebar.button("🔄 Update Stats via Scraper"):
    send_trigger(BROKER, KAFKA_TOPIC_OUT)
    with st.spinner("Trigger sent. Waiting for processed data from Kafka..."):
        new_data = consume_latest_processed_data(
            broker=BROKER,
            topics=[KAFKA_TOPIC_IN_DATA, KAFKA_TOPIC_IN_CONTROL],
        )

    if new_data:
        data = new_data
        st.success(f"✅ Received {len(data)} team records from Kafka!")
    else:
        st.warning("⚠️ No new data received from Kafka. Displaying existing data.")

if data:
    st.success(f"✅ Displaying {len(data)} team records.")
    team_names = [team["team_name"] for team in data]
    selected = st.sidebar.multiselect("Filter Teams:", team_names, default=team_names)

    for team in data:
        if team["team_name"] not in selected:
            continue

        with st.expander(f"{team['team_name']} Dashboard", expanded=True):
            stats = team['team_stats']
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Wins", stats['wins'])
            col2.metric("Losses", stats['losses'])
            col3.metric("Draws", stats['draws'])
            col4.metric("Score Diff", stats['score_difference'])

            tab_form, tab_batters, tab_pitchers = st.tabs(["Team Form", "Batters", "Pitchers"])
            tab_form.metric("Avg Form Score", team['team_form_score'])

            batters_df = pd.DataFrame(team['batters'])
            if not batters_df.empty:
                batters_df.set_index('player_name', inplace=True)
                tab_batters.table(batters_df)
            else:
                tab_batters.info("No batter data available.")

            pitchers_df = pd.DataFrame(team['pitchers'])
            if not pitchers_df.empty:
                pitchers_df.set_index('player_name', inplace=True)
                tab_pitchers.table(pitchers_df)
            else:
                tab_pitchers.info("No pitcher data available.")
else:
    st.warning("No team data available from database.")