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

def send_message(message):
    msg = message.encode(MSG_FMT)
    msg_length = len(msg)
    msg_length = str(msg_length).encode(MSG_FMT)
    msg_length = msg_length + b' ' * (LENGTH - len(msg_length))
    client.send(msg_length)
    client.send(msg)
    
send_message("Hi server, my name is ben.")
msg = input(">>> ")
send_message(msg)
msg = input(">>> ")
send_message(msg)
send_message(DIS_MSG)
