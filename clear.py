from sys import platform
from pathlib import Path
import os
try:
    import winshell
except ModuleNotFoundError:
    os.system("pip install winshell")
    os.system("pip install pypiwin32")


if platform != "win32":
    print("You are not on Windows")
    exit()

try:
    home = str(Path.home())
    filepath_downloads = f"{home}\Downloads"
    os.chdir(filepath_downloads)
except FileNotFoundError:
    print("Wrong directory")
    exit()
except:
    print("Other error")
    exit()

for file in os.listdir(filepath_downloads):
    os.remove(file)

try:
    winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
except:
    print("The bin is empty")
