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
            DATE_TRUNC('day', event_time) AS day,
            SUM(price / 1.25) / COUNT(DISTINCT user_id) AS avg_spend_per_customer
        FROM customers
        WHERE event_type = 'purchase'
          AND event_time >= '2022-10-01'
          AND event_time < '2023-02-01'
        GROUP BY DATE_TRUNC('day', event_time) 
        ORDER BY DATE_TRUNC('day', event_time); 
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


plt.fill_between(dates, values, color="#487DD3")
plt.plot(dates, values, color="#487DD3")

plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b"))
plt.margins(x=0)


plt.yticks(range(0, 41, 5))
plt.ylim(bottom=0) 
plt.ylabel("average spend/customers in ₳")

try:
    plt.show()
except KeyboardInterrupt:
    pass
finally:
    plt.close()