import os
import shutil
import pandas as pd

def move_images(csv_file_path, source_folder, destination_folder, file_extension='.jpg'):
    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    moved_count = 0
    missing_count = 0

    for image_name in df['image']:
        full_image_name = f"{image_name}{file_extension}"

        source_path = os.path.join(source_folder, full_image_name)
        destination_path = os.path.join(destination_folder, full_image_name)

        if os.path.exists(source_path):
            shutil.move(source_path, destination_path)
            moved_count += 1
        else:
            print(f"File not found: {source_path}")
            missing_count += 1

    return moved_count, missing_count

source_folder_path = './dataset/ISIC_2019_Training_Input'  
destination_folder_path = './dataset/new_2019_images'

moved_files, missing_files = move_images('./dataset/new_2019.csv', source_folder_path, destination_folder_path)

print(f"Moved {moved_files} files. {missing_files} files were missing.")
