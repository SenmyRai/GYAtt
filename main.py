import time
from threading import Thread
from app_monitor import is_productive
from overlay import show_overlay
from voice_recognition import listen_for_keyword

def monitor_apps():
    """Monitor if the user is productive and show overlay if not."""
    while True:
        if not is_productive():
            print("Not on a productive app. Showing overlay...")
            show_overlay()
        time.sleep(5)  # Check every 5 seconds

def listen_for_clear():
    """Listen for the trigger phrase to clear the overlay."""
    while True:
        if listen_for_keyword():
            print("Clearing overlay...")
            # You may need to add logic to close the overlay window here
            break

if __name__ == "__main__":
    # Run app monitoring and voice listening in parallel
    monitor_thread = Thread(target=monitor_apps)
    voice_thread = Thread(target=listen_for_clear)

    monitor_thread.start()
    voice_thread.start()

    monitor_thread.join()
    voice_thread.join()
