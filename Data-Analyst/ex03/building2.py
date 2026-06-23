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
SELECT user_id, SUM(price)
FROM customers
WHERE event_type = 'purchase'
GROUP BY user_id

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

monetary_values = [float(row[1]) for row in data]

plt.style.use("seaborn-v0_8")
plt.figure(figsize=(8, 6))

plt.grid(True)

plt.hist(monetary_values, bins=range(-30, 240, 50), edgecolor='white', color="#7693c7fc")

plt.yticks(range(0, 42000, 5000))
plt.ylim(0, 42000)
plt.xlabel('monetary value in ₳')
plt.ylabel('customers')
plt.tight_layout()

try:
    plt.show()
except KeyboardInterrupt:
    pass
finally:
    plt.close()
