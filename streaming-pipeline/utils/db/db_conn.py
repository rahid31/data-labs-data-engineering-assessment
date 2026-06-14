import os
import pymysql
import time


def get_connection(max_retries=5, retry_delay=2):
    for attempt in range(1, max_retries + 1):
        try:
            conn = pymysql.connect(
                host=os.getenv("DB_HOST"),
                port=int(os.getenv("DB_PORT")),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME"),
                connect_timeout=5
            )
            print(f"Connected to MySQL", flush=True)
            return conn
        except Exception as e:
            print(f"Connection failed ({attempt}/{max_retries}): {e}", flush=True)
            if attempt < max_retries:
                print(f"Retrying in {retry_delay}s...", flush=True)
                time.sleep(retry_delay)
    
    print("Failed to connect to MySQL", flush=True)
    return None

def insert_transaction(conn, transaction):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO transactions
            (id, user_id, amount, created_at)
            VALUES (%s, %s, %s, %s)
            """,
            (
                transaction["id"],
                transaction["user_id"],
                transaction["amount"],
                transaction["created_at"]
            )
        )

    conn.commit()

def upsert_transaction_agg(conn, minute_key, total_count):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO transaction_aggs
            (minute_key, total_count)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE
                total_count = VALUES(total_count)
            """,
            (
                minute_key,
                total_count
            )
        )

    conn.commit()