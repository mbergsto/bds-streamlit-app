import streamlit as st
from consumer import consume_latest_processed_data
from producer import send_trigger
BROKER = "172.21.229.182"
PROCESSED_TOPIC = "processed_team_stats"

st.title("KBO Team Stats Dashboard")

if st.button("🔄 Update Stats via Scraper"):
    send_trigger(BROKER)
    st.success("Trigger message sent!")

st.header("📊 Latest Team Stats")
data = consume_latest_processed_data(BROKER, PROCESSED_TOPIC)

for team in data:
    with st.expander(team['team_name']):
        st.subheader("Team Stats")
        st.json(team['team_stats'])

        st.subheader("Batters")
        for batter in team['batters']:
            st.write(batter)

        st.subheader("Pitchers")
        for pitcher in team['pitchers']:
            st.write(pitcher)
