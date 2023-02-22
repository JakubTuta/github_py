import sys
import json
import clipboard

SAVED_DATA = "clipboard.json"


def save_data(filepath, data):
    with open(filepath, "w") as file:
        json.dump(data, file)


def load_data(filepath):
    try:
        with open(filepath, "r") as file:
            data = json.load(file)
            return data
    except:
        return {}


if len(sys.argv) == 2:
    command = sys.argv[1]
    data = load_data(SAVED_DATA)
    
    if command == "save":
        key = input("Enter a key: ")
        data[key] = clipboard.paste()
        save_data(SAVED_DATA, data)
        print("Data saved")
        
    elif command == "load":
        key = input("Enter a key: ")
        if key in data:
            clipboard.copy(data[key])
            print("Data copied to clipboard")
        else:
            print("key does not exist")
            
    elif command == "list":
        lista = data.keys()
        print(*lista, sep='\n')
    
    elif command == "clear":
        save_data(SAVED_DATA, {})
        print("Data cleared")
        
    else:
        print("Use save, load or list")
        
else:
    print("Pass a command")
