#python version 3.11
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib


# ============================================================
# TEXT TO SPEECH
# ============================================================

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")

if voices:
    engine.setProperty("voice", voices[0].id)

engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)


def speak(audio):
    print("JARVIS:", audio)
    engine.say(audio)
    engine.runAndWait()


# ============================================================
# GREETING
# ============================================================

def wishMe():
    hour = datetime.datetime.now().hour

    if 0 <= hour < 12:
        speak("Good Morning!")

    elif 12 <= hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am Jarvis Sir. Please tell me how may I help you?")


# ============================================================
# SPEECH RECOGNITION
# ============================================================

def takeCommand():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("\nListening...")

        recognizer.pause_threshold = 1
        recognizer.energy_threshold = 300
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=10
            )

        except sr.WaitTimeoutError:
            print("Listening timeout.")
            return "None"

    try:

        print("Recognizing...")

        query = recognizer.recognize_google(
            audio,
            language="en-in"
        )

        print(f"User said: {query}")

        return query

    except sr.UnknownValueError:

        print("Could not understand audio.")
        speak("Sorry, I didn't understand that.")

        return "None"

    except sr.RequestError:

        print("Speech recognition service unavailable.")
        speak("Speech recognition service is currently unavailable.")

        return "None"

    except Exception as e:

        print("Speech Error:", e)

        return "None"


# ============================================================
# EMAIL
# ============================================================

def sendEmail(to, content):

    try:

        server = smtplib.SMTP("smtp.gmail.com", 587)

        server.ehlo()
        server.starttls()

        # IMPORTANT:
        # Do NOT put your real Gmail password directly in code.
        #
        # Use a Gmail App Password instead.

        sender_email = "your_email@gmail.com"
        sender_password = "your_app_password"

        server.login(sender_email, sender_password)

        server.sendmail(
            sender_email,
            to,
            content
        )

        server.quit()

        return True

    except Exception as e:

        print("Email Error:", e)

        return False


# ============================================================
# WIKIPEDIA
# ============================================================

def searchWikipedia(query):

    try:

        speak("Searching Wikipedia...")

        search_query = query.replace("wikipedia", "").strip()

        if not search_query:
            speak("What should I search on Wikipedia?")
            return

        results = wikipedia.summary(
            search_query,
            sentences=2
        )

        print("\nWikipedia Result:")
        print(results)

        speak("According to Wikipedia.")
        speak(results)

    except wikipedia.exceptions.DisambiguationError:

        speak(
            "There are multiple results for that topic. "
            "Please be more specific."
        )

    except wikipedia.exceptions.PageError:

        speak(
            "I could not find that topic on Wikipedia."
        )

    except Exception as e:

        print("Wikipedia Error:", e)

        speak(
            "Sorry, I could not access Wikipedia right now."
        )


# ============================================================
# OPEN WEBSITE
# ============================================================

def openWebsite(url, name):

    speak(f"Opening {name}")

    try:
        webbrowser.open(url)

    except Exception as e:

        print("Browser Error:", e)

        speak("I could not open the website.")


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    wishMe()

    while True:

        query = takeCommand().lower()

        if query == "none":
            continue

        # ----------------------------------------------------
        # WIKIPEDIA
        # ----------------------------------------------------

        if "wikipedia" in query:

            searchWikipedia(query)

        # ----------------------------------------------------
        # YOUTUBE
        # ----------------------------------------------------

        elif "open youtube" in query:

            openWebsite(
                "https://www.youtube.com",
                "YouTube"
            )

        # ----------------------------------------------------
        # GOOGLE
        # ----------------------------------------------------

        elif "open google" in query:

            openWebsite(
                "https://www.google.com",
                "Google"
            )

        # ----------------------------------------------------
        # STACK OVERFLOW
        # ----------------------------------------------------

        elif "open stackoverflow" in query:

            openWebsite(
                "https://stackoverflow.com",
                "Stack Overflow"
            )

        # ----------------------------------------------------
        # PLAY MUSIC
        # ----------------------------------------------------

        elif "play music" in query:

            music_dir = r"D:\Songs\Charkha Live"

            try:

                songs = os.listdir(music_dir)

                if songs:

                    song = os.path.join(
                        music_dir,
                        songs[0]
                    )

                    speak("Playing music.")

                    os.startfile(song)

                else:

                    speak("There are no songs in the music folder.")

            except FileNotFoundError:

                speak("I could not find your music folder.")

            except Exception as e:

                print("Music Error:", e)

                speak("I could not play the music.")

        # ----------------------------------------------------
        # TIME
        # ----------------------------------------------------

        elif "the time" in query or "what time" in query:

            current_time = datetime.datetime.now().strftime(
                "%I:%M %p"
            )

            speak(
                f"Sir, the time is {current_time}"
            )

        # ----------------------------------------------------
        # OPEN VS CODE
        # ----------------------------------------------------

        elif "open code" in query or "open vs code" in query:

            code_paths = [

                r"C:\Users\Haris\AppData\Local\Programs\Microsoft VS Code\Code.exe",

                r"C:\Users\abhij\AppData\Local\Programs\Microsoft VS Code\Code.exe",

                r"C:\Program Files\Microsoft VS Code\Code.exe"

            ]

            opened = False

            for code_path in code_paths:

                if os.path.exists(code_path):

                    speak("Opening Visual Studio Code.")

                    os.startfile(code_path)

                    opened = True

                    break

            if not opened:

                speak(
                    "I could not find Visual Studio Code."
                )

        # ----------------------------------------------------
        # EMAIL
        # ----------------------------------------------------

        elif "email to abhishek" in query:

            try:

                speak("What should I say?")

                content = takeCommand()

                if content == "none":

                    continue

                to = "abhishekyourEmail@gmail.com"

                success = sendEmail(
                    to,
                    content
                )

                if success:

                    speak("Email has been sent successfully.")

                else:

                    speak(
                        "Sorry, I was unable to send the email."
                    )

            except Exception as e:

                print("Email Error:", e)

                speak(
                    "Sorry, I was not able to send this email."
                )

        # ----------------------------------------------------
        # GREETING
        # ----------------------------------------------------

        elif "hello" in query or "hi jarvis" in query:

            speak(
                "Hello Sir. How can I help you?"
            )

        # ----------------------------------------------------
        # STOP JARVIS
        # ----------------------------------------------------

        elif (
            "exit" in query
            or "quit" in query
            or "shutdown jarvis" in query
            or "goodbye" in query
        ):

            speak(
                "Goodbye Sir. Have a great day."
            )

            break

        # ----------------------------------------------------
        # UNKNOWN COMMAND
        # ----------------------------------------------------

        else:

            print("No query matched.")

            speak(
                "I don't have an action for that command yet."
            )
