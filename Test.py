import speech_recognition as sr
import pyttsx3

# Initialize speech recognition and text-to-speech engine
rec = sr.Recognizer()
engine = pyttsx3.init()

# Get the available voices
voices = engine.getProperty('voices')

# Set the desired voice (example: using voice 1 - adjust index as needed)
try:
    engine.setProperty('voice', voices[1].id)  # Try different indices if needed
except IndexError:
    print("Invalid voice index. Please check the available voices and indices.")
    exit()
except Exception as e:
    print(f"Error setting voice: {e}")
    exit()

# Define custom responses
responses = {
    "hello": "Namaste Bhaisahab",
    "hi": "Namaste Bhaisahab",
    "what are you doing": "Go and Fuck yourself MotherFucker",
    "whatsapp": "Go and Fuck yourself MotherFucker",
    "hey": "Namaste Bhaisahab",
    "good morning": "Shubh Prabhat Bhaisahab",
    "good afternoon": "Shubh Dopahar Bhaisahab",
    "good evening": "Shubh Sandhya Bhaisahab",
    "good night": "Shubh Ratri Bhaisahab",
    "how are you": "Main theek hoon, aap kaise hain?",
    "how's it going": "Sab badhiya hai.",
    "what's up": "Kya haal hai?",
    "how's life": "Zindagi mast chal rahi hai.",
    "thank you": "Dhanyavaad Bhaisahab",
    "thanks": "Dhanyavaad",
    "okay": "Theek hai",
    "ok": "Theek hai",
    "sounds good": "Achha hai",
    "great": "Bahut achha",
    "awesome": "Badiya",
    "cool": "Mast",
    "bye": "Phir milte hain",
    "goodbye": "Alvida",
    "see you later": "Phir milte hain",
    "cya": "Phir milte hain",
    "bro": "Bhai",
    "bhai": "Bhai",
    "yaar": "Yaar",
    "dost": "Dost",
    "what": "Kya?",
    "why": "Kyun?",
    "when": "Kab?",
    "where": "Kahan?",
    "who": "Kaun?",
    "how": "Kaise?",
    "please": "Kripya",
    "sorry": "Maaf karna",
    "excuse me": "Maaf kijiyega",
    "no problem": "Koi baat nahin",
    "you're welcome": "Aapka swagat hai",
    "help": "Madad",
    "i don't know": "Mujhe nahin pata",
    "i understand": "Main samajh gaya",
    "i don't understand": "Main nahin samjha",
    "yes": "Haan",
    "no": "Nahin",
    "lol": "Hahaha",
    "lmao": "Hahaha",
    "rofl": "Hahaha",
    "wtf": "Go and Fuck yourself MotherFucker",
    "fuck you too": "Fuck you three Bitch",
    "stfu": "Go and Fuck yourself MotherFucker"
}

# Infinite loop for continuous speech recognition
while True:
    try:
        with sr.Microphone() as source:
            print("Speak something...")
            audio = rec.listen(source)

        text = rec.recognize_google(audio).lower() # Convert to lowercase for matching
        print("You said:", text)

        # Check for custom responses
        if text in responses:
            response = responses[text]
            print("Response:", response)
            engine.say(response)
            engine.runAndWait()
        else:
            print("Say Again Motherfucker")
            engine.say("Say Again Motherfucker") # Optional: Default speech
            engine.runAndWait()



    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    except KeyboardInterrupt:
        print("Exiting...")
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        break