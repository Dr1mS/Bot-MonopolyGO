# Game Manipulator Bot

This project contains a bot that automates certain actions in MonopolyGO game using image recognition on pc emulator. The bot is designed to work with the BlueStacks emulator. (should work with any other emulator)

## Project Structure

- `bot.py`: This is the main script that contains the logic for the bot.
- `cache/`: This directory contains the images that the bot uses for image recognition.

## Features

- Automatically roll the dice (set to auto-roll).
- Automatically do shutdown minigame.
- Automatically do bank heist.

## Usage

1. Clone the repository.
2. Install the dependencies using `pip install -r requirements.txt`.
3. Open the BlueStacks emulator and start the MonopolyGO game.
4. Close all the popups
5. Run the bot using `python bot.py` or `py bot.py` or `python3 bot.py`.
6. Select the game window when prompted.
7. The bot will start playing the game automatically
8. Press `f` to stop the bot at any time

## How it works

The bot uses image recognition to detect various game events. It takes screenshots of the game window and compares them with the images in the `cache/` directory to determine the current state of the game. The bot then performs actions based on the detected state.

## What you should know

- All the image was taken from a french version of the game.
- The image was taken from a 2560x1440 screen, so you may need to take new screenshots if you are using a different resolution.
- If the bot is not working as expected, you may need to take new screenshots of the game and replace the images in the `cache/` directory.
- The code is not optimized and may not work as expected on different systems. You may need to tweak the code to make it work on your system.

## Dependencies

This project uses the following libraries:

- `pygetwindow`
- `pyautogui`
- `cv2`
- `numpy`
- `pytesseract`
- `re`
- `random`
- `time`
- `os`
- `keyboard`

## Contributing

Contributions are welcome. Please open an issue to discuss your idea before making a pull request.
