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
- It can be used to solve all levels, but it's not perfect and can not make complex moves.
- It will prioritize to activate clocks and mana vials if possible
- It's not a cheat, it's just a tool to help you solve the minigame
- It's not an integraged bot, it's a script that simulates mouse clicks

## Notes
- It helps to go through easiest minesweeper patterns only: when around number all fields are 100% mines or 100% are empty fields.
- It is intended to be used with human interaction. When its stuck over 2-3 seconds - Hold Q to stop it, then press win+prntScr to take screenshot and esc to pause the game. Find following "non-obvious" moves on screenshot yourself, afterwards click S again to continue bot. 
- Improvements to the bot via PRs are welcome!
