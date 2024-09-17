import os

def delete_images_except_range(folder_path, start_image, end_image):
    start_index = int(start_image.split('_')[-1][5:])
    end_index = int(end_image.split('_')[-1][5:])
    
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.png'):  # Assuming images have .png extension
            index = int(file_name.split('_')[-1].split('.')[0][5:])
            if index < start_index or index > end_index:
                os.remove(os.path.join(folder_path, file_name))
                print(f"Deleted: {file_name}")

def iterate_through_folders_and_delete(root_folder, image_ranges):
    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path):
            folder_prefix = folder_name.split('_')[0]
            for start_image, end_image in image_ranges:
                if folder_prefix == start_image.split('_')[0]:
                    delete_images_except_range(folder_path, start_image, end_image)

# Change the root_folder to the path where your server folders are located
root_folder = "M:\test"
image_ranges = [
    ("2_t2_slice8", "2_t2_slice10"),
    ("5_t2_slice1", "5_t2_slice17"),
    ("6_t2_slice1", "6_t2_slice16"),
    ("8_t2_slice1", "8_t2_slice15"),
    ("9_t2_slice1", "9_t2_slice19"),
    ("10_t2_slice1", "10_t2_slice15"),
    
    
    
]
iterate_through_folders_and_delete(root_folder, image_ranges)

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image_path = 'M:/Research/Book/Application of Linear Algebra/Images/CAT_Original.png'  # Replace with your image path
image = Image.open(image_path)

# Resize the image to 36x36 pixels
resized_image = image.resize((36, 36))

# Convert the image to grayscale
gray_image = resized_image.convert('L')

# Convert grayscale image to a NumPy array
gray_image_array = np.array(gray_image)

# Print the entire array without wrapping
np.set_printoptions(threshold=np.inf, linewidth=np.inf)
print(gray_image_array)

# Display the shape of the grayscale image
print(f"Grayscale image shape (height, width): {gray_image_array.shape}")

# Display the grayscale image using matplotlib
plt.imshow(gray_image_array, cmap='gray')
plt.title('Grayscale Image Representation (36x36)')
plt.axis('off')  # Hide axis
plt.show()



