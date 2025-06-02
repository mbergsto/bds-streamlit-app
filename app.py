import streamlit as st
from mock_consumer import mock_consume_latest_processed_data
#from consumer import consume_latest_processed_data
#from db_utils import fetch_latest_processed_team_stats
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

# Team font colors 
team_colors = {
    "Hanwha Eagles": "#F08200",   # Pumpkin orange :contentReference[oaicite:0]{index=0}
    "LG Twins":       "#C40452",   # Maroon :contentReference[oaicite:1]{index=1}
    "Samsung Lions":  "#1428A0",   # Samsung blue :contentReference[oaicite:2]{index=2}
    "Doosan Bears":   "#000080",   # Navy blue :contentReference[oaicite:3]{index=3}
    "Lotte Giants":   "#FF7F00",   # Orange :contentReference[oaicite:4]{index=4}
    "NC Dinos":       "#405A3D",   # Dino green :contentReference[oaicite:5]{index=5}
    "KT Wiz":         "#E60013",   # KT red :contentReference[oaicite:6]{index=6}
    "Kiwoom Heroes":  "#800020",   # Burgundy :contentReference[oaicite:7]{index=7}
    "SSG Landers":    "#E60013",   # SSG charismatic red :contentReference[oaicite:8]{index=8}
    "KIA Tigers":     "#FF0000",   # Red (Wikipedia: “Colors: Red, white, black”) :contentReference[oaicite:9]{index=9}
}

# Page configuration
st.set_page_config(
    page_title="⚾ KBO Team Stats Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants from environment
BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVER")
KAFKA_TOPIC_IN = os.getenv("KAFKA_TOPIC_IN", "processed_team_stats")
KAFKA_TOPIC_OUT = os.getenv("KAFKA_TOPIC_OUT", "trigger_scrape")

# Title
st.title("⚾ KBO Team Stats Dashboard")

# Trigger Panel
st.sidebar.header("Controls") 

@st.cache_data
def load_data():
    logging.info("Loading data from database via fetch_latest_processed_team_stats...")
    #data = fetch_latest_processed_team_stats()
    data = mock_consume_latest_processed_data()
    #logging.info(f"Fetched {len(data) if data else 0} records from database.")
    return data

data = load_data()

if st.sidebar.button("🔄 Update Stats via Scraper"): 
    send_trigger(BROKER, KAFKA_TOPIC_OUT)
    with st.spinner("Trigger sent. Waiting for processed data from Kafka..."):
         """ data = consume_latest_processed_data(
             broker=BROKER,
             topic=KAFKA_TOPIC_IN,
         )  """
    data = mock_consume_latest_processed_data()

    if data: 
        st.success(f"✅ Received {len(data)} team records from Kafka!")

        # Team filter in sidebar
        team_names = [team["team_name"] for team in data]
        selected = st.sidebar.multiselect(
            "Filter Teams:", team_names, default=team_names
        )

        # Display each selected team's dashboard
        for team in sorted(data, key=lambda x: x["team_name"]):
            if team["team_name"] not in selected: 
                continue

            # Highlight team names
            color = team_colors.get(team["team_name"], "#000000")
            with st.expander(f"{team['team_name']}", expanded=True) : 
                
                # team image
                img_col, text_col = st.columns([1, 9], gap="small")

                logo_path = team_logos.get(team["team_name"], None)
                if logo_path and os.path.exists(logo_path):
                    img_col.image(logo_path, width=50)
                else:
                    img_col.write("")
                
                
                st.markdown(
                    f"<h2 style='color:{color}; font-weight:bold'>{team['team_name']}</h2>",
                    unsafe_allow_html=True
                )
                
                
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
                tab_form.metric("Average Form Score", team['team_form_score'])

                # Batters Table
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
                    tab_batters.table(batters_df)
                else:
                    tab_batters.info("No batter data available.")

                # Pitchers Table
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

        for team in sorted(data, key=lambda x: x["team_name"]):
            if team["team_name"] not in selected: 
                continue

            # Highlight team names
            color = team_colors.get(team["team_name"], "#000000")
            with st.expander(f"{team['team_name']}", expanded=True) : 
                
                # team image
                img_col, text_col = st.columns([1, 9], gap="small")
                logo_path = team_logos.get(team["team_name"], None)
                if logo_path and os.path.exists(logo_path):
                    img_col.image(logo_path, width=50)
                else:
                    img_col.write("")
                
                
                st.markdown(
                    f"<h2 style='color:{color}; font-weight:bold'>{team['team_name']}</h2>",
                    unsafe_allow_html=True
                ) 
                
                
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
                    
                    tab_pitchers.table(pitchers_df)
                else:
                    tab_pitchers.info("No pitcher data available.")
    else:
        st.warning("No team data available from database.")