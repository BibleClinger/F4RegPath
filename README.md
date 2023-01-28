# F4RegPath
Allows simple manipulation of the Falcon BMS registry paths

## How to use:

Download the latest exe in the releases. Run it. Read the information the program tells you. Use at your own risk. Note: If you're a regedit expert, you probably don't need this program.

## Example uses:

Scenario #1: You are trying to install Falcon BMS 4.37, but you're receiving an error that there is an existing registry option for Falcon BMS 4.37. You don't remember installing this version of Falcon BMS before. You have no idea if Falcon BMS is present on your computer.
Solution #1: Run this program, select Falcon BMS 4.37, and click DELETE. Close the program. Install Falcon BMS into an empty directory.

Scenario #2: You moved Falcon BMS 4.37, and now it doesn't run.
Solution #2: Run this program, select Falcon BMS 4.37, and click Change. Choose the directory where you moved it to. Close this program. Try running Falcon BMS.

Scenario #3: You want to move Falcon BMS 4.37 to another directory.
Solution #3: Move it manually. Run this program, select Falcon BMS 4.37, and click Change. Choose the directory where you moved it to. Close this program. Try running Falcon BMS.

## Editing Code (Advanced users only)

Clone the rep. Make your changes. Run it with the required permission. If you want to convert it to an exe, consider pyinstaller with the following arguments:

```
pyinstaller --windowed --uac-admin --icon=icons8-fighter-jet-100.png --add-data ".\*png;." --onefile F4RegPath.py
```
