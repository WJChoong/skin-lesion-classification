import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(45)

# Load the CSV file
df = pd.read_csv('./dataset/ISIC2018_Task3_Test_GroundTruth.csv')  # Replace with your file path

# List of target classes to downsample
# target_classes = ["DF", "VASC", "AK", "SCC"]
target_classes = ["DF", "VASC", "AKIEC"]

# Maximum number of samples for each class
max_samples = 2000

# Columns representing the classes (excluding 'image' and 'UNK' columns)
class_columns = df.columns[1:-1]

# Downsampling classes with more than max_samples images
for cls in class_columns:
    # Get indices of all rows for the class
    class_indices = df[df[cls] == 1].index

    # If the number of samples is more than the max_samples, downsample
    if len(class_indices) > max_samples:
        # Randomly choose max_samples indices to keep
        keep_indices = np.random.choice(class_indices, max_samples, replace=False)

        # Drop the rest
        drop_indices = list(set(class_indices) - set(keep_indices))
        df.drop(index=drop_indices, inplace=True)

# Changing the label of the remaining images of specified classes to UNK
df['UNK'] = 0.0
df.loc[df[target_classes].sum(axis=1) > 0, "UNK"] = 1
df.loc[df[target_classes].sum(axis=1) > 0, target_classes] = 0

# Drop the target classes from the DataFrame
df.drop(columns=target_classes, inplace=True)

# Save the modified dataframe to a new CSV file
df.to_csv('./dataset/val_class.csv', index=False)
