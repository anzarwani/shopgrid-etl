from fastapi import FastAPI
from pydantic import BaseModel
import json
import uuid
import os
from datetime import datetime

app = FastAPI()
STAGING_FILE = "D:\\shopgrid_etl\\staging\\incoming_data.jsonl"

class Record(BaseModel):
    user_id: int
    product_name: str
    category: str
    price: float

@app.post("/ingest/")
async def ingest_data(record: Record):
    full_record = record.dict()
    full_record["transaction_id"] = str(uuid.uuid4())
    full_record["timestamp"] = datetime.now().isoformat()

    os.makedirs(os.path.dirname(STAGING_FILE), exist_ok=True)
    with open(STAGING_FILE, "a") as f:
        f.write(json.dumps(full_record) + "\n")

    return {"status": "ok", "message": "Record stored", "id": full_record["transaction_id"]}
