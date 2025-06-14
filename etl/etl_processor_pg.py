import psycopg2
import json
import os
from datetime import datetime

STAGING_FILE = "D:\shopgrid_etl\staging\incoming_data.jsonl"

VALID_CATEGORIES = {"Apparel", "Electronics", "Home"}

# Adjust with your credentials in db_config.json
with open("config/db_config.json") as f:
    DB_CONFIG = json.load(f)

LOG_FILE = "D:\shopgrid_etl\logs\etl_log.txt"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"[{timestamp}] {msg}\n")

def is_valid(record):
    if record["price"] <= 0:
        return False, "Price must be > 0"
    if record["category"] not in VALID_CATEGORIES:
        return False, f"Invalid category: {record['category']}"
    if not record["product_name"].strip():
        return False, "Product name is empty"
    return True, ""


def clean_record(record):
    # Normalize casing
    record['product_name'] = record['product_name'].title()
    record['category'] = record['category'].capitalize()
    record['timestamp'] = datetime.fromisoformat(record['timestamp'])
    return record

def load_data():
    log("Starting ETL job")
    if not os.path.exists(STAGING_FILE):
        log("No data to process.")
        return

    with open(STAGING_FILE, 'r') as f:
        records = [json.loads(line.strip()) for line in f if line.strip()]

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    for record in records:
        record = clean_record(record)
        is_ok, reason = is_valid(record)
        if not is_ok:
            log(f"Skipping invalid record {record.get('transaction_id', '?')}: {reason}")
            continue
        try:
            cur.execute("""
                INSERT INTO transactions (transaction_id, user_id, product_name, category, price, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (transaction_id) DO NOTHING
            """, (
                record['transaction_id'],
                record['user_id'],
                record['product_name'],
                record['category'],
                record['price'],
                record['timestamp']
            ))
        except Exception as e:
            log(f"DB error on record {record['transaction_id']}: {e}")

    conn.commit()
    conn.close()

    os.remove(STAGING_FILE)
    log("ETL completed. PostgreSQL updated and staging cleared.")

if __name__ == "__main__":
    load_data()
