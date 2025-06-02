import streamlit as st
from consumer import consume_latest_processed_data
from producer import send_trigger

BROKER = "172.21.229.182"
PROCESSED_TOPIC = "processed_team_stats"

st.title("⚾ KBO Team Stats Dashboard")

if st.button("🔄 Update Stats via Scraper"):
    send_trigger(BROKER)
    with st.spinner("Trigger sent. Waiting for processed data from Kafka..."):
        data = consume_latest_processed_data(
            broker=BROKER,
            topic=PROCESSED_TOPIC,
            min_messages=1,
            idle_timeout=30.0  # seconds of inactivity before stopping
        )

    if data:
        st.success(f"✅ Received {len(data)} messages from Kafka!")
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
    else:
        st.warning("⚠️ No data received from Kafka within expected time.")
