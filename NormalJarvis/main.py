import sys
import pyttsx3
import speech_recognition as sr
# import nltk
import datetime
from AppOpener import run
from neuralintents import GenericAssistant
import requests, json
import wolframalpha
import pyjokes
import math
import webbrowser

# nltk.download('omw-1.4')

r = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 175)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def talk(text):
    engine.say(text)
    print("Jarvis: " + text)
    engine.runAndWait()


def get_command():
    global r
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.2)
            audio = r.listen(source)
            text = r.recognize_google(audio)
            print("You: " + text)
            return text
    except sr.UnknownValueError:
        r = sr.Recognizer()
        print("Sorry could not recognize what you said")


def time_now():
    str_time = datetime.datetime.now().strftime("%H:%M")
    talk(f"Sir, the time is {str_time}")


def change_username():
    talk("What do you want me to call you?")
    global r
    done = False

    while not done:
        try:
            with sr.Microphone() as mic:

                r.adjust_for_ambient_noise(mic, duration=0.2)
                audio = r.listen(mic)
                new_username = r.recognize_google(audio)

                with open('username.txt', 'w') as f:
                    f.write(new_username)

                done = True

                talk(f"Your new username is {new_username}")
        except sr.UnknownValueError:
            r = sr.Recognizer()
            talk("I did not understand, sir. Please try again")


def train_now():
    talk("Ok, starting training")
    assistant.train_model()
    assistant.save_model()
    assistant.load_model('jarvis_model')
    talk("The training is finished, sir")


def open_app():
    talk("What app do you want to open?")
    global r
    done = False

    while not done:
        try:
            with sr.Microphone() as mic:

                r.adjust_for_ambient_noise(mic, duration=0.2)
                audio = r.listen(mic)
                app = r.recognize_google(audio)

                run(app)
                done = True

                talk(f"Opened {app}")
        except sr.UnknownValueError:
            r = sr.Recognizer()
            talk("I did not understand, sir. Please try again")


def repeat():
    global r
    done = False

    while not done:
        try:
            with sr.Microphone() as mic:

                r.adjust_for_ambient_noise(mic, duration=0.2)
                audio = r.listen(mic)
                text = r.recognize_google(audio)
                talk(text)
                done = True
        except sr.UnknownValueError:
            r = sr.Recognizer()
            talk("I did not understand, sir. Please try again")


def exit_jarvis():
    talk("Goodbye sir")
    sys.exit(0)


def show_username():
    with open('username.txt', 'r') as f:
        talk(f"Your username is {f.read()}")


def play_song():
    talk("I cannot")


def weather():
    api_key = "0ff96b39bdc83f5eb47e57fbcaa9d598"

    # base_url variable to store url
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = "mioveni"

    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        z = x["weather"]
        weather_description = z[0]["description"]

        talk("There are " + str(math.floor(current_temperature - 273.15)) + "°C " + "and " + str(weather_description))

    else:
        print(" City Not Found ")


def wolf_frame():
    talk("What do you want to search, sir?")
    client = wolframalpha.Client("JL9GTT-XT7A9KULRY")

    global r
    done = False

    while not done:
        try:
            with sr.Microphone() as mic:

                r.adjust_for_ambient_noise(mic, duration=0.2)
                audio = r.listen(mic)
                text = r.recognize_google(audio)

                res = client.query(text)

                try:
                    talk(next(res.results).text)
                except StopIteration:
                    print("No results")
                done = True
        except sr.UnknownValueError:
            r = sr.Recognizer()
            talk("I did not understand, sir. Please try again")


def joke():
    talk(pyjokes.get_joke())


def create_note():
    global r
    talk("What do you want to write onto your note?")
    done = False

    while not done:
        try:
            with sr.Microphone() as mic:

                r.adjust_for_ambient_noise(mic, duration=0.2)
                audio = r.listen(mic)
                note = r.recognize_google(audio)

                talk("Choose a filename!")

                r.adjust_for_ambient_noise(mic, duration=0.2)
                audio = r.listen(mic)
                filename = r.recognize_google(audio)
                filename = filename.lower()

                with open(f"notes/{filename}", 'w') as f:
                    f.write(note)
                    done = True
                    talk(f"I successfully created a note {filename}")
        except sr.UnknownValueError:
            r = sr.Recognizer()
            talk("I did not understand, sir. Please try again")


def web_search():
    global r

    talk("What do you want to search?")

    done = False

    while not done:
        try:
            with sr.Microphone() as mic:

                r.adjust_for_ambient_noise(mic, duration=0.2)
                audio = r.listen(mic)
                query = r.recognize_google(audio)

                webbrowser.open(f"www.google.com/search?q={query}")

                done = True
        except sr.UnknownValueError:
            r = sr.Recognizer()
            talk("I did not understand, sir. Please try again")


mappings = {
    'time': time_now,
    'train': train_now,
    'change_username': change_username,
    'open_app': open_app,
    'repeat': repeat,
    'exit': exit_jarvis,
    'show_username': show_username,
    'play_song': play_song,
    'weather': weather,
    'find_out_something': wolf_frame,
    'joke': joke,
    'create_note': create_note,
    'web_search': web_search
}

assistant = GenericAssistant(
    'intents.json', intent_methods=mappings, model_name="jarvis_model")
assistant.load_model('jarvis_model')


# assistant.train_model()
# assistant.save_model()


def wish_me():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        talk("Good Morning Sir !")

    elif 12 <= hour < 18:
        talk("Good Afternoon Sir !")

    else:
        talk("Good Evening Sir !")

    ass_name = "Jarvis 1 point o"
    talk("I am your Assistant")
    talk(ass_name)


def username():
    with open('username.txt', 'r') as f:
        if f.read() == "":
            change_username()


def run_jarvis():
    while True:
        message = get_command()
        if message is not None:
            res = assistant.request(message)
            if res is not None:
                talk(res)


if __name__ == "__main__":
    wish_me()
    username()
    run_jarvis()
