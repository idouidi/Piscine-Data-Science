import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

df = pd.read_csv('Train_knight.csv')
df = df.drop('knight', axis=1)

df_scaled = StandardScaler().fit_transform(df)

# Calculate variance 
# Variance = Sum of (Xi - Mean)² / n
# - Xi = each individual value
# - Mean = mean of all values
# - (Xi - Mean)² = squared deviation from mean (always positive)
# - Sum of all squared deviations / n = total's skill data

# PCA (Principal Component Analysis)
# Finds new dimensions that maximize variance, removing redundancy.
# Set Principal Compoents that can group the data , while keeping the most information possible. 
# (30 attributes → 3 components that explain 90% of information)

df_pca = PCA().fit(df_scaled)
explained_variance = df_pca.explained_variance_
total_variance = explained_variance.sum()
variances = (explained_variance / total_variance) * 100

print(f"Variances (Percentage):\n{variances}\n")

cumul_variance = np.cumsum(variances)

print(f"Cumulative Variances (Percentage):\n{cumul_variance}")

plt.figure(figsize=(8, 6))
plt.plot(cumul_variance)
plt.ylabel("Explained variance(%)")
plt.xlabel("Number of components")
# plt.grid()
plt.tight_layout()

try:
    plt.show()
except KeyboardInterrupt:
    pass
finally:
    plt.close()