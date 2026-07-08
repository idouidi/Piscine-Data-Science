import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

df_train = pd.read_csv('Train_knight.csv')
df_test = pd.read_csv('Test_knight.csv')

df_train.columns = df_train.columns.str.strip()
df_test.columns = df_test.columns.str.strip()

# CHANGE StandardScaler → MinMaxScaler
# MinMaxScaler scales and translates each feature individually such that it is in the given range on the training set, e.g. between zero and one.
scaler = MinMaxScaler()
df_train_scaled = pd.DataFrame(
    scaler.fit_transform(df_train.drop('knight', axis=1)),
    columns=df_train.columns[df_train.columns != 'knight'],
)

df_test_scaled = pd.DataFrame(
    scaler.transform(df_test),
    columns=df_test.columns
)

print("="*60)
print("STANDARDIZED TRAIN DATA")
print("="*60)
print(df_train_scaled.head(2))
print("\n" + "="*60)

print("STANDARDIZED TEST DATA")
print("="*60)
print(df_test_scaled.head(2))
print("\n")

attr1, attr2 = 'Survival', 'Deflection'
jedi = df_train_scaled[df_train['knight'].str.strip() == 'Jedi']
sith = df_train_scaled[df_train['knight'].str.strip() == 'Sith']

plt.figure(figsize=(8, 6))
plt.scatter(sith[attr1], sith[attr2], color='#E85D75', label='Sith', alpha=0.6, s=50)
plt.scatter(jedi[attr1], jedi[attr2], color='#6495ED', label='Jedi', alpha=0.6, s=50)
plt.xlabel(f'{attr1}')
plt.ylabel(f'{attr2}')
plt.legend(loc='upper right')

plt.tight_layout()
try:
    plt.show()
except KeyboardInterrupt:
    pass
finally:
    plt.close()