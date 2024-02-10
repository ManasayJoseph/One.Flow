import socket

import pyperclip

HEADER = 16
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.4"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# def make_sendable(value):
    

def send(msg , type):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


def recv():
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)
    return msg


def start():
    previous_clipboard = None

    while True:
        current_clipboard = pyperclip.paste()
        # print(previous_clipboard , current_clipboard)
        if current_clipboard == previous_clipboard:
            state = "="

        else:
            previous_clipboard = current_clipboard
            state = "!"
        if state == "!" :
            send(current_clipboard)
            print(recv())
            print(recv())
        
        # val = input("Give me thanos")
        # if val == "send":
        #     send(val)
        #     print(recv())
        # elif val == "break":
        #     send(DISCONNECT_MESSAGE)


start()
