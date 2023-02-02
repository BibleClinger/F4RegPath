@echo off
pyinstaller --windowed --uac-admin --icon=icons8-fighter-jet-100.png --add-data ".\*png;." --onefile F4RegPath.py
