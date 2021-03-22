# Server file
#load additional Python module
import socket
import threading

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 4422
ADDRESS = (SERVER, PORT)
LENGTH = 64
MSG_FMT = "utf-8"
DIS_MSG = "|STOP|"

# create TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

def client_handler(connection, address):
    print(f"|CLIENT {address}| connection started.")
    client_alive = True
    while (client_alive):
        length = int(connection.recv(LENGTH).decode(MSG_FMT))
        message = connection.recv(length).decode(MSG_FMT)
        if (DIS_MSG == message):
            client_alive = False
            connection.send("Connection Terminated.".encode(MSG_FMT))
        else:
            print(f"|CLIENT {address}| echoed \"{message}\"")
            connection.send("Messaged received.".encode(MSG_FMT))

    print(f"|CLIENT {address}| connection terminated.")
    connection.close()

# Starts the server and receives each connection
def start_server():
	server.listen()
	print("|SERVER LISTEN| waiting for connections ...")
	while (1):
		connection, c_address = server.accept()
		thread = threading.Thread(target=client_handler, args=(connection, c_address))
		thread.start()

print(f"|SERVER START| starting up on {SERVER}:{PORT} ...")
start_server()
