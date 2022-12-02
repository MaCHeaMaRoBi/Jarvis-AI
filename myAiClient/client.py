import pyttsx3
import speech_recognition as sr
import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(("94.52.177.116", 6969))


r = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def get_command():
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except:
            print("Sorry could not recognize what you said")
            return ""


while True:
    message = get_command()
    if message != "":

        clientSocket.send(message.encode())

        dataFromServer = clientSocket.recv(1024)
        print(dataFromServer.decode())
        talk(dataFromServer.decode())
