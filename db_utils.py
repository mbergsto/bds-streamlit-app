import os
import json
import mariadb
from dotenv import load_dotenv

load_dotenv()

DB_CONNECTION = os.getenv("DB_CONNECTION", "").strip()
is_local = DB_CONNECTION == "local"

print("is local:", is_local)
print("DB_CONNECTION:", DB_CONNECTION)

db_config = {
    "user": os.getenv("DB_LOCAL_USER") if is_local else os.getenv("DB_REMOTE_USER"),
    "password": os.getenv("DB_LOCAL_PASSWORD") if is_local else os.getenv("DB_REMOTE_PASSWORD"),
    "host": os.getenv("DB_LOCAL_HOST") if is_local else os.getenv("DB_REMOTE_HOST"),
    "port": int(os.getenv("DB_LOCAL_PORT") if is_local else os.getenv("DB_REMOTE_PORT")),
    "database": os.getenv("DB_LOCAL_NAME") if is_local else os.getenv("DB_REMOTE_NAME")
}

def fetch_latest_processed_team_stats():
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT team_name, snapshot FROM processed_team_stats")
        rows = cursor.fetchall()
        data = []
        for team_name, snapshot in rows:
            try:
                parsed_snapshot = json.loads(snapshot)
                parsed_snapshot['team_name'] = team_name
                data.append(parsed_snapshot)
            except json.JSONDecodeError:
                continue

        cursor.close()
        conn.close()
        return data

    except mariadb.Error as e:
        print(f"Database error: {e}")
        return []
