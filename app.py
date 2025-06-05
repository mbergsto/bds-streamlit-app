import streamlit as st
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

# Team logos
team_logos = {
    "Hanwha Eagles":   "logos/hanwha.png",
    "LG Twins":        "logos/lg.png",
    "Samsung Lions":   "logos/samsung.png",
    "Doosan Bears":    "logos/doosan.png",
    "Lotte Giants":    "logos/lotte.png",
    "NC Dinos":        "logos/nc.png",
    "KT Wiz":          "logos/kt.png",
    "Kiwoom Heroes":   "logos/kiwoom.png",
    "SSG Landers":     "logos/ssg.png",
    "KIA Tigers":      "logos/kia.png",
}


# Page configuration
st.set_page_config(
    page_title="⚾ KBO Team Stats Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

#custom CSS 
st.markdown(
    """
    <style>
    div[data-testid="stExpander"] details summary p {
        font-size: 18px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
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

        # Highlight team names
        with st.expander(f"{team['team_name']}", expanded=True) : 
            
            # team image
            img_col, text_col = st.columns([1, 9], gap="small")
            logo_path = team_logos.get(team["team_name"], None)
            if logo_path and os.path.exists(logo_path):
                img_col.image(logo_path, width=50)
            else:
                img_col.write("")
            
            
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
            tab_form.metric("Average Form Score", team['team_form_score'])
            batters_df = pd.DataFrame(team['batters'])
            if not batters_df.empty:
                batters_df.set_index('player_name', inplace=True)
                
                # Change the index name to a user-friendly one
                batters_df.index.name = "Player Name"
                
                # Change column names to user-friendly ones
                batters_df = batters_df.rename(columns={
                "batting_average": "Batting Average",
                "on_base_percentage": "On Base Percentage",
                "form_score": "Form Score"
                })
                
                for col in batters_df.select_dtypes(include=['float']).columns:
                    batters_df[col] = batters_df[col].apply(lambda x: f"{x:.2f}")

                tab_batters.table(batters_df)
            else:
                tab_batters.info("No batter data available.")

            pitchers_df = pd.DataFrame(team['pitchers'])
            if not pitchers_df.empty:
                pitchers_df.set_index('player_name', inplace=True)
                
                # Change the index name to a user-friendly one
                pitchers_df.index.name = "Player Name"
                
                # Change column names to user-friendly ones
                pitchers_df = pitchers_df.rename(columns={
                "era": "ERA",
                "whip": "WHIP",
                "k_per_9": "K Per 9",
                "bb_per_9": "BB per 9",
                "form_score": "Form Score"
                })
                
                for col in pitchers_df.select_dtypes(include=['float']).columns:
                    pitchers_df[col] = pitchers_df[col].apply(lambda x: f"{x:.2f}")

                tab_pitchers.table(pitchers_df)
            else:
                tab_pitchers.info("No pitcher data available.")
else:
    st.warning("No team data available from database.")