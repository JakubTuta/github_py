# Program deletes all files/directories in the Downloads folder
# and clear the trash bin

import os
from pathlib import Path
from sys import platform

try:
    import winshell
except ModuleNotFoundError:
    os.system("pip install winshell")
    os.system("pip install pypiwin32")

# works only on Windows
if platform != "win32":
    print("You are not on Windows")
    exit()

# find the Downloads filepath
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


# delete all files/directories
for file in os.listdir(filepath_downloads):
    file_path = os.path.join(filepath_downloads, file)
    if os.path.isdir(file_path):
        os.system(f"rmdir /s /q {file_path}")
    else:
        os.remove(file_path)

# empty the trash bin
try:
    winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
except:
    print("The bin is empty")


print("Finished")
