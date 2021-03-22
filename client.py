# Client file
import socket

SERVER = "192.168.56.1"
PORT = 4422
ADDRESS = (SERVER, PORT)
LENGTH = 64
MSG_FMT = "utf-8"
DIS_MSG = "|STOP|"

# create TCP/IP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

# Sends message to server and prints out acknowledgement
def send_message(message):
    msg = message.encode(MSG_FMT)
    msg_length = len(msg)
    msg_length = str(msg_length).encode(MSG_FMT)
    msg_length = msg_length + b' ' * (LENGTH - len(msg_length))
    client.send(msg_length)
    client.send(msg)
    print(client.recv(2048).decode(MSG_FMT))


message = ""
print("Type \"|STOP|\" to close connection.")
while (message != DIS_MSG):
    message = input(">>> ")
    msg_chunks = message.split(' ')
    if (msg_chunks[0] == "echo"):
        message = message[len("echo") + 1:len(message)]
        send_message(message)
    if (msg_chunks[0] == "today"):
        message = message[len("today") + 1:len(message)]
        send_message(message)
    if (msg_chunks[0] == "tomorrow"):
        message = message[len("tomorrow") + 1:len(message)]
        send_message(message)
    if (msg_chunks[0] == "rain"):
        message = message[len("rain") + 1:len(message)]
        send_message(message)
    if (message == DIS_MSG):
        send_message(DIS_MSG)
        
