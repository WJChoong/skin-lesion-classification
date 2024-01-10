import pandas as pd
import os

csv_path = './dataset/new_2019.csv'
df = pd.read_csv(csv_path)

images_directory = './dataset/new_2019_images'

file_extension = '.jpg' 

def check_image_existence(image_name):
    full_path = os.path.join(images_directory, image_name.strip() + file_extension)
    exists = os.path.exists(full_path)
    print(f"Checking: {full_path}, Exists: {exists}")
    return exists

df['image_exists'] = df['image'].apply(check_image_existence)

print(df.head())
print("Total number of images:", len(df))

df_filtered = df[df['image_exists'] == False]
print(df_filtered.head())
print(len(df_filtered))
