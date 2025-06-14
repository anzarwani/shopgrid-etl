CREATE TABLE IF NOT EXISTS transactions (
    transaction_id UUID PRIMARY KEY,
    user_id INTEGER,
    product_name TEXT,
    category TEXT,
    price NUMERIC(10, 2),
    timestamp TIMESTAMP
);
 
