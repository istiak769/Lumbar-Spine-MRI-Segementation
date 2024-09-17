import os
import shutil

# Function to create folders for each image type
def create_folders(image_names):
    folders = set()
    for name in image_names:
        folder_name = name.split("_slice")[0]  # Extracting folder name
        folders.add(folder_name)
    for folder in folders:
        os.makedirs(os.path.join(folder_location, folder), exist_ok=True)

# Function to move images to their corresponding folders
def move_images(image_names):
    for name in image_names:
        folder_name = name.split("_slice")[0]  # Extracting folder name
        shutil.move(os.path.join(folder_location, name), os.path.join(folder_location, folder_name))

# Specify the folder location
folder_location = "M:/499/Dataset/Processed_v2/Unprocessed/t1/3d_2d/masks/axis Issues"

# Get all PNG files in the specified directory
png_files = [file for file in os.listdir(folder_location) if file.endswith(".png")]

# Create folders for each image type
create_folders(png_files)

# Move images to their corresponding folders
move_images(png_files)

