import os
import sys
import numpy as np
import psycopg2
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

DB_CONFIG = {
    "host":     "localhost",
    "port":     os.getenv("POSTGRES_PORT"),
    "dbname":   os.getenv("POSTGRES_DB"),
    "user":     os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}

query = """
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

# Normalize the data (Recency, Frequency, Monetary)
# StandardScaler: (x - mean) / std on each column
# Result: all columns have mean=0 and std=1
X_scaled = StandardScaler().fit_transform(np.array(data, dtype=float))

# Test KMeans with k=1 to k=10 clusters
k_range = range(1, 11)

# For each k, run KMeans and calculate WCSS (Within-Cluster Sum of Squares)
wcss = [
    KMeans(
        n_clusters=k,              # Number of clusters to create
        init="k-means++",          # Smart initialization (choose k centroids strategically)
        random_state=42,           # Fixed seed for reproducible results
        n_init=10                  # Run algorithm 10 times, keep best result
    )
    .fit(X_scaled)  # Step 1 : Choose k random centroids (init="k-means++")
                    # Step 2 : Assign each point to the nearest cluster
                    # Step 3 : Recalculate centroids (mean of each cluster)
                    # Step 4 : Reassign points with the NEW centroids
                    # Step 5 : Repeat steps 3-4 until convergence (stability)
                    # Step 6 : Calculate WCSS = sum of squared distances of each point to its center
                    # Step 7 : Store WCSS in .inertia_
    .inertia_       # Get the WCSS value for this clustering
    for k in k_range
]

print("\n" + "="*50)
print("ELBOW METHOD RESULTS")
print("="*50)
 
print(f"\n{'k':<5} {'WCSS':<15} {'Reduction %':<15}")
print("-"*50)
 
for i, (k, wcss_val) in enumerate(zip(k_range, wcss)):
    if i == 0:
        print(f"{k:<5} {wcss_val:<15.0f} {'-':<15}")
    else:
        percent = ((wcss[i-1] - wcss_val) / wcss[i-1]) * 100
        print(f"{k:<5} {wcss_val:<15.0f} {int(percent)}%")
 
# Find optimal k
reductions = [((wcss1 - wcss2) / wcss1) * 100 for wcss1, wcss2 in zip(wcss[:-1], wcss[1:])]
optimal_k = reductions.index(max(reductions)) +2 # +2 to convert index to cluster position
 
print("\n" + "-"*50)
print(f"OPTIMAL: k = {optimal_k}")
print("="*50 + "\n")

plt.style.use("seaborn-v0_8")
plt.figure(figsize=(10, 6))

plt.plot(k_range, wcss, color="#4C72B0", linewidth=2, markersize=6)
plt.title("The Elbow Method")
plt.xlabel("Number of clusters")
plt.grid(True)

plt.tight_layout()

try:
    plt.show()
except KeyboardInterrupt:
    pass
finally:
    plt.close()