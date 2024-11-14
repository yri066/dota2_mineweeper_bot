from time import sleep

import cv2
import pyautogui
import numpy as np
import keyboard  # for handling keyboard input

from detect import process_board, CELL_SIZE, CELL_SPACING

# Flag to control the start/stop of the loop
running = False

def capture_board():
    try:
        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
        return screenshot
    except Exception as e:
        print("Error capturing board:", e)
        return None


def get_neighbors(row, col, rows, cols):
    """Retrieve neighbors of a cell."""
    neighbors = [(row + dr, col + dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if (dr != 0 or dc != 0)]
    return [(r, c) for r, c in neighbors if 0 <= r < rows and 0 <= c < cols]

def find_deductive_safe_moves(board):
    """Use logical deduction to find guaranteed safe moves and flagged moves."""
    rows, cols = board.shape
    safe_moves = []
    flag_moves = []
    bonus_safe_moves = []  # To store 100% safe moves for bonus tiles (7 and 8)

    for row in range(rows):
        for col in range(cols):
            cell_value = board[row, col]

            # Skip completely safe (unclickable) squares (9), as they are not actionable
            if cell_value == 9:
                continue

            # Process cells with 1-4 values indicating the number of adjacent mines
            if 1 <= cell_value <= 5:
                neighbors = get_neighbors(row, col, rows, cols)

                # Find unknown, bonus, and flagged neighbors
                unknown_cells = [(r, c) for r, c in neighbors if board[r, c] == 0 or board[r, c] == 7 or board[r, c] == 8]
                flagged_cells = sum(1 for r, c in neighbors if board[r, c] == 6)

                # Deductive rules for safe and flag moves
                if flagged_cells == cell_value:
                    # All remaining unknown neighbors must be safe
                    for r, c in unknown_cells:
                        if (r, c) not in safe_moves and (r, c) not in bonus_safe_moves:
                            # Check if the cell is a bonus cell (7 or 8) and store it separately if so
                            if board[r, c] == 7 or board[r, c] == 8:
                                bonus_safe_moves.append((r, c))
                            else:
                                safe_moves.append((r, c))
                elif cell_value - flagged_cells == len(unknown_cells):
                    # All remaining unknown neighbors must be mines
                    flag_moves.extend([(r, c) for r, c in unknown_cells if (r, c) not in flag_moves])

    return safe_moves, flag_moves, bonus_safe_moves


def next_move(board):
    # First pass: look for deductive moves
    safe_moves, flag_moves, bonus_safe_moves = find_deductive_safe_moves(board)

    # Recursive propagation for safe moves with re-evaluation of board
    def propagate_safe_moves():
        nonlocal safe_moves, flag_moves, bonus_safe_moves
        changed = True
        while changed:
            changed = False
            new_safe_moves, new_flag_moves, new_bonus_safe_moves = find_deductive_safe_moves(board)
            for move in new_safe_moves:
                if move not in safe_moves:
                    safe_moves.append(move)
                    changed = True
            for move in new_flag_moves:
                if move not in flag_moves:
                    flag_moves.append(move)
                    changed = True
            for move in new_bonus_safe_moves:
                if move not in bonus_safe_moves:
                    bonus_safe_moves.append(move)
                    changed = True

    propagate_safe_moves()

    # If there are flag moves, return all flag moves as a list of actions
    if flag_moves:
        return [('flag', r, c) for r, c in flag_moves]

    # If there are bonus safe moves (7 or 8), return all of them as click actions
    if bonus_safe_moves:
        return [('click', r, c) for r, c in bonus_safe_moves]

    # If there are no flags or bonus moves, but other safe moves are available, return all safe moves as click actions
    if safe_moves:
        # Filter out any completely safe (9) cells, keeping only unknown (0) cells or cells with values 7 and 8
        safe_clicks = [(r, c) for r, c in safe_moves if board[r, c] == 0 or board[r, c] == 7 or board[r, c] == 8]
        if safe_clicks:
            return [('click', r, c) for r, c in safe_clicks]

    # If no definitive moves are found, choose a backup cell to "guess"
    guess_cells = [(row, col) for row in range(board.shape[0]) for col in range(board.shape[1])
                   if board[row, col] in [0, 7, 8]]

    if guess_cells:
        r, c = guess_cells[0]  # Select the first available cell as a guess
        return [('guess', r, c)]

    # No moves found, game likely finished or no deductive moves remain
    return None



def click_cell(action, row, col, top_left_corner):
    if action == None:
        return

    # Calculate the exact center position of the cell with spacing accounted for
    x = top_left_corner[0] + col * (CELL_SIZE + CELL_SPACING) + CELL_SIZE // 2
    y = top_left_corner[1] + row * (CELL_SIZE + CELL_SPACING) + CELL_SIZE // 2

    pyautogui.moveTo(x, y)
    sleep(0.1)
    # Perform the click
    if action == "click":
        pyautogui.click(x, y)
    elif action == "flag":
        pyautogui.click(x, y, button="right")  # return to default position


def main_loop():
    global running
    last_valid_board = None  # Keep track of the last valid board state
    try_count = 0
    while running:
        if keyboard.is_pressed('q'):
            print("Q pressed, stopping the automation...")
            running = False
            break
        pyautogui.moveTo(10, 10)
        img = capture_board()

        try:
            # Process the new screenshot to get the current board state
            # Pass the last valid board as an optional parameter
            board, top_left_corner = process_board(img, last_valid_board)

            # If processing is successful, update the last valid board
            last_valid_board = board
        except Exception as e:
            print("Error processing board, trying again...:", e)
            continue

        # Find the next move based on the current board state
        moves = next_move(board)
        if moves and moves[0][0] != 'guess':
            for move, row, col in moves:
                click_cell(move, row, col, top_left_corner)
        else:

            if try_count > 3:
                if moves is not None and moves[0][0] == 'guess':
                    pyautogui.press('1')
                    click_cell("click", moves[0][1], moves[0][2], top_left_corner)
                    try_count = 0
                else:
                    print("No moves found, stopping the automation...")
                    running = False
            else:
                try_count += 1
                last_valid_board = None
                continue

def start_game():
    global running
    if not running:
        running = True
        print("Starting Minesweeper automation...")
        main_loop()

# Start and stop the automation on specific key presses
keyboard.add_hotkey('s', lambda: start_game())

print("Press 's' to start the bot, hold 'q' to pause it. Press 'ctrl+c' to stop.")
# Keep the script running to listen for keyboard events
keyboard.wait('ctrl+c')
