import pandas as pd
import numpy as np

np.random.seed(45)

df = pd.read_csv('./dataset/ISIC_2019_Training_GroundTruth.csv')  # Replace with your file path
target_classes = ["DF", "VASC", "AK", "SCC"]
# target_classes = ["DF", "VASC", "AKIEC"]

max_samples = 2500

class_columns = df.columns[1:-1]

for cls in class_columns:
    class_indices = df[df[cls] == 1].index

    if len(class_indices) > max_samples:
        keep_indices = np.random.choice(class_indices, max_samples, replace=False)

        drop_indices = list(set(class_indices) - set(keep_indices))
        df.drop(index=drop_indices, inplace=True)

df['UNK'] = 0.0
df.loc[df[target_classes].sum(axis=1) > 0, "UNK"] = 1
df.loc[df[target_classes].sum(axis=1) > 0, target_classes] = 0

df.drop(columns=target_classes, inplace=True)
df.to_csv('./dataset/new_2019.csv', index=False)
