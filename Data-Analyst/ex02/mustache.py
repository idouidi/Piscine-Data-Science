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
        SELECT DISTINCT ON (user_id, event_time, price)
            price
        FROM customers
        WHERE event_type = 'purchase'
          AND event_time >= '2022-10-01'
          AND event_time < '2023-02-01'
    """
    )

    prices = [float(row[0]) for row in cursor.fetchall()]

    cursor.close()
    conn.close()

except Exception as e:
    print(f"[ERROR] {e}")
    sys.exit(1)

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
    vert=False,  # Display the boxplot horizontally instead of vertically
    patch_artist=True,  # Enable filling the box with a color (required for facecolor)
    widths=0.6,  # Set the width/thickness of the box
    showfliers=True,  # Display data points outside the whiskers (outliers)
    # Customizes the main body of the box (fill color, border color, and border thickness)
    boxprops=dict(facecolor=box_face_color, color=outline_color, linewidth=1.0),
    # Customizes the median line inside the box (color and thickness)
    medianprops=dict(color=outline_color, linewidth=1.5),
    # Customizes the caps (the small vertical ticks at the end of the whiskers)
    capprops=dict(color=outline_color, linewidth=1.0),
    # Customizes the outlier points ('d' for diamond shape, color, and size)
    flierprops=dict(
        marker="d",
        markerfacecolor=outline_color,
        markeredgecolor=outline_color,
        markersize=4,
    ),
)

plt.xlim(-90, 340)
plt.xticks(range(-50, 301, 50))
plt.xlabel("price")
plt.yticks([])


try:
    plt.show()
except KeyboardInterrupt:
    pass
finally:
    plt.close()
