# Real-time Dummy Transaction Streaming Pipeline

A real-time event streaming pipeline built with Apache Kafka and MySQL that captures, processes, and aggregates transaction data in real-time.

## Overview

This project demonstrates a modern streaming architecture that:
- **Produces** random transaction events continuously
- **Streams** transactions through Apache Kafka
- **Consumes** and processes events in real-time
- **Stores** transaction data in MySQL
- **Aggregates** transaction counts by minute

---

## Project Structure

```
streaming-pipeline/
├── producer.py              # Generates random transaction events
├── consumer.py              # Consumes and processes transactions
├── docker-compose.yaml      # Docker services orchestration
├── Dockerfile               # Container image configuration
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (create manually)
│
└── utils/
    └── db/
        ├── db_conn.py       # Database connection utilities
        └── init.sql         # MySQL schema & user setup
```

---

## Docker Setup

### Prerequisites

- Docker & Docker Compose installed
- Linux/macOS or WSL2 on Windows

### Installation Steps

1. **Clone or navigate to the project:**
   ```bash
   cd streaming-pipeline
   ```

2. **Create `.env` file** in the root directory:
   ```bash
   cat > .env << 'EOF'
   MYSQL_ROOT_PASSWORD=your_root_password

   DB_HOST=mysql
   DB_PORT=3306
   DB_NAME=stg_transactions
   DB_USER=admin_user
   DB_PASSWORD=admin123!
   EOF
   ```

3. **Build and start all services:**
   ```bash
   sudo docker compose up --build
   ```

---

## Usage Commands

### Start the Pipeline
```bash
sudo docker compose up --build
```

### Start in Background (Detached Mode)
```bash
sudo docker compose up -d --build
```

### Stop All Services
```bash
sudo docker compose down
```

### Stop & Remove Volumes
```bash
sudo docker compose down -v --remove-orphans
```

### View Logs

- **All services:**
  ```bash
  sudo docker compose logs -f
  ```

Or

- **By Containers:**
  ```bash
  sudo docker compose logs -f {container_name}
  ```

### Access MySQL Database
```bash
sudo docker exec -it mysql mysql -u admin_user -p stg_transactions
```
Password: `admin123!`

### Query Transaction Data
```sql
-- View all transactions
SELECT * FROM transactions ORDER BY created_at DESC LIMIT 10;

-- View aggregated counts per minute
SELECT * FROM transaction_aggs ORDER BY minute_key DESC;

-- Count total transactions
SELECT COUNT(*) as total_transactions FROM transactions;
```

---

## Producer & Consumer Details

### Producer Behavior

**What it does:**
- Generates random transactions every 6 seconds (10 transactions per minute)
- Each transaction includes:
  - Unique transaction ID (UUID)
  - Random user ID (1000-9999)
  - Random amount (10,000 - 1,000,000 units)
  - Current timestamp (ISO format)
- Sends to Kafka topic: `transactions`

**Example Output:**
```
Produced: {
  'id': '550e8400-e29b-41d4-a716-446655440000',
  'user_id': 5432,
  'amount': 456789,
  'created_at': '2026-06-15T14:30:45.123456'
}
Produced: {
  'id': '6ba7b810-9dad-11d1-80b4-00c04fd430c8',
  'user_id': 8901,
  'amount': 234567,
  'created_at': '2026-06-15T14:30:51.654321'
}
```

### Consumer Behavior

**What it does:**
- Listens to Kafka `transactions` topic
- For each transaction:
  1. Inserts into MySQL `transactions` table
  2. Extracts minute (YYYY-MM-DD HH:MM format)
  3. Counts transactions per minute
  4. Updates/inserts into MySQL `transaction_aggs` table

**Consumer Flow:**
```
Kafka Message
    ↓
Parse Transaction
    ↓
Insert into DB
    ↓
Extract Minute Key
    ↓
Count & Aggregate
    ↓
Upsert to Aggregates Table
    ↓
Print Summary
```

**Example Output:**
```
✓ Connected to MySQL on attempt 1
[2026-06-15 14:30] Total transactions: 1
[2026-06-15 14:30] Total transactions: 2
[2026-06-15 14:30] Total transactions: 3
...
[2026-06-15 14:31] Total transactions: 1
[2026-06-15 14:31] Total transactions: 2
```

### Data Schema

**transactions table:**
```
- id VARCHAR(255) PRIMARY KEY
- user_id INT
- amount FLOAT
- created_at DATETIME
```

**transaction_aggs table:**
```
- minute_key VARCHAR(20) PRIMARY KEY
- total_count INT
```

---

## Architecture

```
┌─────────────┐
│  Producer   │ → Generates transactions (every 6 seconds)
└─────────────┘
       ↓
┌─────────────┐
│   Kafka     │ → Streams transactions via "transactions" topic
└─────────────┘
       ↓
┌─────────────┐
│  Consumer   │ → Processes and aggregates
└─────────────┘
       ↓
┌─────────────┐
│   MySQL     │ → Stores transactions & aggregates
└─────────────┘
```

---

## Troubleshooting

**Consumer can't connect to MySQL:**
- Ensure `.env` file exists with correct values
- Check MySQL container is healthy: `sudo docker compose ps`
- View MySQL logs: `sudo docker compose logs mysql`

**Kafka connection errors:**
- Ensure all containers are running: `sudo docker compose ps`
- Check if ports 9092 (Kafka), 3306 (MySQL) are not in use

**Database credentials don't match:**
- Verify `.env` values match `utils/db/init.sql`
- Current credentials: `admin_user` / `admin123!`


