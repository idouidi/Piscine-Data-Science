import os
import sys

import psycopg2
import numpy as np
import matplotlib.pyplot as plt

required_vars = ["POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DB", "POSTGRES_PORT"]
for var in required_vars:
    if not os.getenv(var):
        print(f"[ERROR] Environment variable {var} is not set.")
        sys.exit(1)

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
        SELECT DISTINCT ON (user_id, event_time, price) 
            price AS converted_price
        FROM customers
        WHERE event_type = 'purchase'
          AND event_time >= '2022-10-01'
          AND event_time < '2023-02-01'
    """
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

except Exception as e:
    print(f"[ERROR] {e}")
    sys.exit(1)

prices = [float(row[0]) for row in rows]

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

box_face_color = "#76c876"
outline_color = "#4c4c4c"

plt.figure()

plt.boxplot(
    prices,
    vert=False,  # Horizontal display
    patch_artist=True,  # Enable filling the box with color (required for facecolor)
    widths=0.7,  # Increase box height to fill the vertical space
    showfliers=False,  # Hide outliers (essential to zoom in on the box)
    # Box customization (Seaborn green color, thin border)
    boxprops=dict(facecolor=box_face_color, color=outline_color, linewidth=1.0),
    # Median line
    medianprops=dict(color=outline_color, linewidth=1.3),
    # Whiskers
    whiskerprops=dict(color=outline_color, linewidth=1.0),
    # Caps at the end of whiskers
    capprops=dict(color=outline_color, linewidth=1.0),
)


plt.xticks(range(0, 14, 2))
plt.xlabel("price")

# Hide Y-axis and its associated grid lines
plt.yticks([])
plt.gca().yaxis.grid(False)

# Optimize margins/padding
plt.tight_layout()

try:
    plt.show()
except KeyboardInterrupt:
    pass
finally:
    plt.close()
