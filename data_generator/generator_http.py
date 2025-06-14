import requests
import uuid
import random
from datetime import datetime
import time

PRODUCTS = [
    ("Red Hat", "Apparel", 499.99),
    ("Blue Shirt", "Apparel", 799.00),
    ("Smart Watch", "Electronics", 2599.50),
    ("Wireless Mouse", "Electronics", 649.75),
    ("Coffee Mug", "Home", 299.00)
]

def generate_record():
    product = random.choice(PRODUCTS)
    return {
        # "transaction_id": str(uuid.uuid4()),
        "user_id": random.randint(1000, 1100),
        "product_name": product[0],
        "category": product[1],
        "price": round(product[2] + random.uniform(-50, 50), 2),
        "timestamp": datetime.now().isoformat()
    }

for _ in range(10):
    rec = generate_record()
    try:
        r = requests.post("http://localhost:8000/ingest/", json=rec)
        print(f"Sent: {rec} → Status: {r.status_code}")
    except Exception as e:
        print(f"❌ Failed to send: {e}")
    time.sleep(0.5)
