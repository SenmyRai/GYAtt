import speech_recognition as sr
from overlay import clear_overlay 

# Hardcoded keyword to clear the overlay
trigger_phrase = "sorry Mommy"

def listen_for_keyword(stop_overlay_event):
    """Listen for the trigger phrase using the microphone."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for the trigger phrase...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
        recognizer.energy_threshold = 1500  
        
        try:
            audio = recognizer.listen(source, timeout=15)  # Increased timeout for better capture
            print(f"Audio captured: {audio}")  
            text = recognizer.recognize_google(audio)
            print(f"Recognized text: {text}")  
            if trigger_phrase.lower() in text.lower():
                clear_overlay()  
                stop_overlay_event.set()  
                return True
            return False
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return False
        except sr.RequestError:
            print("Speech recognition service unavailable.")
            return False
        except sr.WaitTimeoutError:
            print("Listening timed out. Trying again.")
            return False

if __name__ == "__main__":
    # Test voice recognition
    if listen_for_keyword():
        print("Keyword detected!")
    else:
        print("Keyword not detected.")
