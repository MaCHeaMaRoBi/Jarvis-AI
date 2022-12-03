import random
import json
import pickle
import numpy as np
import pyttsx3
import speech_recognition as sr
import socket
import threading
import time
from queue import Queue

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model


lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbotmodel.h5')


r = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


# def talk(text):
#     engine.say(text)
#     engine.runAndWait()


# def get_command():
#     with sr.Microphone() as source:
#         audio = r.listen(source)
#         try:
#             text = r.recognize_google(audio)
#             return text
#         except:
#             print("Sorry could not recognize what you said")
#             return ""


def clean_up_sentece(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words


def bag_of_words(sentence):
    sentence_words = clean_up_sentece(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)


def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list


def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result


NUMBER_OF_THREADS = 2
JOB_NUMBER = {1, 2}
queue = Queue()
all_connections = []
all_address = []


def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 6969
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()

# ////////////#
# OLD CODE#
# ////////////#

# Closing previous connections whe server.py restarts


def accept_connections():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)  # prevents timeout

            all_connections.append(conn)
            all_address.append(address)

            print("Connection has been established: ", address[0])

        except:
            print("Error accepting connections")


# 2nd thread functions - selects all the clients

def start_jarvis():
    while True:
        cmd = input('jarvis> ')

        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        else:
            print("command not recognized")


def list_connections():
    results = ''

    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode('HEARTBEAT'))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_address[i]
            continue

        results = str(i) + "   " + str(all_address[i][0]) + "   " + str(all_address[i][1]) + "\n"

    print("---- Clients ----" + "\n" + results)


def get_target(cmd):
    try:
        target = cmd.replace('select ', "")
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to: " + str(all_address[target][0]))
        print(str(all_address[target][0]) + ">", end="")
        return conn

    except:
        print("Selection not valid")
        return None


def send_target_commands(conn):
    while True:
        # try:
        dataFromClient = conn.recv(20480)
        if not dataFromClient:           # Receive nothing? client closed connection,
            break
        print("Received", dataFromClient.decode())
        ints = predict_class(dataFromClient.decode())
        res = get_response(ints, intents)
        conn.send(res.encode())
        print("Sended: ", res)
        # except:
        #     print("Error sending commands")
        #     break


def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accept_connections()
        if x == 2:
            start_jarvis()

        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()


create_workers()
create_jobs()


# ////////////#
# OLD CODE#
# ////////////#

# talk("At your service sir")
# while True:
#     (clientConnected, clientAddress) = serverSocket.accept()
#     print("Accepted a connection request from %s:%s" %
#           (clientAddress[0], clientAddress[1]))
#     clients.append({clientAddress[0], 0})
#     print(clients)

#     while True:
#         dataFromClient = clientConnected.recv(1024)
#         if not dataFromClient:           # Receive nothing? client closed connection,
#             clients.pop()
#             break
#         print("Received", dataFromClient.decode())
#         ints = predict_class(dataFromClient.decode())
#         res = get_response(ints, intents)
#         clientConnected.send(res.encode())
#         print("Sended: ", res)
