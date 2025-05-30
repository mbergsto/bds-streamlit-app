# bds-streamlit-app

A Streamlit web application for triggering and visualizing processed KBO game data in a big data pipeline using Kafka, Scrapy, and MariaDB.

## Features

- Trigger Scrapy-based web scraping jobs via Kafka
- Real-time display of processed KBO team statistics
- Kafka consumer integration for automatic data retrieval
- Clean, interactive dashboard with expandable team views
- Displays team form, batters, and pitchers directly in the browser

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/mbergsto/bds-streamlit-app.git
   cd bds-streamlit-app
   ```
2. (Optional but recommended) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   Create a `.env` file in the root directory with the following content:

   ```env
   DB_CONNECTION=local  # Set to "local" or "remote" to choose which DB configuration to use

   KAFKA_BOOTSTRAP_SERVER=172.21.229.182
   KAFKA_TOPIC_IN=processed_team_stats  # Topic the app listens to for incoming processed data
   KAFKA_TOPIC_OUT=trigger_scrape       # Topic used to trigger the scraping pipeline

   # Remote DB configuration
   DB_REMOTE_USER=bigdata
   DB_REMOTE_PASSWORD=bigdata+
   DB_REMOTE_HOST=192.168.1.102
   DB_REMOTE_PORT=3306
   DB_REMOTE_NAME=scraping_db

   # Local DB configuration
   DB_LOCAL_USER=bigdata
   DB_LOCAL_PASSWORD=bigdata+
   DB_LOCAL_HOST=127.0.0.1
   DB_LOCAL_PORT=3307
   DB_LOCAL_NAME=scraping_local
   ```

5. Run the app:
   ```bash
   streamlit run app.py
   ```
