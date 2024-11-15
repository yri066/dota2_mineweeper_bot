# dota2_mineweeper_bot
Automatic solver for Dota 2 Act IV Minesweeper minigame

You can run it from source code with Python, or execute the compiled binary.

## Requirements
- Python 3.11+ (https://www.python.org/downloads/)
- Pip (https://pip.pypa.io/en/stable/installation/)
- Dota 2 with FullHD resolution: 1920x1080

## How to install
1. Clone the repository
2. Install the required packages with `pip install -r requirements.txt`
3. Run the script with `python main.py`
4. Launch Dota 2 and start the Minesweeper minigame
5. Press the first field in the game (bot cannot start)
6. Press 's' to start the bot, hold 'q' to stop it (should stop after the level is completed)
7. Select the new level, press on the first field and click "s" again ...
8. Click 'ctrl+c' to terminate completely

## Features
- Automatic solver for Dota 2 Act IV Minesweeper minigame
- It can be used to solve all levels, but it's not perfect and can get stuck. Then screenshot is taken and game is paused.
- It will use ability if there is an unavoidable guess situation. 
- It will prioritize to activate clocks and mana vials if possible
- It's not a cheat, it's just a tool to help you solve the minigame
- It's not an integrated bot, it's a script that simulates mouse clicks

## Notes
- The bot will behave unexpectedly when "6" appears on the board. Its better to stop it, resolve all tiles around 6 and continue the bot. 
- Improvements to the bot via PRs are welcome!
