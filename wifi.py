import re
import subprocess
from tkinter import *

command_output = subprocess.run(
    ["netsh", "wlan", "show", "profiles"], capture_output=True
).stdout.decode()
profile_names = re.findall("All User Profile     : (.*)\r", command_output)

wifi_list = []

if len(profile_names) != 0:
    for name in profile_names:
        wifi_profile = {}

        profile_info = subprocess.run(
            ["netsh", "wlan", "show", "profile", name], capture_output=True
        ).stdout.decode()

        if re.search("Security key           : Absent", profile_info):
            continue
        else:
            wifi_profile["ssid"] = name

            profile_info_pass = subprocess.run(
                ["netsh", "wlan", "show", "profile", name, "key=clear"],
                capture_output=True,
            ).stdout.decode()
            password = re.search("Key Content            : (.*)\r", profile_info_pass)

            if password == None:
                wifi_profile["password"] = None
            else:
                wifi_profile["password"] = password[1]

            wifi_list.append(wifi_profile)


root = Tk()
root.title("WIFI")
root.resizable(False, False)

Label(root, text="Nazwa wifi:", font=100).grid(row=0, column=0, padx=10, pady=10)
Label(root, text="Hasło:", font=100).grid(row=0, column=1, padx=10, pady=10)

for i, wifi in enumerate(wifi_list):
    # print(f'Id: {wifi_list[i]["ssid"]}\t\tHasło: {wifi_list[i]["password"]}')
    myLabelId = Label(root, text=wifi["ssid"], font=100)
    myLabelId.grid(row=i + 1, column=0, padx=10, pady=10, sticky=W)

    myLabelPassword = Label(root, text=wifi["password"], font=100)
    myLabelPassword.grid(row=i + 1, column=1, padx=10, pady=10, sticky=W)


root.mainloop()
