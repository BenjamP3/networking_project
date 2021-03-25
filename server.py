# Server file
# load modules
import socket
import threading
import time
import configparser

LENGTH = 64
MSG_FMT = "utf-8"
DIS_MSG = "|STOP|"

# create TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# read in server, port, and valid commands from config file to define server socket
parser = configparser.ConfigParser()
parser.read('sys_defaults.ini')
list_of_cmds = parser.get('commands', 'list')
COMMANDS = list_of_cmds.split(' ')
SERVER = parser.get('server_info', 'address') # Should be loop back address
PORT = int(parser.get('server_info', 'port'))
ADDRESS = (SERVER, PORT)
server.bind(ADDRESS)

# receives client and handles each client's requests
def client_handler(connection, address):
    print(f"{time.ctime(time.time())} {address} connection started.")
    client_alive = True
    while (client_alive):
        length = int(connection.recv(LENGTH).decode(MSG_FMT))
        message = connection.recv(length).decode(MSG_FMT)
        if (DIS_MSG == message):
            client_alive = False
            connection.send("Connection terminated.".encode(MSG_FMT))
        else:
            print(f"{time.ctime(time.time())} {address} echoed \"{message}\"")
            connection.send("Messaged received.".encode(MSG_FMT))

    print(f"{time.ctime(time.time())} {address} connection terminated.")
    connection.close()

# starts the server and receives each connection
def start_server():
	server.listen()
	print(f"{time.ctime(time.time())} |SERVER| waiting for connections ...")
	while (1):
		connection, c_address = server.accept()
		thread = threading.Thread(target=client_handler, args=(connection, c_address))
		thread.start()
        
# STARTING SERVER
print(f"{time.ctime(time.time())} |SERVER| starting up on port {PORT} ...")
start_server()
