import os
import sys
import numpy as np
import psycopg2
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

DB_CONFIG = {
    "host": "localhost",
    "port": os.getenv("POSTGRES_PORT"),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}

QUERY = """
    WITH per_user AS (
        SELECT
            MAX(event_time) AS last_purchase,
            COUNT(*) AS frequency,
            SUM(price) AS monetary
        FROM customers
        WHERE event_type = 'purchase'
        GROUP BY user_id
    )
    SELECT
        EXTRACT(DAY FROM (MAX(last_purchase) OVER () - last_purchase)) AS recency,
        frequency,
        monetary
    FROM per_user;
"""

try:
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(QUERY)
    data = cur.fetchall()
    cur.close()
    conn.close()
except Exception as e:
    print(f"[ERROR] {e}")
    sys.exit(1)

if not data:
    print("[WARNING] No data found")
    sys.exit(0)



X = np.array(data, dtype=float)
recency, frequency, monetary = X[:, 0], X[:, 1], X[:, 2]

# Normalize features: (x - mean) / std -> all columns have mean=0, std=1
# This improves KMeans performance
X_scaled = StandardScaler().fit_transform(X)


clusters = KMeans(n_clusters=5,
                  init="k-means++",
                  random_state=42,
                  n_init=10).fit_predict(X_scaled)


# For each cluster (0-4), calculate:
# - count: number of customers in this cluster
# - recency_median: median days since last purchase
# - frequency_median: median number of purchases
# - monetary_average: average total spent
cluster_stats = [
    {
        "count": int(np.sum(clusters == cluster_id)),
        "recency_median": np.median(recency[clusters == cluster_id]),
        "frequency_median": np.median(frequency[clusters == cluster_id]),
        "monetary_average": np.mean(monetary[clusters == cluster_id]),
    }
    for cluster_id in range(5)
]


remaining = set(range(5))
cluster_names = [None] * 5

# "Inactive" cluster (highest recency = not purchased recently)
inactive_id = max(remaining, key=lambda c: cluster_stats[c]["recency_median"])
cluster_names[inactive_id] = "Inactive"
remaining.remove(inactive_id)

# "Platinum" and "Gold" clusters (highest monetary values)
for tier in ("Platinum", "Gold"):
    top_value_id = max(remaining, key=lambda c: cluster_stats[c]["monetary_average"])
    cluster_names[top_value_id] = tier
    remaining.remove(top_value_id)

# "New customer" cluster (lowest recency among remaining = recently started)
new_id = min(remaining, key=lambda c: cluster_stats[c]["recency_median"])
cluster_names[new_id] = "New customer"
remaining.remove(new_id)

# Assign "Silver" to the last remaining cluster
cluster_names[remaining.pop()] = "Silver"


# Define segments and their colors in priority order
SEGMENTS = {
    "Platinum": "#E5E4E2",
    "Gold": "#D4AF37",
    "Silver": "#A6A6A6",
    "New customer": "#6FBF97",
    "Inactive": "#D4A574"
}

# Extract the display order from SEGMENTS keys
# Example: ["Platinum", "Gold", "Silver", "New customer", "Inactive"]
segment_order = list(SEGMENTS.keys())

# Sort cluster indices (0, 1, 2, 3, 4) by their position in segment_order
ordered_ids = sorted(
    range(5),
    key=lambda c: segment_order.index(cluster_names[c])
)

names_ordered = [cluster_names[c] for c in ordered_ids]
counts = [cluster_stats[c]["count"] for c in ordered_ids]
colors = [SEGMENTS[cluster_names[c]] for c in ordered_ids]

plt.figure(figsize=(12, 6))

# Create horizontal bar chart with names, counts, and colors aligned
plt.barh(names_ordered, counts, color=colors, edgecolor="black", linewidth=1)

# Set x-axis label
plt.xlabel("Number of customers", fontsize=12, fontweight="bold")

# Set x-axis limits and ticks
max_count = max(counts)
plt.xlim(0, max_count)
plt.xticks(range(0, int(max_count * 1.1) + 5000, 5000))

# Add count labels on top of each bar
for i, count in enumerate(counts):
    plt.text(count + 500, i, str(count), va="center", fontsize=12, fontweight="bold")

# Invert y-axis so "Platinum" appears at top
plt.gca().invert_yaxis()

# Adjust layout to prevent label cutoff
plt.tight_layout()


try:
    plt.show()
except KeyboardInterrupt:
    pass
finally:
    plt.close()