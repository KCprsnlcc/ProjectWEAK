import pyttsx3
import wikipedia
import speech_recognition as sr
import datetime

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


def get_current_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")  # Example: 03:45 PM
    return current_time


def main():
    speak("Hello my name is Jacob,I'm an AI that will assist you in searching on Wikipedia. what is your name?")

    user_name = listen()

    if user_name:
        speak(f"Nice to meet you, {user_name}! How can I assist you today?")
    else:
        speak("I'm sorry, I didn't catch your name. How can I assist you today?")
    conversation = []  # Store conversation history

    while True:
        command = listen().lower()

        if "reset" in command:
            speak("Resetting the conversation. How can I assist you now?")
            conversation = []  # Clear conversation history
            continue  # Continue listening

        if "stop" in command:
            speak("Goodbye! Thank you for using me as your assistant.")
            break

        if "jacob" in command:
            speak("What would you like to search for")
            query = listen()
            try:
                result = wikipedia.summary(query, sentences=2)
                conversation.append(f"{result}")
                speak(conversation[-1])  # Speak the most recent result
            except wikipedia.exceptions.DisambiguationError as e:
                speak("There are multiple options. Can you be more specific?")
            except wikipedia.exceptions.PageError as e:
                speak("I couldn't find any results for that query.")

        elif "current time" in command:
            current_time = get_current_time()

            speak(f"The current time is {current_time}.")

        elif "tell me a joke" in command or "can you tell jokes" in command:
            joke = pyjokes.get_joke()
            speak(joke)

        else:
            speak("I'm not sure how to respond to that.")
            conversation.append("User: " + command)  # Store user's input in the conversation history


main()
