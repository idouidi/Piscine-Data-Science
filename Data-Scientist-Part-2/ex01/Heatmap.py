import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Train_knight.csv')
df.columns = df.columns.str.strip()

df['knight'] = df['knight'].map({'Jedi': 0, 'Sith': 1})

corr = df.corr()


plt.figure(figsize=(11, 8))

plt.xticks(range(len(corr.columns)), corr.columns, fontsize=9, rotation=90)
plt.yticks(range(len(corr.columns)), corr.columns, fontsize=9)
plt.imshow(corr, cmap='magma')

cbar = plt.colorbar()
plt.tight_layout()

try:
    plt.show()
except KeyboardInterrupt:
    pass
finally:
    plt.close()
