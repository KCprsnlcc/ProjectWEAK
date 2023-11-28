import pyttsx3
import wikipedia
import speech_recognition as sr
import keyboard  # Import the keyboard library

# Initialize the Text-to-Speech engine
engine = pyttsx3.init()

# Initialize the speech recognition
recognizer = sr.Recognizer()


def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        command = ""

        try:
            command = recognizer.recognize_google(audio)
            print("You said: " + command)
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
        except sr.RequestError as e:
            print("Sorry, I encountered an error while processing your request: {0}".format(e))

        return command


def main():
    speak("Hello, I'm Thursday. I'm an AI that will assist you in searching on Wikipedia.")

    while True:
        # Add a keyboard event to trigger listening when the Space key is pressed
        keyboard.wait("space")
        speak("What would you like to search for on Wikipedia?")
        query = listen()
        try:
            result = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia, " + result)
        except wikipedia.exceptions.DisambiguationError as e:
            speak("There are multiple options. Can you be more specific?")
        except wikipedia.exceptions.PageError as e:
            speak("I couldn't find any results for that query.")
        keyboard.wait("space")  # Add this line to wait for the Space key again before the next search


if __name__ == "__main__":
    main()
