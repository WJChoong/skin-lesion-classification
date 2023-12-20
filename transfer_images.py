import pandas as pd
from sklearn.utils import resample
import os
import shutil

# Load the dataset
file_path = './dataset/ISIC_2019_Training_GroundTruth.csv'  # Update with your file path
data = pd.read_csv(file_path)

# Change the label of AK, DF, VASC, SCC to UNK
data['UNK'] = data[['AK', 'DF', 'VASC', 'SCC']].sum(axis=1).clip(upper=1)
data.drop(['AK', 'DF', 'VASC', 'SCC', "UNK"], axis=1, inplace=True)

# Set random seed for reproducibility
seed = 42

# Downsample classes with more than 2500 images to 2500
downsampled_data = pd.DataFrame()
class_counts = data.drop('image', axis=1).sum().sort_values(ascending=False)

for class_name, count in class_counts.items():
    if count > 2500:
        class_data = data[data[class_name] == 1]
        downsampled_class_data = resample(class_data, replace=False, n_samples=2500, random_state=seed)
        downsampled_data = pd.concat([downsampled_data, downsampled_class_data], axis=0)
    else:
        class_data = data[data[class_name] == 1]
        downsampled_data = pd.concat([downsampled_data, class_data], axis=0)

# Save the new dataset to a CSV file
new_dataset_path = './dataset/2019_4_class.csv'  # Update with your desired path
downsampled_data.to_csv(new_dataset_path, index=False)

# Define the source and destination folders for the images
source_folder = './dataset/ISIC_2019_Training_Input'  # Update with your source folder path
destination_folder = './dataset/2019_4_class'  # Update with your destination folder path

# Create destination folder if it doesn't exist
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Copy images from the source folder to the new folder
for image_name in downsampled_data['image']:
    src_path = os.path.join(source_folder, image_name + '.jpg')
    dest_path = os.path.join(destination_folder, image_name + '.jpg')
    shutil.copy(src_path, dest_path)
