import json
import os
from datetime import datetime
from utils.db.db_conn import (get_connection, insert_transaction, upsert_transaction_agg)

conn = get_connection()

if conn is None:
    print("DB connection failed, exiting...", flush=True)
    exit(1)

from kafka import KafkaConsumer

BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "localhost:9092"
)

consumer = KafkaConsumer(
    "transactions",
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    group_id="transaction-consumers"
)

counts = {}
current_minute = None

for message in consumer:
    transaction = message.value

    insert_transaction(conn, transaction)

    ts = datetime.fromisoformat(transaction["created_at"])

    minute_key = ts.strftime("%Y-%m-%d %H:%M")

    counts[minute_key] = counts.get(minute_key, 0) + 1

    upsert_transaction_agg(
        conn,
        minute_key,
        counts[minute_key]
    )

    print(
        f"[{minute_key}] Total transactions: "
        f"{counts[minute_key]}",
        flush=True
    )