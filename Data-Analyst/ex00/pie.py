import os
import sys

import psycopg2
import matplotlib.pyplot as plt

required_vars = ["POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DB", "POSTGRES_PORT"]
for var in required_vars:
    if not os.getenv(var):
        print(f"[ERROR] Environment variable {var} is not set.")
        sys.exit(1)

DB_CONFIG = {
    "host":     "localhost",
    "port":     os.getenv("POSTGRES_PORT"),
    "dbname":   os.getenv("POSTGRES_DB"),
    "user":     os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}

try:
    conn   = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT event_type, COUNT(*) FROM customers GROUP BY event_type ORDER BY COUNT(*) DESC")
    rows   = cursor.fetchall()
    cursor.close()
    conn.close()
except Exception as e:
    print(f"[ERROR] {e}")
    sys.exit(1)


labels = [row[0] for row in rows]
totals = [row[1] for row in rows]


plt.figure()

plt.pie(
    totals,
    labels=labels,
    autopct="%1.1f%%",
    wedgeprops={"edgecolor": "white"}
)

try:
    plt.show()
except KeyboardInterrupt:
    pass
finally:
    plt.close()