import zipfile
import os
import tkinter as tk
from tkinter import messagebox

folders = ['mods', 'shaderpacks']
path_str = "{drive}\\Users\\{user}\\AppData\\Roaming\\.minecraft"
jdk17_link = 'https://download.oracle.com/java/17/latest/jdk-17_windows-x64_bin.exe'
fabric_link = 'https://maven.fabricmc.net/net/fabricmc/fabric-installer/1.0.1/fabric-installer-1.0.1.jar'

def get_user():
    print(f"Username: {os.getenv('USERNAME')}")
    
    return os.getenv('USERNAME')

def get_drive():
    print(f"SystemDrive: {os.getenv('SystemDrive')}")

    return os.getenv('SystemDrive')

def backup_mods():
    print("Backing up mods...")

    mods_path = os.path.join(path_str.format(drive=get_drive(), user=get_user()), 'mods')

    if not os.path.exists(mods_path):
        print("The mods directory does not exist")
        return

    backup_path = os.path.join(path_str.format(drive=get_drive(), user=get_user()), 'mods_backup')
    if not os.path.exists(backup_path):
        print("The mods_backup directory does not exist, creating...")
        os.makedirs(backup_path)

    os.system(f'xcopy /E /Y "{mods_path}" "{backup_path}"')
    print("Backed up all mods")

    print("Deleting old mods...")
    os.system(f'rd /S /Q "{mods_path}"')

def unzip_file(zip_path, extract_to):
    print(f"Extracting {zip_path} to {extract_to}...")

    if not os.path.exists(zip_path):
        print(f"The file {zip_path} does not exist.")
        return

    if not os.path.exists(extract_to):
        print(f"The directory {extract_to} does not exist, creating...")
        os.makedirs(extract_to)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        print(f"Extracted all files to {extract_to}")

def copy_to_path(src, dst):
    print(f"Copying {src} to {dst}...")

    if not os.path.exists(src):
        print(f"The file {src} does not exist.")
        return

    if not os.path.exists(dst):
        print(f"The directory {dst} does not exist, creating...")
        os.makedirs(dst)

    os.system(f'xcopy /E /Y "{src}" "{dst}"')
    print(f"Copied all files to {dst}")

def download_jdk17(jdk_path):
    print("Downloading JDK 17...")

    if os.path.exists(jdk_path):
        print("JDK 17 already exists")
        return
    
    os.system(f'curl -o {jdk_path} {jdk17_link}')
    print("Downloaded JDK 17")

def install_jdk17(jdk_path):
    print("Installing JDK 17...")

    os.system(jdk_path)
    print("Installed JDK 17")

def show_popup(message):
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    messagebox.showinfo("Minecraft Mods", message)
    root.destroy()

def download_fabric(fabric_path):
    print("Downloading Fabric...")

    if os.path.exists(fabric_path):
        print("Fabric already exists")
        return
    
    os.system(f'curl -o {fabric_path} {fabric_link}')
    print("Downloaded Fabric")

def install_fabric(fabric_path):
    os.system(f'java -jar {fabric_path}')
    print("Installed Fabric")


if __name__ == "__main__":
    show_popup("Make sure Minecraft Java is Installed")
    cur_dir = os.path.dirname(os.path.realpath(__file__))

    jdk_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'jdk-17_windows-x64_bin.exe')
    download_jdk17(jdk_path)
    install_jdk17(jdk_path)

    fabric_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fabric-installer-1.0.1.jar')
    download_fabric(fabric_path)
    show_popup("Install Fabric for Minecraft version 1.20.6")
    install_fabric(fabric_path)

    backup_mods()

    for zip_path in [os.path.join(cur_dir, f'{zip_path}.zip') for zip_path in folders]:
        unzip_file(zip_path, cur_dir)

    for folder in folders:
        copy_to_path(os.path.join(cur_dir, folder), os.path.join(path_str.format(drive=get_drive(), user=get_user()), folder))