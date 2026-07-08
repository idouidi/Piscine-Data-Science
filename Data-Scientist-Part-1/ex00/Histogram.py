import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('Test_knight.csv')
df.columns = df.columns.str.strip()
columns = df.columns.tolist()

CUSTOM_CONFIG = {
    'Sensitivity': {'x': list(np.arange(10, 30, 5)), 'y': list(np.arange(0, 20, 5))},
    'Hability': {'x': list(np.arange(10, 40, 10)), 'y': list(np.arange(0, 12, 2))},
    'Strength': {'x': list(np.arange(50, 200, 50)), 'y': list(np.arange(0, 20, 5))},
    'Power': {'x': list(np.arange(500, 2500, 500)), 'y': list(np.arange(0, 25, 5))},
    'Agility': {'x': list(np.arange(0.050, 0.175, 0.025)), 'y': list(np.arange(0, 20, 5))},
    'Dexterity': {'x': list(np.arange(0.1, 0.4, 0.1)), 'y': list(np.arange(0, 20, 5))},
    'Awareness': {'x': list(np.arange(0.0, 0.5, 0.1)), 'y': list(np.arange(0, 25, 5))},
    'Prescience': {'x': list(np.arange(0.00, 0.25, 0.05)), 'y': list(np.arange(0, 25, 5))},
    'Reactivity': {'x': list(np.arange(0.15, 0.30, 0.05)), 'y': list(np.arange(0, 20, 5))},
    'Midi-chlorien': {'x': list(np.arange(0.06, 0.11, 0.02)), 'y': list(np.arange(0, 20, 5))},
    'Slash': {'x': list(np.arange(0.5, 2.0, 0.5)), 'y': list(np.arange(0, 25, 5))},
    'Push': {'x': list(np.arange(1, 4, 1)), 'y': list(np.arange(0, 20, 5))},
    'Pull': {'x': list(np.arange(2, 12, 2)), 'y': list(np.arange(0, 25, 5))},
    'Lightsaber': {'x': list(np.arange(0, 250, 50)), 'y': list(np.arange(0, 50, 10))},
    'Survival': {'x': list(np.arange(0.005, 0.025, 0.005)), 'y': list(np.arange(0, 30, 5))},
    'Repulse': {'x': list(np.arange(0.00, 0.15, 0.05)), 'y': list(np.arange(0, 30, 5))},
    'Friendship': {'x': list(np.arange(0.0, 0.2, 0.05)), 'y': list(np.arange(0, 25, 5))},
    'Blocking': {'x': list(np.arange(0.0, 0.04, 0.01)), 'y': list(np.arange(0, 15, 2.5))},
    'Deflection': {'x': list(np.arange(0.02, 0.1, 0.02)), 'y': list(np.arange(0, 30, 5))},
    'Mass': {'x': list(np.arange(0.000, 0.025, 0.005)), 'y': list(np.arange(0, 40, 10))},
    'Recovery': {'x': list(np.arange(10, 40, 5)), 'y': list(np.arange(0, 25, 5))},
    'Evade': {'x': list(np.arange(10, 60, 10)), 'y': list(np.arange(0, 20, 5))},
    'Stims': {'x': list(np.arange(100, 250, 50)), 'y': list(np.arange(0, 20, 5))},
    'Sprint': {'x': list(np.arange(1000, 4000, 1000)), 'y': list(np.arange(0, 30, 5))},
    'Combo': {'x': list(np.arange(0.10, 0.25, 0.05)), 'y': list(np.arange(0, 12, 2))},
    'Delay': {'x': list(np.arange(0.0, 1.0, 0.2)), 'y': list(np.arange(0, 20, 5))},
    'Attunement': {'x': list(np.arange(0.0, 1.0, 0.2)), 'y': list(np.arange(0, 15, 2.5))},
    'Empowered': {'x': list(np.arange(0.0, 0.4, 0.1)), 'y': list(np.arange(0, 20, 5))},
    'Burst': {'x': list(np.arange(0.2, 0.8, 0.2)), 'y': list(np.arange(0, 25, 5))},
    'Grasping': {'x': list(np.arange(0.10, 0.2, 0.05)), 'y': list(np.arange(0, 25, 5))},
}

plt.figure(figsize=(20, 18))

for idx, column in enumerate(columns, 1):
    # (6 rows x 5 columns)
    plt.subplot(6, 5, idx)
    plt.hist(df[column], bins=36, color='green', alpha=0.7, label='knight')
    plt.title(column, fontsize=10)
    plt.legend(loc='upper right', fontsize=8)
    plt.margins(x=0.1, y=0.1)

    # Apply custom ticks if defined for this column
    if column in CUSTOM_CONFIG:
        config = CUSTOM_CONFIG[column]
        plt.xticks(config['x'])
        plt.yticks(config['y'])

plt.tight_layout()

plt.savefig('histogram.png', dpi=300)

try:
    plt.show()
except KeyboardInterrupt:
    pass
finally:
    plt.close()