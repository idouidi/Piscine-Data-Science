import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('Train_knight.csv')
df.columns = df.columns.str.strip()
df['knight'] = df['knight'].astype(str).str.strip()

# Séparer par classe
jedi_data = df[df['knight'] == 'Jedi']
sith_data = df[df['knight'] == 'Sith']

columns = [col for col in df.columns if col != 'knight']

CUSTOM_CONFIG = {
    'Sensitivity': {'x': list(np.arange(10, 30, 5)), 'y': list(np.arange(0, 30, 5))},
    'Hability': {'x': list(np.arange(0, 50, 10)), 'y': list(np.arange(0, 40, 10))},
    'Strength': {'x': list(np.arange(50, 200, 50)), 'y': list(np.arange(0, 30, 5))},
    'Power': {'x': list(np.arange(1000, 2500, 1000)), 'y': list(np.arange(0, 30, 5))},
    'Agility': {'x': list(np.arange(0.050, 0.175, 0.025)), 'y': list(np.arange(0, 40, 10))},

    'Dexterity': {'x': list(np.arange(0.1, 0.4, 0.1)), 'y': list(np.arange(0, 40, 10))},
    'Awareness': {'x': list(np.arange(0.0, 0.5, 0.1)), 'y': list(np.arange(0, 60, 10))},
    'Prescience': {'x': list(np.arange(0.00, 0.25, 0.05)), 'y': list(np.arange(0, 30, 5))},
    'Reactivity': {'x': list(np.arange(0.10, 0.35, 0.05)), 'y': list(np.arange(0, 40, 10))},
    'Midi-chlorien': {'x': list(np.arange(0.06, 0.10, 0.02)), 'y': list(np.arange(0, 50, 10))},

    'Slash': {'x': list(np.arange(0, 4, 1)), 'y': list(np.arange(0, 40, 10))},
    'Push': {'x': list(np.arange(1, 6, 1)), 'y': list(np.arange(0, 40, 10))},
    'Pull': {'x': list(np.arange(0, 25, 5)), 'y': list(np.arange(0, 40, 10))},
    'Lightsaber': {'x': list(np.arange(0, 500, 200)), 'y': list(np.arange(0, 50, 10))},
    'Survival': {'x': list(np.arange(0.01, 0.04, 0.01)), 'y': list(np.arange(0, 40, 10))},

    'Repulse': {'x': list(np.arange(0.00, 0.15, 0.05)), 'y': list(np.arange(0, 60, 10))},
    'Friendship': {'x': list(np.arange(0.0, 0.5, 0.1)), 'y': list(np.arange(0, 150, 25))},
    'Blocking': {'x': list(np.arange(0.00, 0.06, 0.02)), 'y': list(np.arange(0, 60, 10))},
    'Deflection': {'x': list(np.arange(0.02, 0.10, 0.02)), 'y': list(np.arange(0, 50, 10))},
    'Mass': {'x': list(np.arange(0.00, 0.04, 0.01)), 'y': list(np.arange(0, 100, 20))},

    'Recovery': {'x': list(np.arange(10, 40, 10)), 'y': list(np.arange(0, 30, 5))},
    'Evade': {'x': list(np.arange(20, 60, 10)), 'y': list(np.arange(0, 30, 5))},
    'Stims': {'x': list(np.arange(50, 300, 50)), 'y': list(np.arange(0, 30, 5))},
    'Sprint': {'x': list(np.arange(1000, 5000, 1000)), 'y': list(np.arange(0, 40, 10))},
    'Combo': {'x': list(np.arange(0.10, 0.25, 0.05)), 'y': list(np.arange(0, 40, 10))},

    'Delay': {'x': list(np.arange(0.00, 1.25, 0.25)), 'y': list(np.arange(0, 40, 10))},
    'Attunement': {'x': list(np.arange(0.0, 1.2, 0.5)), 'y': list(np.arange(0, 50, 10))},
    'Empowered': {'x': list(np.arange(0.0, 0.4, 0.1)), 'y': list(np.arange(0, 40, 10))},
    'Burst': {'x': list(np.arange(0.2, 0.8, 0.2)), 'y': list(np.arange(0, 30, 5))},
    'Grasping': {'x': list(np.arange(0.05, 0.25, 0.05)), 'y': list(np.arange(0, 50, 10))},
}

plt.figure(figsize=(20, 18))

for idx, column in enumerate(columns, 1):
    # (6 rows x 5 columns)
    plt.subplot(6, 5, idx)

    plt.hist(jedi_data[column].dropna(), bins=36, color="#5656E6", alpha=0.6, label='Jedi')
    plt.hist(sith_data[column].dropna(), bins=36, color="#F49E9E", alpha=0.6, label='Sith')

    plt.title(column, fontsize=10)
    plt.legend(loc='upper right', fontsize=8)

    # Apply custom ticks if defined for this column
    if column in CUSTOM_CONFIG:
        config = CUSTOM_CONFIG[column]
        plt.xticks(config['x'])
        plt.yticks(config['y'])

plt.tight_layout()

plt.savefig('histogram_comparison.png', dpi=300)

try:
    plt.show()
except KeyboardInterrupt:
    pass
finally:
    plt.close()