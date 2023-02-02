# F4RegPath.py -- by BibleClinger
#
# This tool enumerates the Benchmark Sims registry for Falcon BMS entries.
# It allows users to change the location of an existing BMS registry entry.
# It allows users to delete an existing BMS registry entry.
import sys
import os.path
import winreg
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import webbrowser

version = "0.0.2 alpha"

HelpMsg = """Select the version. Press Change to change the installation path in the registry, or DELETE to delete the registry entry.

Config Found = This checks if your installation either has a file called \'Falcon BMS.cfg\' where expected.
If it is missing, then you may have already deleted your installation.

Note: This tool does NOT move BMS directories as of yet. Move it yourself, and then use the Change option.

Use this tool at your own risk. Editing the registry can be dangerous to your computer and your data."""

aboutMessage = f'Programmed by BibleClinger\n\nVersion: {version}\n\nFighter Jet icon from https://icons8.com/icon/7T9paWRNQ1CI/fighter-jet\n\nWould you like to visit?'

changeButton = None
deleteButton = None
tree = None
root = None

data = []

baseSubKey = r"SOFTWARE\WOW6432Node\Benchmark Sims\\"
configSubPath = r"\user\config\Falcon BMS.cfg"
iconFile = 'icons8-fighter-jet-100.png'
icon_url = 'https://icons8.com/icon/7T9paWRNQ1CI/fighter-jet'

def HasConfig(path):
    return os.path.exists(path + configSubPath)

def SetPathFromReg(version, newDir):
    try:
        regHandle = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        keyHandle = winreg.OpenKey(regHandle, baseSubKey + version, access=winreg.KEY_WRITE)
        winreg.SetValueEx(keyHandle, "basedir", 0, winreg.REG_SZ, newDir)
    except OSError:
        tk.messagebox.showerror(title="Registry Error", message="Error when WRITING to registry. This could be a permissions issue.")
    finally:
        winreg.CloseKey(keyHandle)
        winreg.CloseKey(regHandle)

def deleteVersionFromReg(version):
    try:
        regHandle = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        keyHandle = winreg.OpenKey(regHandle, baseSubKey, access=winreg.KEY_WRITE)
        winreg.DeleteKey(keyHandle, version)
    except OSError:
        tk.messagebox.showerror(title="Registry Error", message="Error when DELETING from registry. This is likely a permissions issue.")
    finally:
        winreg.CloseKey(keyHandle)
        winreg.CloseKey(regHandle)

def GetPathsFromReg():
    arr = []
    regHandle = None
    keyHandle = None
    try:
        regHandle = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        keyHandle = winreg.OpenKey(regHandle, baseSubKey)
        queryInfo = winreg.QueryInfoKey(keyHandle)
        i = 0
        while i<queryInfo[0]: # queryInfo[0] gives us how many subkeys there are -- ie. how many BMS installations there are
            keyString = winreg.EnumKey(keyHandle, i)
            try:
                subKeyHandle = winreg.OpenKey(regHandle, baseSubKey + keyString)
                valuePack = winreg.QueryValueEx(subKeyHandle, "baseDir")
                arr.append((keyString, valuePack[0], HasConfig(valuePack[0])))
            except OSError:
                arr.append((keyString, "<Unable to read>", "<Unknown>"))
            finally:
                winreg.CloseKey(subKeyHandle)
            i = i + 1
    except OSError:
        tk.messagebox.showerror(title="Registry Error", message="Error while querying registry. Perhaps this is a permission issue. Perhaps BMS was never installed.")
    finally:
        if(keyHandle):
            winreg.CloseKey(keyHandle)
        if(regHandle):
            winreg.CloseKey(regHandle)
        return arr

def RefreshTree():
    global data, changeButton, deleteButton, tree
    data = GetPathsFromReg()
    tree.delete(*tree.get_children())
    if len(data) > 0:
        for d in data:
            tree.insert('', 0, values=d) # Putting them in reverse, because newest entry should be top if all works out
    else:
        tree.insert('', 0, values=('<Falcon BMS Missing>', "<None>", "False"))
        changeButton["state"] = "disable"
        deleteButton["state"] = "disable"
    SelectFirstTreeChild()

def SelectFirstTreeChild():
    child_id = tree.get_children()[0] # Select first element
    tree.focus(child_id)
    tree.selection_set(child_id)

def item_selected(event):
    global changeButton
    items = tree.selection()
    if (len(items) > 1) or (len(data) == 0):
        changeButton["state"] = "disable" # We don't want to change multiple entries, but we may want to delete them
    else:
        changeButton["state"] = "normal"

def changeClick():
    newDir = tk.filedialog.askdirectory()
    if(newDir != ""):
        entry = tree.item(tree.focus())
        version = entry["values"][0]
        SetPathFromReg(version, os.path.normpath(newDir))
        RefreshTree()

def deleteClick():
    #entry = tree.item(tree.focus())
    #version = entry["values"][0]
    items = tree.selection()
    # Are you sure?
    if tkinter.messagebox.askyesno(title="Undoable", message=f'You selected {len(items)} {"entry" if len(items) == 1 else "entries"} for deletion. This CANNOT be undone. Are you sure you want to delete?'):
        for i in items:
            version = tree.item(i)["values"][0]
            deleteVersionFromReg(version)
        RefreshTree()

def showAbout():
    if tkinter.messagebox.askyesno(title="About...", message=aboutMessage):
        webbrowser.open_new(icon_url)

def CreateAndExecuteGUI():
    global root, tree, changeButton, deleteButton
    root = tk.Tk()
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    elif __file__:
        application_path = os.path.dirname(__file__)
    root.iconphoto(False, tk.PhotoImage(file=os.path.join(application_path, iconFile)))
    root.title('F4RegPath: ' + 'v' + version)
    root.geometry('725x375')
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    file_menu = tk.Menu(menubar, tearoff=False)
    file_menu.add_command(label='About', command=showAbout)
    file_menu.add_separator()
    file_menu.add_command(label='Exit', command=root.destroy)

    menubar.add_cascade(label="File", menu=file_menu)

    columns = ('version', 'path', 'config')
    tree = ttk.Treeview(root, columns=columns, show='headings')
    tree.heading('version', text='Version')
    tree.heading('path', text='Path')
    tree.heading('config', text='Config Found')

    tree.bind('<<TreeviewSelect>>', item_selected)
    tree.grid(row=0, column=0, sticky='nsew', rowspan=2, columnspan=2)

    scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=2, rowspan=2, sticky='ns')

    ttk.Label(root, text=HelpMsg).grid(row=2, column=0, sticky='ns')

    changeButton = ttk.Button(root, text='Change', command=changeClick)
    changeButton.grid(row=0, column=3, columnspan=3, sticky='ew')
    #moveButton = ttk.Button(root, text='Move')
    #moveButton.grid(row=1, column=3, columnspan=3, sticky='ew')
    deleteButton = ttk.Button(root, text='DELETE', command=deleteClick)
    deleteButton.grid(row=1, column=3, columnspan=3, sticky='ew')
    RefreshTree()
    if(len(data) == 0):
        changeButton["state"] = "disable"
        deleteButton["state"] = "disable"
    root.mainloop()

CreateAndExecuteGUI()
