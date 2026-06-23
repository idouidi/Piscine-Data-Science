import os
import sys
import psycopg2
import matplotlib.pyplot as plt

DB_CONFIG = {
    "host":     "localhost",
    "port":     os.getenv("POSTGRES_PORT"),
    "dbname":   os.getenv("POSTGRES_DB"),
    "user":     os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}

query = """
    SELECT user_id, COUNT(*)
    FROM customers
    WHERE event_type = 'purchase'
    GROUP BY user_id
    HAVING COUNT(*) <= 40
"""


try:
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    conn.close()
except Exception as e:
    print(f"[ERROR] {e}")
    sys.exit(1)

if not data:
    print("[WARNING] No data found")
    sys.exit(0)

frequency = [row[1] for row in data]

plt.style.use("seaborn-v0_8")
plt.figure(figsize=(8, 6))

plt.grid(True)
plt.hist(frequency, bins=5, edgecolor='white', color="#7693c7fc")
plt.ylabel('customers')
plt.xlabel('frequency')
plt.xticks(range(0, 39, 10))
plt.ylim(0, 60000)
plt.tight_layout()

try:
    plt.show()
except KeyboardInterrupt:
    pass
finally:
    plt.close()
