# 🛒 ShopGrid Catalog ETL

A real-world, production-style ETL pipeline built without Docker or Kafka — designed for simplicity, clarity, and extensibility.

## Project Structure

- **`generator/`** — Python script to generate synthetic product transactions and send via HTTP
- **`ingest/`** — FastAPI server to receive transactions and stage them as `.jsonl`
- **`etl/`** — ETL script to clean, validate, and load records into PostgreSQL
- **`logs/`** — Auto-generated ETL logs
- **`staging/`** — Temporary holding for incoming data
- **`config/`** — Database credentials (not tracked by Git)

## Quick Start

### 1. Setup PostgreSQL

Create table:

```sql
CREATE TABLE transactions (
    transaction_id UUID PRIMARY KEY,
    user_id INT,
    product_name TEXT,
    category TEXT,
    price NUMERIC,
    timestamp TIMESTAMP
);
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the ingestion API

```bash
uvicorn ingestion.fastapi_ingress:app --reload
```

### 4. Send test data

```bash
python generator/generator_http.py
```

### 5. Run ETL manually

```bash
python etl/etl_processor_pg.py
```