import pandas as pd

df = pd.read_csv('Train_knight.csv')
df.columns = df.columns.str.strip()

df['knight'] = df['knight'].str.strip().map({'Sith': 0, 'Jedi': 1})

correlation = df.corr()

knight_corr = correlation['knight'].sort_values(ascending=False)


for col, corr in knight_corr.items():
    print(f"{col:<13} {corr:>15.6f}")
