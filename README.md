# dota2_mineweeper_bot
Automatic solver for Dota 2 Act IV Minesweeper minigame

You can run it from source code with Python, or execute the compiled binary.

## Requirements
- Python 3.11+ (https://www.python.org/downloads/)
- Pip (https://pip.pypa.io/en/stable/installation/)

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
- It can solve all levels, but it's not perfect and can make mistakes
- It is probability dependent, so it can get stuck if there is no clear move, then it will use ability
- It will prioritize to activate clocks and mana vials if possible
- It's not a cheat, it's just a tool to help you solve the minigame
- It's not a bot, it's a script that simulates mouse clicks
