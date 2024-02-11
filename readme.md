# Game Manipulator Bot

This project contains a bot that automates certain actions in MonopolyGO game using image recognition on pc emulator. The bot is designed to work with the BlueStacks emulator. (should work with any other emulator)

## Project Structure

- `bot.py`: This is the main script that contains the logic for the bot.
- `cache/`: This directory contains the images that the bot uses for image recognition.

## Features

- Detects and handles various game events. (e.g. dice roll, braquage, siege, etc.)
- Play until you stop it by pressing F.
- Works with the BlueStacks emulator.

## No ready yet

- AutoBuy
- Auto recup mission

## Usage

1. Run the `bot.py` script.
2. When prompted, enter the number of the window you want to use.
3. The bot will start automating tasks in the game.

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
