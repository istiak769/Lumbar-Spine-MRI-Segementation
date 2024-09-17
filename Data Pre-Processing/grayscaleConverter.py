import os
from PIL import Image

# Path to the folder containing grayscale images
input_folder = "rgb_mask"

# Path to the folder where you want to save PNG images
output_folder = "gray_mask"

# Ensure the output folder exists, if not create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# List all files in the input folder
files = os.listdir(input_folder)

# Loop through each file in the folder
for file in files:
    # Check if the file is an image
    if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
        # Open the image
        img_path = os.path.join(input_folder, file)
        img = Image.open(img_path)
        
        # Convert the image to grayscale if it's not already
        if img.mode != "L":
            img = img.convert("L")
        
        # Save the image as PNG in the output folder
        img_name = os.path.splitext(file)[0] + ".png"
        output_path = os.path.join(output_folder, img_name)
        img.save(output_path)
        print(f"{file} converted and saved as {img_name}")

print("Conversion completed!")
