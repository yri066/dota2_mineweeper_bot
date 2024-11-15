import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

# Constants
SSIM_THRESHOLD = 0.6  # SSIM threshold to consider two images as identical
IMAGE_DIR = "images"
BOARD_SIZES = [(9, 9), (11, 12), (13, 15), (14, 18), (16, 20)]
BOARD_MINES = [10, 19, 32, 47, 66]

# Reference resolution for Full HD (1920x1080)
REFERENCE_WIDTH = 1920
REFERENCE_HEIGHT = 1080
REFERENCE_CELL_SIZE = 34  # Default cell size in Full HD
REFERENCE_CELL_SPACING = 2  # Default cell spacing in Full HD

def calculate_scaling_factors(image_width, image_height):
    """Calculate scaling factors for cell size and spacing based on resolution."""
    width_scale = image_width / REFERENCE_WIDTH
    height_scale = image_height / REFERENCE_HEIGHT
    return width_scale, height_scale

def calculate_relative_dimensions(image_width, image_height):
    """Calculate cell size and spacing relative to Full HD."""
    width_scale, height_scale = calculate_scaling_factors(image_width, image_height)
    cell_size = int(REFERENCE_CELL_SIZE * min(width_scale, height_scale))
    cell_spacing = int(REFERENCE_CELL_SPACING * min(width_scale, height_scale))
    return cell_size, cell_spacing

def calculate_board_offsets(image_width, image_height):
    """Calculate resolution-dependent offsets based on Full HD reference."""
    x_offset = int(5 * (image_width / REFERENCE_WIDTH))
    y_offset = int(1 * (image_height / REFERENCE_HEIGHT))
    return x_offset, y_offset

def calculate_cell_offsets(image_width, image_height):
    """Calculate resolution-dependent offsets based on Full HD reference."""
    x_offset = int(3 * (image_width / REFERENCE_WIDTH))
    y_offset = int(3 * (image_height / REFERENCE_HEIGHT))
    return x_offset, y_offset

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
        # save debug image
        cv2.imwrite(f"debug/debug_cell_image_{np.random.randint(1000)}.png", cell_image)
        raise ValueError("No matching cell image found with sufficient accuracy.")

def process_single_cell(image, row, col, top_left, cell_size, cell_spacing, offset, last_valid_board):
    """Process a single cell in the board grid."""
    cell_x = top_left[0] + col * (cell_size + cell_spacing) + offset[0]
    cell_y = top_left[1] + row * (cell_size + cell_spacing) + offset[1]

    # Extract and process the cell image
    cell_image = image[cell_y:cell_y + cell_size, cell_x:cell_x + cell_size]
    gray_cell_image = cv2.cvtColor(cell_image, cv2.COLOR_BGR2GRAY)

    cell_value = identify_cell_image(gray_cell_image)
    return cell_value

def process_board(image, last_valid_board=None):
    top_left_color = (17, 29, 39)
    bottom_right_color = (17, 29, 39)
    top_left = None
    bottom_right = None

    # Create a copy of the image for debugging
    debug_image = image.copy()

    # Calculate resolution-dependent dimensions and offsets
    cell_size, cell_spacing = calculate_relative_dimensions(image.shape[1], image.shape[0])
    board_x_offset, board_y_offset = calculate_board_offsets(image.shape[1], image.shape[0])
    cell_x_offset, cell_y_offset = calculate_cell_offsets(image.shape[1], image.shape[0])

    # Locate the grid boundaries
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            pixel = image[y, x]
            if not top_left and pixel[0] == top_left_color[0] and pixel[1] == top_left_color[1] and pixel[2] == top_left_color[2]:
                top_left = (x, y)
            if pixel[0] == bottom_right_color[0] and pixel[1] == bottom_right_color[1] and pixel[2] == bottom_right_color[2]:
                bottom_right = (x, y)

    if top_left and bottom_right:
        # Adjust grid boundaries using resolution-dependent offsets
        top_left = (top_left[0] - board_x_offset, top_left[1] + board_y_offset)
        bottom_right = (bottom_right[0] + board_x_offset, bottom_right[1] - board_y_offset)

        # Draw the detected board boundary on the debug image
        cv2.rectangle(debug_image, top_left, bottom_right, (0, 255, 0), 2)

        # Calculate grid dimensions
        grid_width = bottom_right[0] - top_left[0]
        grid_height = bottom_right[1] - top_left[1]

        # Calculate the number of rows and columns based on predefined board sizes
        cols, rows = grid_width // (cell_size + cell_spacing), grid_height // (cell_size + cell_spacing)

        # Draw each cell outline for debugging
        for row in range(rows):
            for col in range(cols):
                # Calculate cell position
                cell_x = top_left[0] + col * (cell_size + cell_spacing) + cell_x_offset
                cell_y = top_left[1] + row * (cell_size + cell_spacing) + cell_y_offset

                # Draw a rectangle around each cell
                cv2.rectangle(debug_image, (cell_x, cell_y),
                              (cell_x + cell_size, cell_y + cell_size),
                              (255, 0, 0), 1)

        # Save the debug image with detected board and cell outlines
        cv2.imwrite("debug_board_detection.png", debug_image)

        # Estimate number of rows and columns
        if (rows, cols) not in BOARD_SIZES:
            raise ValueError("Invalid board size detected: unable to match to predefined sizes.")

        board = np.empty((rows, cols), dtype=int)

        # Process each cell sequentially (optional)
        for row in range(rows):
            for col in range(cols):
                if last_valid_board is not None and last_valid_board[row, col] not in [0, 7, 8]:
                    # Skip cells that are not 0, 7, or 8 in last_valid_board
                    board[row, col] = last_valid_board[row, col]
                else:
                    # Process cell
                    cell_x = top_left[0] + col * (cell_size + cell_spacing) + cell_x_offset
                    cell_y = top_left[1] + row * (cell_size + cell_spacing) + cell_y_offset
                    cell_image = image[cell_y:cell_y + cell_size, cell_x:cell_x + cell_size]
                    gray_cell_image = cv2.cvtColor(cell_image, cv2.COLOR_BGR2GRAY)
                    board[row, col] = identify_cell_image(gray_cell_image)

        return board, top_left, rows, cols, BOARD_MINES[BOARD_SIZES.index((rows, cols))]
    else:
        raise ValueError("Unable to detect board boundaries.")