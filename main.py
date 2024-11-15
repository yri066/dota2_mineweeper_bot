from time import sleep

import cv2
import pyautogui
import numpy as np
import keyboard  # for handling keyboard input

from detect import process_board, CELL_SIZE, CELL_SPACING
from remote_solver import solve_board

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

def click_cell(action, row, col, top_left_corner):
    if action == None:
        return

    # Calculate the exact center position of the cell with spacing accounted for
    x = top_left_corner[0] + col * (CELL_SIZE + CELL_SPACING) + CELL_SIZE // 2
    y = top_left_corner[1] + row * (CELL_SIZE + CELL_SPACING) + CELL_SIZE // 2

    pyautogui.moveTo(x, y)
    # Perform the click
    if action == "click":
        pyautogui.click(x, y)
    if action == "guess":
        pyautogui.press('1')
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
            board, top_left_corner, num_rows, num_columns, n_mines = process_board(img, last_valid_board)

            # If processing is successful, update the last valid board
            last_valid_board = board
        except Exception as e:
            print("Error processing board, trying again...:", e)
            continue

        # Find the next move based on the current board state
        try:
            moves = solve_board(board, num_columns, num_rows, n_mines)
            for move, row, col in moves:
                click_cell(move, row, col, top_left_corner)
                print(f"Performing action: {move} at ({row}, {col})")
        except Exception as e:
            print("Error solving board, taking screenshot and stopping the automation...:", e)
            pyautogui.screenshot("last_board.png")
            sleep(1)
            # click escape to stop the game
            pyautogui.press('esc')
            running = False
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
