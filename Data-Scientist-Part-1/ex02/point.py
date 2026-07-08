import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('Train_knight.csv')
df.columns = df.columns.str.strip()
df['knight'] = df['knight'].str.strip()

df_test = pd.read_csv('Test_knight.csv')
df_test.columns = df_test.columns.str.strip()

df_corr = df.copy()
df_corr['knight'] = df_corr['knight'].map({'Sith': 0, 'Jedi': 1})
knight_corr = df_corr.corr()['knight'].drop('knight').sort_values(ascending=False)

# top 5 best
print("="*60)
print("TOP 5 STRONGEST CORRELATIONS")
print("="*60)
for i, (attr, corr) in enumerate(knight_corr.head(5).items(), 1):
    print(f"{i}. {attr:<20} {corr:+.6f}")
print("="*60 + "\n")

# top 5 worst
print("="*60)
print("TOP 5 WEAKEST CORRELATIONS")
print("="*60)
for i, (attr, corr) in enumerate(knight_corr.tail(5).iloc[::-1].items(), 1):
    print(f"{i}. {attr:<20} {corr:+.6f}")
print("="*60 + "\n")

jedi = df[df['knight'] == 'Jedi']
sith = df[df['knight'] == 'Sith']

# Best attributes (the exo is outdated, best match exercie is Empowered and Stims)
attr1_best, attr2_best = 'Empowered', 'Prescience'

# Worst attributes the exo is outdated, best match exercie is Push and Deflection)
attr1_worst, attr2_worst = 'Survival', 'Deflection'

# Create 2 subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))


axes[0, 0].scatter(sith[attr1_best], sith[attr2_best], color='#E85D75', label='Sith', alpha=0.4)
axes[0, 0].scatter(jedi[attr1_best], jedi[attr2_best], color='#6495ED', label='Jedi', alpha=0.4)
axes[0, 0].set_xlabel(attr1_best)
axes[0, 0].set_ylabel(attr2_best)
axes[0, 0].legend(loc='upper left')

axes[0, 1].scatter(sith[attr1_worst], sith[attr2_worst], color='#E85D75', label='Sith', alpha=0.4)
axes[0, 1].scatter(jedi[attr1_worst], jedi[attr2_worst], color='#6495ED', label='Jedi', alpha=0.4)
axes[0, 1].set_xlabel(attr1_worst)
axes[0, 1].set_ylabel(attr2_worst)
axes[0, 1].legend(loc='upper right')

axes[1, 0].scatter(df_test[attr1_best], df_test[attr2_best], color='green', alpha=0.4)
axes[1, 0].set_xlabel(attr1_best)
axes[1, 0].set_ylabel(attr2_best)

axes[1, 1].scatter(df_test[attr1_worst], df_test[attr2_worst], color='green', alpha=0.4)
axes[1, 1].set_xlabel(attr1_worst)
axes[1, 1].set_ylabel(attr2_worst)

plt.tight_layout()

try:
    plt.show()
except KeyboardInterrupt:
    pass
finally:
    plt.close()