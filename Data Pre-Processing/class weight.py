from sklearn.utils.class_weight import compute_class_weight
import cv2
import numpy as np

# Load the label mask
label_mask_path = 'M:/499/Dataset/Processed/Processed/L/L/t2/masks/1_t2/1_t2_slice28.png'
label_mask = cv2.imread(label_mask_path, cv2.IMREAD_GRAYSCALE)

# Get the unique classes present in the label mask
unique_classes = np.unique(label_mask)

# Map the unique classes to the desired class names
class_mapping = {class_label: class_name for class_name, class_label in enumerate(unique_classes)}

# Map the label mask using the class mapping
mapped_label_mask = np.vectorize(class_mapping.get)(label_mask)

# Compute class weights
classes = np.unique(mapped_label_mask)
class_weights = compute_class_weight(class_weight='balanced', classes=classes, y=mapped_label_mask.flatten())

# Convert class weights to a dictionary
class_weights_dict = {class_name: weight for class_name, weight in zip(classes, class_weights)}
print("Class weights dictionary:", class_weights_dict)



from sklearn.utils.class_weight import compute_class_weight
import cv2
import numpy as np
import os

# Function to calculate class weights for a single image
def calculate_class_weights(image_path):
    # Load the label mask
    label_mask = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Get the unique classes present in the label mask
    unique_classes = np.unique(label_mask)

    # Map the unique classes to the desired class names
    class_mapping = {class_label: class_name for class_name, class_label in enumerate(unique_classes)}

    # Map the label mask using the class mapping
    mapped_label_mask = np.vectorize(class_mapping.get)(label_mask)

    # Compute class weights
    classes = np.unique(mapped_label_mask)
    class_weights = compute_class_weight(class_weight='balanced', classes=classes, y=mapped_label_mask.flatten())

    # Convert class weights to a dictionary
    class_weights_dict = {class_name: weight for class_name, weight in zip(classes, class_weights)}
    return class_weights_dict

# Folder containing images
folder_path = 'M:/499/Dataset/Processed/Processed/masks'

# List all files in the folder
image_files = os.listdir(folder_path)

# Calculate class weights for each image
for image_file in image_files:
    # Check if the file is an image (you may need to adjust this condition based on your file naming convention)
    if image_file.endswith('.png') or image_file.endswith('.jpg'):
        image_path = os.path.join(folder_path, image_file)
        class_weights = calculate_class_weights(image_path)
        print("Class weights for", image_file, ":", class_weights)
