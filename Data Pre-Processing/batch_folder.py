import os
import shutil

def create_batches(folder_path, batch_size=20):
    # List all items in the folder
    items = os.listdir(folder_path)
    # Sort the items for consistent ordering
    items.sort()
    num_items = len(items)
    num_batches = (num_items + batch_size - 1) // batch_size

    for batch_num in range(1, num_batches + 1):
        # Create batch folder
        batch_folder = os.path.join(folder_path, f"batch{batch_num}")
        os.makedirs(batch_folder, exist_ok=True)

        # Determine the range of items to move to this batch
        start_index = (batch_num - 1) * batch_size
        end_index = min(batch_num * batch_size, num_items)

        # Move items to batch folder
        for item_index in range(start_index, end_index):
            item = items[item_index]
            item_path = os.path.join(folder_path, item)
            shutil.move(item_path, batch_folder)

if __name__ == "__main__":
    # Insert the folder path here
    folder_path = r"M:/499/Dataset/Processed_v2/Unprocessed/t1/3D/masks"

    if os.path.isdir(folder_path):
        create_batches(folder_path)
        print("Batches created successfully!")
    else:
        print("Invalid folder path.")
