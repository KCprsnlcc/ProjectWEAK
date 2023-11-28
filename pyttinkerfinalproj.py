import wikipedia
import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time

class WikipediaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wikipedia Voice Assistant")

        # Set the background color with a gradient effect
        self.set_gradient_background()

        # Text-to-speech engine
        self.engine = pyttsx3.init()

        # GUI components
        self.create_gui()

        # Speech recognition setup
        self.recognizer = sr.Recognizer()

    def set_gradient_background(self):
        # Create a frame with a gradient background
        frame = tk.Frame(self.root, bg="#008080")  # Teal color code: #008080
        frame.place(relwidth=1, relheight=1)

    def create_gui(self):
        # Entry for search query
        self.query_entry = tk.Entry(self.root, width=40)
        self.query_entry.grid(row=0, column=0, padx=10, pady=10)

        # Search button
        search_button = tk.Button(self.root, text="Search", command=self.search_wikipedia)
        search_button.grid(row=0, column=1, padx=10, pady=10)

        # ScrolledText for displaying results
        self.results_text = scrolledtext.ScrolledText(self.root, width=60, height=10)
        self.results_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Start/Stop listening button
        self.listen_button = tk.Button(self.root, text="Start Listening", command=self.toggle_listening)
        self.listen_button.grid(row=2, column=0, columnspan=2, pady=10)

    def search_wikipedia(self):
        query = self.query_entry.get()
        try:
            result = wikipedia.summary(query, sentences=2)
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, result)
            self.speak(result)
        except wikipedia.exceptions.DisambiguationError as e:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"Ambiguous search query. Please be more specific.\n{e}")
            self.speak(f"Ambiguous search query. Please be more specific.")
        except wikipedia.exceptions.PageError:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "No matching results found.")
            self.speak("No matching results found.")

    def toggle_listening(self):
        if self.listen_button["text"] == "Start Listening":
            self.listen_button["text"] = "Stop Listening"
            self.listen_thread = threading.Thread(target=self.listen_for_query)
            self.listen_thread.start()
        else:
            self.listen_button["text"] = "Start Listening"
            self.recognizer.stop_listen()

    def listen_for_query(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "Listening for query...")
            self.speak("Listening for query. Please speak.")
            audio = self.recognizer.listen(source)

        try:
            query = self.recognizer.recognize_google(audio)
            self.query_entry.delete(0, tk.END)
            self.query_entry.insert(tk.END, query)
            self.search_wikipedia()
        except sr.UnknownValueError:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "Sorry, I could not understand the query.")
            self.speak("Sorry, I could not understand the query.")
        except sr.RequestError as e:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"Error connecting to Google Speech Recognition API: {e}")
            self.speak(f"Error connecting to Google Speech Recognition API: {e}")

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()


if __name__ == "__main__":
    root = tk.Tk()
    app = WikipediaApp(root)
    root.mainloop()
