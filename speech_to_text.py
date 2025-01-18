import speech_recognition as sr

rec = sr.Recognizer()
# Set a fixed energy threshold (adjust based on your environment)
rec.energy_threshold = 300  
rec.dynamic_energy_threshold = False  # Disable dynamic adjustment



def recognize_speech():
    # Use the microphone as source for input (specify the microphone index)
    with sr.Microphone() as source:  
        # Adjusting for ambient noise
        rec.adjust_for_ambient_noise(source, duration=0.5)      
        print("Listening...")
        audio = rec.listen(source, timeout=10, phrase_time_limit=10)
 
        try:
            # Recognize speech using Google Web Speech API
            text = rec.recognize_google(audio, language="vi-VN")
            print(f"You said: {text}")
            return text
            
        except sr.UnknownValueError:
            print("Google Web Speech API could not understand the audio")
            return None
            
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")
            return None

if __name__ == "__main__":
    while True:
        print("Press Enter to start speaking...")
        input()  # Wait for user input
        result = recognize_speech()
        if result:
            print(f"Result: {result}")
        else:
            print("No valid speech detected.")