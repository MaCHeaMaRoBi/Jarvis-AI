import pyttsx3
import speech_recognition as sr
import numpy as np
import nltk
nltk.download('omw-1.4')
from neuralintents import GenericAssistant


r = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def get_command():
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.2)
            audio = r.listen(source)
            text = r.recognize_google(audio)
            return text
    except sr.UnknownValueError:
        print("Sorry could not recognize what you said")
        return None


def time_now():
    print("ma cac")

def train_now():
    talk("Ok, starting training")
    assistant.train_model()
    assistant.save_model()
    assistant.load_model('jarvis_model')
    talk("The training is finished, sir")


mappings = {
    'time': time_now,
    'train': train_now
}

assistant = GenericAssistant(
    'intents.json', intent_methods=mappings, model_name="jarvis_model")
assistant.load_model('jarvis_model')
# assistant.train_model()
# assistant.save_model()


def run_jarvis():
    while True:
        message = get_command()
        if message is not None:
            print("You: ", message)

            res = assistant.request(message)
            if res is not None:
                print("Jarvis: ", res)
                talk(res)


if __name__ == "__main__":
    run_jarvis()
