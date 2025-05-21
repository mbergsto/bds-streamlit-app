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
   git clone https://github.com/yourusername/bds-streamlit-app.git
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
4. Run the app:
   ```bash
   streamlit run app.py
   ```
