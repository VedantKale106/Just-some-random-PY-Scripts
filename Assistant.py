import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import wolframalpha

# Initialize speech recognition and text-to-speech
r = sr.Recognizer()
engine = pyttsx3.init()


# Wolfram Alpha setup (get your ACTUAL API key from Wolfram Alpha website)
app_id = "YOUR_WOLFRAM_ALPHA_API_KEY"  # REPLACE THIS!
client = wolframalpha.Client(app_id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning.")
    elif 12 <= hour < 18:
        speak("Good afternoon.")
    else:
        speak("Good evening.")
    speak("I'm Bekkar AI. How can I help you?")

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio).lower()
        print("You said:", query)
        return query
    except sr.UnknownValueError:
        speak("I couldn't understand you.")
        return ""
    except sr.RequestError as e:
        speak(f"My speech recognition service is having issues: {e}")
        return ""

def process_query(query):
    if "hello" in query or "hi" in query:
        greet()

    elif "time" in query:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}.")

    elif "date" in query:
        today = datetime.date.today().strftime("%B %d, %Y")
        speak(f"Today's date is {today}.")

    elif "open website" in query:
        website = query.replace("open website", "").strip()
        if not website:
            speak("Which website do you want me to open?")
            website = listen()
            if not website:
                return
        url = "https://" + website  # or http:// if needed
        webbrowser.open(url)
        speak(f"Opening {website}.")

    elif "wikipedia" in query:
        try:
            query = query.replace("wikipedia", "").strip()
            results = wikipedia.summary(query, sentences=2)
            speak(f"According to Wikipedia, {results}")
        except wikipedia.exceptions.PageError:
            speak("Wikipedia couldn't find that.")
        except wikipedia.exceptions.DisambiguationError as e:
            speak("Wikipedia found multiple results. Here are some options:")
            print(e.options)
            # You might want to add code here to let the user choose

    elif "calculate" in query or "what is" in query or "solve" in query:
        try:
            res = client.query(query)
            answer = next(res.results).text
            speak(f"The answer is {answer}.")
        except Exception as e:
            speak("I couldn't calculate that.")
            print(f"Wolfram Alpha Error: {e}")

    elif "exit" in query or "quit" in query or "close" in query:
        speak("Goodbye.")
        exit()

    else:
        speak("I can't understand that MotherFucker.")

if __name__ == "__main__":
    greet()
    while True:
        query = listen()
        if query:
            process_query(query)