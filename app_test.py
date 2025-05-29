import streamlit as st
#from consumer import consume_latest_processed_data
from mock_consumer import mock_consume_latest_processed_data
from db_utils import fetch_latest_processed_team_stats
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
BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVER", "localhost")
PROCESSED_TOPIC = os.getenv("KAFKA_TOPIC_OUT", "processed_team_stats")

# Title
st.title("⚾ KBO Team Stats Dashboard")

# Trigger Panel
st.sidebar.header("Controls") 

@st.cache_data
def load_data():
    logging.info("Loading data from database via fetch_latest_processed_team_stats...")
    data = fetch_latest_processed_team_stats()
    logging.info(f"Fetched {len(data) if data else 0} records from database.")
    return data

data = load_data()

if st.sidebar.button("🔄 Update Stats via Scraper"): 
    #send_trigger(BROKER)
    with st.spinner("Trigger sent. Waiting for processed data from Kafka..."):
        # data = consume_latest_processed_data(
        #     broker=BROKER,
        #     topic=PROCESSED_TOPIC,
        #     min_messages=1,
        #     idle_timeout=30.0
        # ) 
        data = mock_consume_latest_processed_data()

    if data: 
        st.success(f"✅ Received {len(data)} team records from Kafka!")

        # Team filter in sidebar
        team_names = [team["team_name"] for team in data]
        selected = st.sidebar.multiselect(
            "Filter Teams:", team_names, default=team_names
        )

        # Display each selected team's dashboard
        for team in data:
            if team["team_name"] not in selected: 
                continue

            with st.expander(f"{team['team_name']} Dashboard", expanded=True):
                # Team Stats Metrics
                stats = team['team_stats']
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Wins", stats['wins'])
                col2.metric("Losses", stats['losses'])
                col3.metric("Draws", stats['draws'])
                col4.metric("Score Diff", stats['score_difference'])

                # Tabs for detailed views
                tab_form, tab_batters, tab_pitchers = st.tabs([
                    "Team Form", 
                    "Batters", 
                    "Pitchers"
                ])

                # Team Form: Precomputed form score
                tab_form.metric("Avg Form Score", team['team_form_score'])

                # Batters Table
                batters_df = pd.DataFrame(team['batters'])
                if not batters_df.empty:
                    batters_df.set_index('player_name', inplace=True)
                    tab_batters.table(batters_df)
                else:
                    tab_batters.info("No batter data available.")

                # Pitchers Table
                pitchers_df = pd.DataFrame(team['pitchers'])
                if not pitchers_df.empty:
                    pitchers_df.set_index('player_name', inplace=True)
                    tab_pitchers.table(pitchers_df)
                else:
                    tab_pitchers.info("No pitcher data available.")
    else:
        st.warning("⚠️ No data received from Kafka within expected time.") # If no available new data
else:
    if data:
        st.success(f"✅ Loaded {len(data)} team records from the database.")
        # Team filter in sidebar
        team_names = [team["team_name"] for team in data]
        selected = st.sidebar.multiselect(
            "Filter Teams:", team_names, default=team_names
        )

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

                tab_form, tab_batters, tab_pitchers = st.tabs([
                    "Team Form", 
                    "Batters", 
                    "Pitchers"
                ])
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