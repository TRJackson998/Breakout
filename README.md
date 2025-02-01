# Breakout

CMSC 495 Capstone Project implementing the game Breakout in Python

## Poetry Package Management

https://python-poetry.org/docs/

Follow along with the docs for installation. Run `poetry config virtualenvs.in-project true` to make sure the virtual environment wil be set up in the project folder, then run the command `poetry install` in the outer Breakout folder to initialize the virtual environment.

To add packages, run the command `poetry add {package_name}`

## PyInstaller

https://pyinstaller.org/en/stable/

We are using PyInstaller to package our program as an executable file for the end user. Run build_exe.cmd in the outer Breakout folder to create a new executable named breakout.exe in the same folder. This is a standalone executable app version of our main program.
