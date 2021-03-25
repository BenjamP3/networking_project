# Client file
# load modules
import socket
import configparser

LENGTH = 64
MSG_FMT = "utf-8"
DIS_MSG = "|STOP|"

# create TCP/IP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# read in server, port, and valid commands from config file
parser = configparser.ConfigParser()
parser.read('sys_defaults.ini')
list_of_cmds = parser.get('commands', 'list')
COMMANDS = list_of_cmds.split(' ')
SERVER = parser.get('server_info', 'address') # Should be loop back address
PORT = int(parser.get('server_info', 'port'))
ADDRESS = (SERVER, PORT)

# sends message to server and prints out acknowledgement
def send_message(message):
    msg = message.encode(MSG_FMT)
    msg_length = len(msg)
    msg_length = str(msg_length).encode(MSG_FMT)
    msg_length = msg_length + b' ' * (LENGTH - len(msg_length))
    client.send(msg_length)
    client.send(msg)
    print(client.recv(2048).decode(MSG_FMT))

# prints to console all of the acceptable commands
def print_commands():
    print("Commands:")
    for cmd in COMMANDS:
        print("    " + cmd)

# determines if the command is valid. returns true if valid, returns false if not valid
def check_command(command):
    valid = False
    if (command in COMMANDS):
        valid = True
    return valid

# obtains the input from the user. returns a valid command with arguments as a string
def obtain_command():
    command = input("$$ ")
    arguments = command.split(' ')
    while (not check_command(arguments[0])):
        print("Invalid command: {command}")
        print_commands()
        command = input("$$ ")
        arguments = command.split(' ')
    return command

# runs client process
def start_client():
    command = ""
    print(f"Connection secured to {SERVER}. Type \"help\" to see definitions of commands.")
    while (command != DIS_MSG):
        command = obtain_command()
        send_message(command)

# create TCP/IP socket and stablish connection to server
validConnection = True
try:
    client.connect(ADDRESS)
except:
    print("ERROR: Unable to connect to server. Program terminated.")
    validConnection = False

# start client process
if (validConnection):
    # prints my laptop ip address to show two IP addresses are being used (my laptop and the loopback address)
    print("Laptop IP Address: " + str(socket.gethostbyname(socket.gethostname())))
    start_client()
