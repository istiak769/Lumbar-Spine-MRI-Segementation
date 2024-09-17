import SimpleITK as sitk
import os
import numpy as np
import cv2
import matplotlib.pyplot as plt

def visualize_sagittal_slices(image_path):
    # Load the image
    image = sitk.ReadImage(image_path)

    # Get the size of the image
    size = image.GetSize()
    x_size = size[0]

    # Visualize sagittal slices
    for x in range(x_size):
        # Extract the sagittal slice
        sagittal_slice = image[x, :, :]

        # Convert to numpy array
        sagittal_array = sitk.GetArrayViewFromImage(sagittal_slice)

        # Plot the slice
        plt.imshow(sagittal_array, cmap='gray')
        plt.title(f'Slice {x + 1}')
        plt.axis('off')
        plt.show()

def save_sagittal_slices(image_path, output_dir):
    # Load the image
    image = sitk.ReadImage(image_path)

    # Get the size of the image
    size = image.GetSize()
    x_size = size[0]

    # Define the target dimensions
    target_height = 620
    target_width = 512

    # Extract sagittal slices, rotate them, flip horizontally, resize them, and save them
    for x in range(x_size):
        # Extract the sagittal slice
        sagittal_slice = image[x,:,:]

        # Convert to numpy array
        sagittal_array = sitk.GetArrayViewFromImage(sagittal_slice)

        # Normalize intensity values
        sagittal_array = (sagittal_array - np.min(sagittal_array)) / (np.max(sagittal_array) - np.min(sagittal_array)) * 255

        # Convert to unsigned integer 8-bit
        sagittal_array = sagittal_array.astype(np.uint8)

        # Rotate the image 180 degrees
        rotated_slice = cv2.rotate(sagittal_array, cv2.ROTATE_180)

        # Flip horizontally
        flipped_slice = cv2.flip(rotated_slice, 1)

        # Resize the image
        resized_slice = cv2.resize(flipped_slice, (target_width, target_height))

        # Save the resized slice as PNG
        slice_filename = os.path.basename(image_path).split('.')[0] + f'_slice{x+1}.png'
        slice_path = os.path.join(output_dir, slice_filename)

        # Save the slice using OpenCV
        cv2.imwrite(slice_path, resized_slice)

        print(f"Saved sagittal slice {x+1}/{x_size} as {slice_filename}")

# Provide the path to the .mha image file and the output directory to save the slices
image_path = r"M:\499\New folder\Need to process\batch 1\masks\7_t1.mha"
output_dir = r"M:\499\New folder\Need to process\batch 1\masks\7_t1"

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Visualize the sagittal slices
#visualize_sagittal_slices(image_path)

# Save the sagittal slices
save_sagittal_slices(image_path, output_dir)
