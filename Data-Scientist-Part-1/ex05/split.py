import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv('Train_knight.csv')
df.columns = df.columns.str.strip()

# Split: 70% training, 30% validation
# test_size=0.30 means 30% of the data will be used for validation, and the remaining 70% will be used for training.
# random_state=42 is used to ensure that the split is reproducible. This means that every time you run the code with the same random_state, you'll get the same split of data.
training, validation = train_test_split(df, test_size=0.30, random_state=42)

# Save
training.to_csv('Training_knight.csv', index=False)
validation.to_csv('Validation_knight.csv', index=False)

print("="*60)
print("SPLIT RESULTS: 70% TRAINING / 30% VALIDATION")
print("="*60)
print(f"\nTraining_knight.csv: {len(training)} rows ({len(training)/len(df)*100:.1f}%)")
print(f"  - Jedi: {len(training[training['knight'].str.strip() == 'Jedi'])}")
print(f"  - Sith: {len(training[training['knight'].str.strip() == 'Sith'])}")

print(f"\nValidation_knight.csv: {len(validation)} rows ({len(validation)/len(df)*100:.1f}%)")
print(f"  - Jedi: {len(validation[validation['knight'].str.strip() == 'Jedi'])}")
print(f"  - Sith: {len(validation[validation['knight'].str.strip() == 'Sith'])}")
print("="*60)
