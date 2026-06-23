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

X_scaled = StandardScaler().fit_transform(X)

clusters = KMeans(n_clusters=5,
                  init="k-means++",
                  random_state=42,
                  n_init=10).fit_predict(X_scaled)

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

inactive_id = max(remaining, key=lambda c: cluster_stats[c]["recency_median"])
cluster_names[inactive_id] = "Inactive"
remaining.remove(inactive_id)

for tier in ("Platinum", "Gold"):
    top_value_id = max(remaining, key=lambda c: cluster_stats[c]["monetary_average"])
    cluster_names[top_value_id] = tier
    remaining.remove(top_value_id)

new_id = min(remaining, key=lambda c: cluster_stats[c]["recency_median"])
cluster_names[new_id] = "New customer"
remaining.remove(new_id)

cluster_names[remaining.pop()] = "Silver"

print("\n" + "=" * 70)
print("RFM CLUSTERING ANALYSIS (k=5)")
print("=" * 70)

for cluster_id in range(5):
    stats = cluster_stats[cluster_id]
    print(f"\n{cluster_names[cluster_id].upper()}")
    print(f"  Count: {stats['count']}")
    print(f"  Recency (median): {stats['recency_median']:.1f} days")
    print(f"  Frequency (median): {stats['frequency_median']:.1f}")
    print(f"  Monetary (average): {stats['monetary_average']:.2f}₳")

print("\n" + "=" * 70 + "\n")

SEGMENTS = {
    "Platinum": "#E5E4E2",
    "Gold": "#D4AF37",
    "Silver": "#A6A6A6",
    "New customer": "#6FBF97",
    "Inactive": "#D4A574"
}

segment_order = list(SEGMENTS.keys())

ordered_ids = sorted(
    range(5),
    key=lambda c: segment_order.index(cluster_names[c])
)

max_monetary = max(cluster_stats[c]["monetary_average"] for c in range(5))
max_frequency = max(cluster_stats[c]["frequency_median"] for c in ordered_ids)
max_recency = max(cluster_stats[c]["recency_median"] for c in ordered_ids) / 30

plt.figure(figsize=(10, 7))

for cluster_id in ordered_ids:
    stats = cluster_stats[cluster_id]
    name = cluster_names[cluster_id]
    x = stats["recency_median"] / 30
    y = stats["frequency_median"] / 5
    color = SEGMENTS[name]
    size = 80 + (stats["monetary_average"] / max_monetary) * 700

    plt.scatter(x, y, s=size, color=color, edgecolor="black", linewidth=1.5, alpha=0.8)

    plt.annotate(
        f'Average\n"{name}":\n{stats["monetary_average"]:.2f}₳',
        (x, y),
        textcoords="offset points",
        xytext=(0, 15),
        ha="center",
        fontsize=9,
        fontweight="bold",
    )

plt.xlabel("Median Recency (months)", fontsize=12, fontweight="bold")
plt.ylabel("Median Frequency", fontsize=12, fontweight="bold")

plt.xticks(range(0, 4))
plt.yticks(range(0, 26, 5))

plt.tight_layout()

try:
    plt.show()
except KeyboardInterrupt:
    pass
finally:
    plt.close()