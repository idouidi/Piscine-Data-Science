import matplotlib.pyplot as plt
import numpy as np


with open('truth.txt', 'r') as f:
    truth = f.read().splitlines()

with open('predictions.txt', 'r') as f:
    predictions = f.read().splitlines()

# Encode: Jedi=0, Sith=1
truth_encoded = [0 if label == 'Jedi' else 1 for label in truth]
pred_encoded = [0 if label == 'Jedi' else 1 for label in predictions]

cm = [[0, 0],
      [0, 0]]

for i in range(len(truth_encoded)):
    true_label = truth_encoded[i]
    pred_label = pred_encoded[i]
    cm[true_label][pred_label] += 1

# Extract values for [[TP, FN], [FP, TN]] format
TP = cm[0][0]  # Actual Jedi predicted as Jedi
FN = cm[0][1]  # Actual Jedi predicted as Sith
FP = cm[1][0]  # Actual Sith predicted as Jedi
TN = cm[1][1]  # Actual Sith predicted as Sith

total = sum(sum(row) for row in cm)

jedi_precision = TP / (TP + FP) if (TP + FP) > 0 else 0
jedi_recall = TP / (TP + FN) if (TP + FN) > 0 else 0
jedi_f1 = 2 * (jedi_precision * jedi_recall) / (jedi_precision + jedi_recall) if (jedi_precision + jedi_recall) > 0 else 0
jedi_total = TP + FN

sith_precision = TN / (TN + FN) if (TN + FN) > 0 else 0
sith_recall = TN / (TN + FP) if (TN + FP) > 0 else 0
sith_f1 = 2 * (sith_precision * sith_recall) / (sith_precision + sith_recall) if (sith_precision + sith_recall) > 0 else 0
sith_total = TN + FP

# Overall accuracy
accuracy = (TP + TN) / total * 100

print("="*70)
print("CONFUSION MATRIX ANALYSIS")
print("="*70)
print(f"\n{'':<15} {'Precision':<15} {'Recall':<15} {'F1-Score':<15} {'Total':<10}")
print("-"*70)
print(f"{'Jedi':<15} {jedi_precision:<15.2f} {jedi_recall:<15.2f} {jedi_f1:<15.2f} {jedi_total:<10}")
print(f"{'Sith':<15} {sith_precision:<15.2f} {sith_recall:<15.2f} {sith_f1:<15.2f} {sith_total:<10}")
print("-"*70)
print(f"{'Accuracy':<15} {'':<15} {'':<15} {accuracy/100:<15.2f} {total:<10}")
print("="*70)

print(f"[[{TP} {FN}]")
print(f" [{FP} {TN}]]")
print("="*70)

plt.figure(figsize=(8, 6))

data = np.array([[TP, FN],
                 [FP, TN]])
# Display heatmap
plt.imshow(data, cmap='viridis', aspect='auto')

plt.xticks([0, 1], ['0', '1'], fontsize=12)
plt.yticks([0, 1], ['0', '1'], fontsize=12)
plt.xlabel('Predicted', fontsize=12, fontweight='bold')
plt.ylabel('Actual', fontsize=12, fontweight='bold')

for i in range(2):
    for j in range(2):
        if i == 1 and j == 0:
            plt.text(j, i, data[i, j], color="black", fontsize=24)
        else:
            plt.text(j, i, data[i, j], color="white", fontsize=24)

# Add colorbar
cbar = plt.colorbar()

plt.tight_layout()
try:
    plt.show()
except KeyboardInterrupt:
    pass
finally:
    plt.close()