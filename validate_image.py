import pandas as pd
import os

# Load the CSV file with absolute path
csv_path = './dataset/val_class.csv'
df = pd.read_csv(csv_path)

# Path to the directory containing the images with absolute path
images_directory = './dataset/ISIC2018_Task3_Test_Input'

# File extension to append
file_extension = '.jpg'  # Change this if your images use a different extension

# Function to check image existence and print the path for all images
def check_image_existence(image_name):
    full_path = os.path.join(images_directory, image_name.strip() + file_extension)
    exists = os.path.exists(full_path)
    print(f"Checking: {full_path}, Exists: {exists}")
    return exists

# Checking which images exist
df['image_exists'] = df['image'].apply(check_image_existence)

# Displaying the first few rows of the dataframe to verify the results
print(df.head())

# Print total length of the dataframe
print("Total number of images:", len(df))

df_filtered = df[df['image_exists'] == False]
print(df_filtered.head())
print(len(df_filtered))
