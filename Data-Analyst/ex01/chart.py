import os
import sys

import psycopg2
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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
    cursor.execute("""
        SELECT
            DATE(event_time),
            COUNT(DISTINCT user_id)
        FROM customers
        WHERE event_type = 'purchase'
          AND event_time >= '2022-10-01'
          AND event_time < '2023-02-01'
        GROUP BY DATE(event_time)
        ORDER BY DATE(event_time);
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

except Exception as e:
    print(f"[ERROR] {e}")
    sys.exit(1)

dates = [row[0] for row in rows]
values = [row[1] for row in rows]


plt.style.use("ggplot")

plt.figure()

plt.plot(dates, values, color="#4C72B0", linewidth=1)


plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b"))
plt.margins(x=0)


plt.yticks([500, 1000, 1500, 2000])
plt.ylabel("Number of customers")

try:
    plt.show()
except KeyboardInterrupt:
    pass
finally:
    plt.close()