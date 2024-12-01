import speech_recognition as sr

# Hardcoded keyword to clear the overlay
trigger_phrase = "clear screen"

def listen_for_keyword():
    """Listen for the trigger phrase using the microphone."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for the trigger phrase...")
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return trigger_phrase.lower() in text.lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return False
        except sr.RequestError:
            print("Speech recognition service unavailable.")
            return False

if __name__ == "__main__":
    # Test voice recognition
    if listen_for_keyword():
        print("Keyword detected!")
    else:
        print("Keyword not detected.")
