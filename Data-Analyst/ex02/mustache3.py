import os
import sys
import psycopg2
import numpy as np
import matplotlib.pyplot as plt

DB_CONFIG = {
    "host": "localhost",
    "port": os.getenv("POSTGRES_PORT"),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}

try:
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(
        """
SELECT user_id, AVG(price) AS avg_price
FROM customers
WHERE event_type = 'purchase'
GROUP BY user_id
HAVING AVG(price) BETWEEN 27 AND 42;
    """
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

except Exception as e:
    print(f"[ERROR] {e}")
    sys.exit(1)

prices = [float(row[1]) for row in rows]

if not prices:
    print("[WARNING] No price found")
    sys.exit(0)

count_val = float(len(prices))
mean_val = np.mean(prices)
std_val = np.std(prices)
min_val = np.min(prices)
q1_val = np.percentile(prices, 25)
median_val = np.percentile(prices, 50)
q3_val = np.percentile(prices, 75)
max_val = np.max(prices)

print(f"{'count':<10}{count_val:>13.6f}")
print(f"{'mean':<10}{mean_val:>13.6f}")
print(f"{'std':<10}{std_val:>13.6f}")
print(f"{'min':<10}{min_val:>13.6f}")
print(f"{'25%':<10}{q1_val:>13.6f}")
print(f"{'50%':<10}{median_val:>13.6f}")
print(f"{'75%':<10}{q3_val:>13.6f}")
print(f"{'max':<10}{max_val:>13.6f}")

plt.style.use("seaborn-v0_8")

plt.figure(figsize=(10, 6))

outline_color = "#4c4c4c"
box_face_color = "#7298B8"

plt.boxplot(
    prices,
    vert=False,
    widths=0.6,
    patch_artist=True,
    whis=(2, 95),  # à ajuster éventuellement
    boxprops=dict(facecolor=box_face_color, edgecolor=outline_color, linewidth=2),
    medianprops=dict(color=outline_color, linewidth=2),
    whiskerprops=dict(color=outline_color, linewidth=1.7),
    capprops=dict(color=outline_color, linewidth=1.7),
    flierprops=dict(
        marker="D",
        markersize=6,
        markerfacecolor=outline_color,
        markeredgecolor=outline_color,
    ),
)

plt.yticks([])
plt.xlabel("price")

plt.xticks(np.arange(28, 43, 2))
plt.xlim(26, 43)

plt.grid(True, axis="x")
plt.tight_layout()

try:
    plt.show()
except KeyboardInterrupt:
    pass
finally:
    plt.close()
