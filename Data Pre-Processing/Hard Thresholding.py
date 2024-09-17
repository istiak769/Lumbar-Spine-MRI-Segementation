import os
from PIL import Image
from collections import Counter

def get_unique_pixel_colors(image_path):
    # Open the image
    image = Image.open(image_path)
    
    # Get the pixel colors
    pixels = list(image.getdata())

    # Count the occurrences of each pixel color
    color_count = Counter(pixels)
    
    # Return unique pixel colors and their counts
    return color_count

def replace_colors_with_red(image):
    # Get the width and height of the image
    width, height = image.size

    # Convert the image to RGB mode (if not already in RGB)
    image = image.convert("RGB")

    # Create a new image to store the modified pixels
    new_image = Image.new("RGB", (width, height))

    # Iterate over each pixel in the image
    for x in range(width):
        for y in range(height):
            # Get the RGB values of the pixel
            pixel = image.getpixel((x, y))

            # Define the color ranges to be replaced with red
            if all(1 <= value <= 10 for value in pixel):
                new_image.putpixel((x, y), (255, 0, 0))  # Replace with red
            elif all(90 <= value <= 180 for value in pixel):
                new_image.putpixel((x, y), (0, 255, 0))  # Replace with green
            elif all(180 <= value <= 255 for value in pixel):
                new_image.putpixel((x, y), (0, 0, 255))  # Replace with blue
            else:
                 new_image.putpixel((x, y), (0, 0, 0))  # Replace with black

    return new_image

def replace_with_neighbor_color(image):
    # Get the width and height of the image
    width, height = image.size

    # Convert the image to RGB mode
    image = image.convert("RGB")

    # Create a new image to store the modified pixels
    new_image = Image.new("RGB", (width, height))

    # Iterate over each pixel in the image
    for x in range(width):
        for y in range(height):
            # Get the RGB value of the current pixel
            current_pixel = image.getpixel((x, y))

            # Check if any adjacent pixels have the same color
            adjacent_colors = []
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    # Skip the current pixel
                    if dx == 0 and dy == 0:
                        continue
                    # Calculate the coordinates of the adjacent pixel
                    nx, ny = x + dx, y + dy
                    # Ensure the adjacent pixel is within the image bounds
                    if 0 <= nx < width and 0 <= ny < height:
                        adjacent_pixel = image.getpixel((nx, ny))
                        if adjacent_pixel == current_pixel:
                            adjacent_colors.append(adjacent_pixel)

            # If any adjacent pixel has the same color, replace current pixel with that color
            if adjacent_colors:
                new_image.putpixel((x, y), adjacent_colors[0])
            else:
                # If no adjacent pixel has the same color, replace with black
                new_image.putpixel((x, y), (0, 0, 0))

    return new_image

def remove_outline(image):
    # Get the width and height of the image
    width, height = image.size

    # Convert the image to RGB mode
    image = image.convert("RGB")

    # Create a new image to store the modified pixels
    new_image = Image.new("RGB", (width, height))

    # Iterate over each pixel in the image
    for x in range(width):
        for y in range(height):
            # Get the RGB value of the current pixel
            current_pixel = image.getpixel((x, y))

            # Get the most common color in the neighboring pixels
            neighbor_colors = []
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                # Check if neighboring pixel is within image bounds
                if 0 <= nx < width and 0 <= ny < height:
                    neighbor_pixel = image.getpixel((nx, ny))
                    neighbor_colors.append(neighbor_pixel)

            # Count occurrences of each neighboring color
            color_counter = Counter(neighbor_colors)

            # Get the most common color among neighbors
            most_common_color = color_counter.most_common(1)[0][0]

            # If the current pixel is different from the most common color, replace it
            if current_pixel != most_common_color:
                new_image.putpixel((x, y), most_common_color)
            else:
                # Otherwise, keep the color of the current pixel
                new_image.putpixel((x, y), current_pixel)

    return new_image

def replace_border_color(image):
    # Get the width and height of the image
    width, height = image.size

    # Convert the image to RGB mode
    image = image.convert("RGB")

    # Create a new image to store the modified pixels
    new_image = Image.new("RGB", (width, height))

    # Iterate over each pixel in the image
    for x in range(width):
        for y in range(height):
            # Get the RGB value of the current pixel
            current_pixel = image.getpixel((x, y))

            # Get the colors of adjacent pixels
            neighbor_colors = []
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    # Check if neighboring pixel is within image bounds and not the current pixel
                    if (0 <= nx < width and 0 <= ny < height) and (nx, ny) != (x, y):
                        neighbor_pixel = image.getpixel((nx, ny))
                        neighbor_colors.append(neighbor_pixel)

            # Count occurrences of each neighboring color
            color_counter = Counter(neighbor_colors)

            # Get the most common color among neighbors
            most_common_color = color_counter.most_common(1)[0][0]

            # If both adjacent pixels are of a different color, replace current pixel with the most common color among neighbors
            if len(color_counter) >= 2 and current_pixel != most_common_color:
                new_image.putpixel((x, y), most_common_color)
            else:
                # Otherwise, keep the color of the current pixel
                new_image.putpixel((x, y), current_pixel)

    return new_image

