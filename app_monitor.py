import psutil

# List of productive apps (add more as needed)
productive_apps = ["Notepad.exe"]

def is_productive():
    """Check if any productive app is currently active."""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] in productive_apps:
            return True
    return False

if __name__ == "__main__":
    # Test if a productive app is running
    if is_productive():
        print("You're being productive!")
    else:
        print("Time to get back to work!")
