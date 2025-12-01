from src.db import get_db

conn = get_db()
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS whatsapp_messages (
    id SERIAL PRIMARY KEY,
    sender VARCHAR(50),
    message TEXT,
    created_at TIMESTAMP DEFAULT NOW()
)
""")

conn.commit()
cur.close()
conn.close()

print("TABLE CREATED")