def replace_single_pixels(image):
    # Get the width and height of the image
    width, height = image.size

    # Convert the image to RGB mode
    image = image.convert("RGB")

    # Create a new image to store the modified pixels
    new_image = Image.new("RGB", (width, height))

    # Iterate over each pixel in the image
    for x in range(width):
        for y in range(height):
            # Get the RGB value of the current pixel
            current_pixel = image.getpixel((x, y))

            # Check if the current pixel is a single pixel of a different color compared to its neighbors
            if is_single_pixel(current_pixel, image, x, y):
                # Get the most common color among neighboring pixels
                most_common_color = get_most_common_neighbor_color(image, x, y)

                # Replace the current pixel with the most common color among neighbors
                new_image.putpixel((x, y), most_common_color)
            else:
                # Keep the color of the current pixel
                new_image.putpixel((x, y), current_pixel)

    return new_image

def is_single_pixel(pixel, image, x, y):
    # Get the colors of adjacent pixels
    neighbor_colors = [image.getpixel((x + dx, y + dy)) for dx in range(-1, 2) for dy in range(-1, 2)
                       if (dx != 0 or dy != 0) and 0 <= x + dx < image.width and 0 <= y + dy < image.height]

    # Count occurrences of each neighboring color
    color_counter = Counter(neighbor_colors)

    # Check if the current pixel is a single pixel of a different color compared to its neighbors
    return color_counter[pixel] == 0

def get_most_common_neighbor_color(image, x, y):
    # Get the colors of adjacent pixels
    neighbor_colors = [image.getpixel((x + dx, y + dy)) for dx in range(-1, 2) for dy in range(-1, 2)
                       if (dx != 0 or dy != 0) and 0 <= x + dx < image.width and 0 <= y + dy < image.height]

    # Count occurrences of each neighboring color
    color_counter = Counter(neighbor_colors)

    # Get the most common color among neighboring pixels
    most_common_color = color_counter.most_common(1)[0][0]

    return most_common_color
def replace_green_blue_with_red(image):
    # Get the width and height of the image
    width, height = image.size

    # Convert the image to RGB mode
    image = image.convert("RGB")

    # Flag to check if red color is present
    red_present = False

    # Flag to check if green or blue color is present
    green_blue_present = False

    # Iterate over each pixel in the image
    for x in range(width):
        for y in range(height):
            # Get the RGB value of the current pixel
            r, g, b = image.getpixel((x, y))

            # Check if red color is present
            if r != 0:
                red_present = True

            # Check if green or blue color is present
            if g != 0 or b != 0:
                green_blue_present = True

            # If both red and green/blue colors are present, no need to check further
            if red_present and green_blue_present:
                break
        if red_present and green_blue_present:
            break

    # If red color is present, no need to do anything
    if red_present:
        return image

    # If green or blue color is present but not red color, replace with red
    if green_blue_present:
        new_image = Image.new("RGB", (width, height))
        for x in range(width):
            for y in range(height):
                r, g, b = image.getpixel((x, y))
                if g != 0 or b != 0:
                    new_image.putpixel((x, y), (255, 0, 0))  # Replace with red
                else:
                    new_image.putpixel((x, y), (r, g, b))
        return new_image

    # If no green or blue color is present, return the original image
    return image
def process_images_in_folder(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get a list of all files in the input folder
    input_files = os.listdir(input_folder)

    # Process each image file
    for file_name in input_files:
        # Construct the full path to the input image
        input_image_path = os.path.join(input_folder, file_name)
        
        # Construct the full path to the output image
        output_image_path = os.path.join(output_folder, file_name)

        # Check if the output image already exists
        if os.path.exists(output_image_path):
            print(f"Skipping {file_name} as it already exists in the output folder.")
            continue

        # Open the image
        image = Image.open(input_image_path)

        # Apply the image processing functions
        image = replace_colors_with_red(image)
        image = replace_with_neighbor_color(image)
        image = remove_outline(image)
        image = replace_border_color(image)
        image = replace_single_pixels(image)
        image = replace_green_blue_with_red(image)

        # Save the modified image
        image.save(output_image_path)
        print(f"{file_name} processed and saved in the output folder.")

# Example usage:
input_folder = "demo"
output_folder = "demo_mask"
process_images_in_folder(input_folder, output_folder)
print("All images processed and saved in the output folder!")
