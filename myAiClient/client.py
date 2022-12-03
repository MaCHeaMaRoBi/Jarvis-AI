import pyttsx3
import speech_recognition as sr
import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(("192.168.0.117", 6969))


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
            if 'jarvis' in text:
                text = text.replace('jarvis', '')
    except:
        print("Sorry could not recognize what you said")
        return None
    return text


def run_jarvis():
    message = get_command()
    if message is not None:
        # if "goodbye" or "bye" in message:
        # break

        clientSocket.send(message.encode())
        print("Sended: ", message)

        dataFromServer = clientSocket.recv(20480)
        print("Received: ", dataFromServer.decode())
        talk(dataFromServer.decode())


while True:
    run_jarvis()
