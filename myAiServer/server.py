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
from neuralintents import GenericAssistant
import sys


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

        results = str(
            i) + "   " + str(all_address[i][0]) + "   " + str(all_address[i][1]) + "\n"

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
        print("Received: ", dataFromClient.decode())
        # ints = predict_class(dataFromClient.decode())
        # res = get_response(ints, intents)
        res = assistant.request(dataFromClient.decode())
        print(res)
        if res is None:
            break
        conn.send(res.encode())
        print("Sended: ", res)
        # except:
        #     print("Error sending commands")
        #     break


def what_time_is_it():
    print('is my cock')


mappings = {
    'time': what_time_is_it
}

assistant = GenericAssistant(
    'intents.json', intent_methods=mappings, model_name="jarvis_model")
assistant.load_model('jarvis_model')
# assistant.train_model()
# assistant.save_model()


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
