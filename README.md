# F4RegPath
Allows simple manipulation of the Falcon BMS registry paths

## Is this safe?

Editing the registry inherently comes with some level of risk. If you need to use this program, you probably already did something unsafe or incorrect. Use this tool at your own risk.

## How to use:

Download the latest exe in the releases. Run it. Read the information the program tells you. Use at your own risk. Note: If you're a regedit expert, you probably don't need this program.

## Example uses:

| Scenario | Solution |
| ----------- | ----------- |
| You are trying to install Falcon BMS 4.37, but you're receiving an error that there is an existing registry option for Falcon BMS 4.37. You don't remember installing this version of Falcon BMS before. You have no idea if Falcon BMS is present on your computer. | Run this program, select Falcon BMS 4.37, and click DELETE. Close the program. Install Falcon BMS into an empty directory. |
| You moved Falcon BMS 4.37, and now it doesn't run. | Run this program, select Falcon BMS 4.37, and click Change. Choose the directory where you moved it to. Close this program. Try running Falcon BMS. |
| You want to move Falcon BMS 4.37 to another directory without reinstalling. | Move your Falcon BMS installation manually. Run this program, select Falcon BMS 4.37, and click Change. Choose the directory where you moved it to. Close this program. Try running Falcon BMS. |

## Editing Code (Advanced users only)

Clone the rep. Make your changes. Run it with the required permission. If you want to convert it to an exe, consider pyinstaller with the following arguments:

```
pyinstaller --windowed --uac-admin --icon=icons8-fighter-jet-100.png --add-data ".\*png;." --onefile F4RegPath.py
```

## License

Everything except the icon is released under the MIT license.

[Fighter Jet](https://icons8.com/icon/7T9paWRNQ1CI/fighter-jet) icon by [Icons8](https://icons8.com). As required by the free license, the program must link to the Fighter Jet page. Changes to the program must either use another icon with a different license, or else respect this requirement.
