import os
import json
import time
import uuid
import random
from datetime import datetime

from kafka import KafkaProducer


producer = KafkaProducer(
    bootstrap_servers=os.getenv(
        "KAFKA_BOOTSTRAP_SERVERS",
        "localhost:9092"
    ),
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

TOPIC = "transactions"

while True:
    transaction = {
        "id": str(uuid.uuid4()),
        "user_id": random.randint(1000, 9999),
        "amount": random.randint(10000, 1000000),
        "created_at": datetime.now().isoformat()
    }

    producer.send(TOPIC, value=transaction)
    # producer.flush()

    print(f"Produced: {transaction}")

    time.sleep(6) # Sleep for 6 seconds to produce 10 transactions per minute