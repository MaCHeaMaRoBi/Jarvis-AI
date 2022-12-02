import random
import json
import pickle
import numpy as np
import pyttsx3
import speech_recognition as sr
import socket

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(("192.168.0.117", 6969))
serverSocket.listen()

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


clients = []

# talk("At your service sir")
while True:
    (clientConnected, clientAddress) = serverSocket.accept()
    print("Accepted a connection request from %s:%s" %
          (clientAddress[0], clientAddress[1]))
    clients.append({clientAddress[0], 0})
    print(clients)

    while True:
        dataFromClient = clientConnected.recv(1024)
        print(dataFromClient.decode())
        ints = predict_class(dataFromClient.decode())
        res = get_response(ints, intents)
        clientConnected.send(res.encode())
