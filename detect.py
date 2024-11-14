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

def compare_image(cell_image, reference_image_path):
    """Compare a cell image with a reference image and return the similarity score."""
    reference_image = cv2.imread(reference_image_path, cv2.IMREAD_GRAYSCALE)

    # Resize cell image to match reference image dimensions, if necessary
    if reference_image.shape != cell_image.shape:
        cell_image_resized = cv2.resize(cell_image, (reference_image.shape[1], reference_image.shape[0]))
    else:
        cell_image_resized = cell_image

    # Calculate SSIM
    similarity = ssim(reference_image, cell_image_resized)
    return similarity

def identify_cell_image(cell_image):
    """Identify the cell value by comparing with images in the 'images' folder using SSIM."""
    highest_similarity = 0
    best_match = None

    # Iterate through each image in IMAGE_DIR and compare with cell image
    image_paths = [os.path.join(IMAGE_DIR, filename) for filename in os.listdir(IMAGE_DIR)]
    for image_path in image_paths:
        similarity = compare_image(cell_image, image_path)
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = os.path.basename(image_path)

    # Check if the best match meets the threshold requirement
    if highest_similarity >= SSIM_THRESHOLD:
        # Assume filename starts with a number representing cell's numerical value
        cell_value = int(best_match[0])
        return cell_value
    else:
        raise ValueError("No matching cell image found with sufficient accuracy.")

def process_single_cell(image, row, col, top_left, last_valid_board):
    """Process a single cell in the board grid."""
    cell_x = top_left[0] + col * (CELL_SIZE + CELL_SPACING) + OFFSET
    cell_y = top_left[1] + row * (CELL_SIZE + CELL_SPACING) + OFFSET

    # Extract and process the cell image
    cell_image = image[cell_y:cell_y + CELL_SIZE, cell_x:cell_x + CELL_SIZE]
    gray_cell_image = cv2.cvtColor(cell_image, cv2.COLOR_BGR2GRAY)

    cell_value = identify_cell_image(gray_cell_image)
    return cell_value

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
            raise ValueError("Invalid board size detected: " + str((num_rows, num_columns)))

        board = np.empty((num_rows, num_columns), dtype=int)

        # Process each cell sequentially
        for row in range(num_rows):
            for col in range(num_columns):
                if last_valid_board is not None and last_valid_board[row, col] not in [0, 7, 8]:
                    # Skip cells that are not 0, 7, or 8 in last_valid_board
                    board[row, col] = last_valid_board[row, col]
                else:
                    # Process cell
                    board[row, col] = process_single_cell(image, row, col, top_left, last_valid_board)

        return board, top_left
