import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

# Cell parameters
CELL_SIZE = 34  # Cell size in pixels
CELL_SPACING = 2  # Space between cells
OFFSET = 3  # Offset to center the grid
SSIM_THRESHOLD = 0.6  # SSIM threshold to consider two images as identical

IMAGE_DIR = "images"

BOARD_SIZES = [(9, 9), (11, 12), (13, 15), (14, 18), (16, 20)]

# def euclidean_distance(color1, color2):
#     # Calculate the Euclidean distance between two colors
#     return np.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)))
#
#
# def analyze_cell_color(image, cell_x, cell_y, cell_size):
#     """
#     Analyze the average color of the 9 middle pixels of a cell and find the closest target color.
#
#     Parameters:
#         image (numpy.ndarray): The image containing the cells.
#         cell_x (int): X-coordinate of the cell's top-left corner.
#         cell_y (int): Y-coordinate of the cell's top-left corner.
#         cell_size (int): Size of each cell.
#         target_colors (dict): Dictionary mapping integers to target BGR colors.
#
#     Returns:
#         int: The integer representing the closest color from target_colors.
#     """
#     # Calculate the middle point of the cell
#     mid_x = cell_x + cell_size // 2
#     mid_y = cell_y + cell_size // 2
#
#     # Define a 3x3 region around the middle pixel and compute the average color
#     pixel_sum = np.array([0, 0, 0], dtype=int)  # To accumulate BGR values
#
#     for dy in range(-2, 3):  # -1, 0, 1
#         for dx in range(-2, 3):  # -1, 0, 1
#             pixel = image[mid_y + dy, mid_x + dx]
#             pixel_sum += pixel  # Accumulate BGR values
#
#     # Calculate the average color
#     average_color = tuple((pixel_sum // 25).tolist())
#
#     # Allow multiple colors per key
#     target_colors = {
#         -1: [(41, 58, 77), (45, 63, 84)],  # Dirt
#         0: [(28, 94, 78), (169, 91, 6), (102, 115, 122), (196, 109, 0), (34, 102, 105)],  # Grass
#         1: [(39, 101, 88)],  # 1 with multiple color options
#         2: [(39, 120, 119)],  # 2
#         3: [(16, 112, 131)],  # 3
#         4: [(4, 124, 192)],  # 4
#         5: [(162, 153, 211)],  # Flag
#     }
#
#     # Find the closest color ID among all target colors with multiple options per key
#     distances = []
#     for key, color_options in target_colors.items():
#         # Find the minimum distance for any color in the list of options for this key
#         closest_distance = min(euclidean_distance(average_color, color) for color in color_options)
#         distances.append((key, closest_distance))
#
#     # Sort distances and select the closest 'num_colors' IDs
#     closest_colors_id = [key for key, _ in sorted(distances, key=lambda item: item[1])[:1]][0]
#     return closest_colors_id


def save_cell_image(cell_image, cell_id):
    """Save cell image if unique (based on SSIM) or skip if similar to existing images."""
    for filename in os.listdir(IMAGE_DIR):
        existing_image_path = os.path.join(IMAGE_DIR, filename)
        existing_image = cv2.imread(existing_image_path, cv2.IMREAD_GRAYSCALE)

        # Resize the new cell image to match existing image size if needed
        if existing_image.shape != cell_image.shape:
            cell_image = cv2.resize(cell_image, (existing_image.shape[1], existing_image.shape[0]))

        # Compute SSIM between the cell image and existing images
        similarity = ssim(existing_image, cell_image)

        if similarity >= SSIM_THRESHOLD:
            print(f"Image similar to {filename}, not saving.")
            return

    # Save the image if no similar image was found
    new_image_path = os.path.join(IMAGE_DIR, f"0_{cell_id}.png")
    cv2.imwrite(new_image_path, cell_image)
    print(f"New unique cell image saved as {new_image_path}")

def identify_cell_image(cell_image):
    """Identify the cell value by comparing with images in the 'images' folder using SSIM."""
    best_match = None
    highest_similarity = 0

    for filename in os.listdir(IMAGE_DIR):
        image_path = os.path.join(IMAGE_DIR, filename)
        reference_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # Resize cell image to match reference image dimensions, if necessary
        if reference_image.shape != cell_image.shape:
            cell_image_resized = cv2.resize(cell_image, (reference_image.shape[1], reference_image.shape[0]))
        else:
            cell_image_resized = cell_image

        # Calculate SSIM
        similarity = ssim(reference_image, cell_image_resized)
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = filename

    # Check if the best match meets the threshold requirement
    if highest_similarity >= SSIM_THRESHOLD:
        # Take the first character of the filename as the cell's numerical value
        cell_value = int(best_match[0])  # Assumes filename starts with a number (e.g., "3_something.png")
        return cell_value
    else:
        # Save the image if no similar image was found
        # new_image_path = os.path.join(IMAGE_DIR, f"0_{randint(999)}.png")
        # cv2.imwrite(new_image_path, cell_image)
        # No match above the threshold
        raise ValueError("No matching cell image found with sufficient accuracy.")

def process_board(image, last_valid_board=None):
    top_left_color = (17, 29, 39)
    bottom_right_color = (17, 29, 39)
    top_left = None
    bottom_right = None

    # Locate the grid boundaries
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            pixel = image[y, x]
            if not top_left and pixel[0] == top_left_color[0] and pixel[1] == top_left_color[1] and pixel[2] == top_left_color[2]:
                top_left = (x, y)
            if pixel[0] == bottom_right_color[0] and pixel[1] == bottom_right_color[1] and pixel[2] == bottom_right_color[2]:
                bottom_right = (x, y)

    if top_left and bottom_right:
        # Adjust grid boundaries
        top_left = (top_left[0] - 5, top_left[1] + 1)
        bottom_right = (bottom_right[0] + 5, bottom_right[1] - 1)

        # Calculate grid dimensions
        grid_width = bottom_right[0] - top_left[0]
        grid_height = bottom_right[1] - top_left[1]
        num_columns = grid_width // (CELL_SIZE + CELL_SPACING)
        num_rows = grid_height // (CELL_SIZE + CELL_SPACING)

        if (num_rows, num_columns) not in BOARD_SIZES:
            raise ValueError("Invalid board size detected." + str((num_rows, num_columns)))

        board = np.empty((num_rows, num_columns), dtype=int)

        for row in range(num_rows):
            for col in range(num_columns):
                # Apply the mask based on last_valid_board
                if last_valid_board is not None and last_valid_board[row, col] not in [0, 7, 8]:
                    # Skip cells that are not 0, 7, or 8 in last_valid_board
                    board[row, col] = last_valid_board[row, col]
                    continue

                # Calculate the top-left corner of each cell
                cell_x = top_left[0] + col * (CELL_SIZE + CELL_SPACING) + OFFSET
                cell_y = top_left[1] + row * (CELL_SIZE + CELL_SPACING) + OFFSET

                # Extract and process the cell image
                cell_image = image[cell_y:cell_y + CELL_SIZE, cell_x:cell_x + CELL_SIZE]
                gray_cell_image = cv2.cvtColor(cell_image, cv2.COLOR_BGR2GRAY)

                # Identify the cell value based on image matching
                try:
                    cell_value = identify_cell_image(gray_cell_image)
                    board[row, col] = cell_value
                except ValueError:
                    # Mark as unidentified if no match is found
                    board[row, col] = -1

        return board, top_left


