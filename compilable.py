import os
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import requests
from win32com.client import Dispatch
from zipfile import ZipFile
import pyi_splash
pyi_splash.update_text("Portal 2 VR mod installer")
portalfolder = None
# Check default paths for Portal 2
def download_repo(repo):
    request = requests.get(f"https://api.github.com/repos/{repo}/releases/latest")
    request_json = json.loads(request.text)
    assets_json = request_json["assets"]
    assets_actual_json = assets_json[0]
    download_url = assets_actual_json["browser_download_url"]
    return download_url

if os.path.exists("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Portal 2"):
    print("Found Portal 2 folder automatically!")
    portalfolder = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Portal 2"
    pyi_splash.close()
elif os.path.exists("D:\\steam\\steamapps\\common\\Portal 2"):
    print("Found Portal 2 folder automatically!")
    portalfolder = "D:\\steam\\steamapps\\common\\Portal 2"
    pyi_splash.close()
else:
    # Did not find. Asking user
    pyi_splash.close()
    root = tk.Tk()
    root.withdraw()

    folderPath = filedialog.askdirectory(title="Select the Portal 2 folder")

    if folderPath:
        portalfolder = folderPath

if os.path.exists(os.path.join(portalfolder, "portal2.exe")):
    print(f'Portal 2 folder path: {portalfolder}')
    os.chdir(portalfolder)
    
    # Getting latest version details
    download_url = download_repo("Gistix/portal2vr")
    result = messagebox.askokcancel("Confirmation", "Do you want to download and install Portal 2 VR mod?")
    if result:
        tk.messagebox.showinfo(title="Installing...", message="This may take a while")
        print("Downloading...")
        response = requests.get(download_url)
        open("Portal2VR.zip", "wb").write(response.content)
        print("Installing...")
        if os.path.exists("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Portal 2\\portal2_dlc3"):
            print("It seems like you have a portal2_dlc3 folder already exists.")
            print("This installation will override pak01_dir.vpk, UpdateSoundCache.cmd and _master.cache")
            stauts = messagebox.askokcancel(title="Override warning!!!!!!", message="It seems like you have a portal2_dlc3 folder already exists.\nThis installation will override pak01_dir.vpk, UpdateSoundCache.cmd and _master.cache")
            if stauts:
                pass
            else:
                exit()
        with ZipFile('Portal2VR.zip', 'r') as f:
            f.extractall()
        result = messagebox.askyesno("Installation was successful", "Do you want to download and install Mod manager?")
        if result:
            manager_url = download_repo("Juliasmatius/Portal-2-VR-manager")
            print("Downloading...")
            response = requests.get(manager_url)
            open("ModManager.bat", "wb").write(response.content)
            result = messagebox.askyesno("Installation was successful", "Do you want to make a shortcut?")
            if result:
                
                desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 
                path = os.path.join(desktop, "Portal 2 VR mod.lnk")
                target = portalfolder+"ModManager.bat"
                wDir = portalfolder
                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(path)
                shortcut.Targetpath = target
                shortcut.WorkingDirectory = wDir
                shortcut.save()
                
    else:
        print("Cancelled Installation","Portal2VR.zip")
        exit()
else:
    print("The folder you chose was invalid.")
    exit()
