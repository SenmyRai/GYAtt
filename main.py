import time
from threading import Thread
from app_monitor import is_productive
from overlay import show_overlay_in_main_thread, clear_overlay
from voice_recognition import listen_for_keyword
from threading import Event

# Create an event to signal stopping the overlay
stop_overlay_event = Event()

def monitor_apps():
    """Monitor if the user is productive and show overlay if not."""
    while True:
        if stop_overlay_event.is_set():  # If the event is set, stop the loop
            print("Overlay cleared, stopping app monitoring.")
            break

        if not is_productive():
            print("Not on a productive app. Showing overlay...")
            if not stop_overlay_event.is_set():  # Only show overlay if not stopped
                show_overlay_in_main_thread()  # Start showing the overlay in the main thread
        
        time.sleep(1) 

def listen_for_clear():
    """Listen for the trigger phrase to clear the overlay and reset screen."""
    while True:
        if listen_for_keyword(stop_overlay_event):  # Pass stop_overlay_event here
            print("Keyword detected! Stopping overlay...")
            stop_overlay_event.set()  
            clear_overlay()  # Clear all images on the screen
            
            # Wait for 5 seconds before resuming productivity check
            print("Waiting for 5 seconds...")
            time.sleep(5)
            print("Resuming app monitoring...")

            # Resuming app monitoring after the 5-second wait
            stop_overlay_event.clear()  
            
         
            overlay_thread = Thread(target=show_overlay_in_main_thread)
            voice_thread = Thread(target=listen_for_clear)

            overlay_thread.start()
            voice_thread.start()

            overlay_thread.join()
            voice_thread.join()

if __name__ == "__main__":
  
    monitor_thread = Thread(target=monitor_apps)
    voice_thread = Thread(target=listen_for_clear)

    monitor_thread.start()
    voice_thread.start()

    monitor_thread.join()
    voice_thread.join()
