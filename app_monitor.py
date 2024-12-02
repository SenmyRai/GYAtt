import psutil
productive_apps = ["Notepad.exe"]

def is_productive():
    try:
        with open("productive_apps.txt", "r") as f:
            productive_apps = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        productive_apps = []  # If the file doesn't exist, no apps are marked productive
    
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] in productive_apps:
            return True
    return False

if __name__ == "__main__":
    if is_productive():
        print("You're being productive!")
    else:
        print("Time to get back to work!")
