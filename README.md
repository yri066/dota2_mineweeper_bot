# dota2_mineweeper_bot
Automatic solver for Dota 2 Act IV Minesweeper minigame

You can run it from source code with Python, or execute the compiled binary.

## Requirements if run from .exe
- Dota 2 with FullHD resolution: 1920x1080

## Requirements if run from source code.
- Dota 2 with FullHD resolution: 1920x1080
- Python 3.11+ (https://www.python.org/downloads/)
- Pip (https://pip.pypa.io/en/stable/installation/)

## How to install from .exe
1. Clone the repository
2. Run `run.exe` file in the directory with other files.
   
## How to install from source code 
1. Clone the repository
2. Install the required packages with `pip install -r requirements.txt`
3. Run the script with `python main.py`

## How to use
1. Launch Dota 2 and start the Minesweeper minigame.
2. Launch bot.
3. Press the first field in the game (bot cannot start)
4. Press 's' to start the bot, hold 'q' to stop it (should stop after the level is completed)
5. Click 'ctrl+c' to terminate completely

## Features
- Automatic solver for Dota 2 Act IV Minesweeper minigame
- It can be used to solve all levels, but it's not perfect and can get stuck. Then screenshot is taken and game is paused.
- It will use ability if there is an unavoidable guess situation. 
- It will prioritize to activate clocks and mana vials if possible
- It's not a cheat, it's just a tool to help you solve the minigame
- It's not an integrated bot, it's a script that simulates mouse clicks

## Notes
- The bot will behave unexpectedly when "6" appears on the board. Its better to stop it, resolve all tiles around 6 and continue the bot.
- In case of "board not detected" messages and bot not working, try changing in-game resolution to native screen resolution and different options: fullscreen/borderless window
- The bot will not work with HDR enabled. 
- Improvements to the bot via PRs are welcome!
