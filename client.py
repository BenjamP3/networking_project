# Client file
# load modules
import socket
import configparser
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

# create TCP/IP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
LENGTH = 64
MSG_FMT = "utf-8"
DIS_MSG = "|STOP|"

# read in server, port, and valid commands from config file
parser = configparser.ConfigParser()
parser.read('sys_defaults.ini')
list_of_cmds = parser.get('commands', 'cmd')
COMMANDS = list_of_cmds.split(' ')
SERVER = parser.get('server_info', 'address') # Should be loop back address
PORT = int(parser.get('server_info', 'port'))
ADDRESS = (SERVER, PORT)
validConnection = ['True']

# sends message to server and prints out acknowledgement
def send_message(message):
    msg = message.encode(MSG_FMT)
    msg_length = len(msg)
    msg_length = str(msg_length).encode(MSG_FMT)
    msg_length = msg_length + b' ' * (LENGTH - len(msg_length))
    client.send(msg_length)
    client.send(msg)

# prints commands with hints to the console
def print_commands_hints():
    output = "Command definitions:"
    for ind in range(len(COMMANDS)):
        cmd = COMMANDS[ind]
        if (cmd == "|STOP|"):
            cmd = 'stop'
        cmd_def = parser.get('commands', cmd)
        output = output + "\n   " + cmd_def
    output = output + "\n   \"help\" - Lists definitions of other available commands"
    updateFeedback(output)

# prints to console all of the acceptable commands
def print_commands(command):
    output = f"Invalid command: {command}\nCommands:"
    for cmd in COMMANDS:
        output = output + "\n   " + cmd
    
    updateFeedback(output)

# determines if the command is valid. returns true if valid, returns false if not valid
def check_command(command):
    valid = False
    if (command in COMMANDS):
        valid = True
    return valid

# updates large textbox with feedback
def updateFeedback(msg):
    feedback.config(state='normal')
    feedback.delete(1.0, 'end')
    feedback.insert('1.0', msg)
    feedback.config(state='disabled')

# captures command from GUI
def submitQuery(event=None):
    updateFeedback("")
    command = query.get()
    arguments = command.split(' ')
    valid = check_command(arguments[0])
    if (valid):
        send_message(command)
        response = client.recv(2048).decode(MSG_FMT)
        if (arguments[0] == DIS_MSG):
            validConnection[0] = 'False'
            root.destroy()
            print(response)
        else:
            updateFeedback(response)
            query.delete(0, 'end')
    else:
        if (arguments[0].lower() == 'help'):
            print_commands_hints()
        else:
            print_commands(command)
        query.delete(0, 'end')

# clears query and result from server
def clearGUI():
    query.delete(0, 'end')
    updateFeedback("")

root = tk.Tk()
#tmp = root.geometry("700x500")
tmp = root.title("One Command Weather App")
root.configure(background="#69C8DF")
root.bind('<Return>', submitQuery)
#Style colors
style = ttk.Style()
style.configure('TFrame',background="#69C8DF", font = ('Dubai', 15))
style.configure('TButton',background="#69C8DF", font = ('Dubai', 15))
style.configure('TLabel',background="#69C8DF", font = ('Dubai', 15))

#Header area of GUI
header = ttk.Frame(root)
header.pack()
header_img = Image.open("weather.jpg")
header_img = header_img.resize((150, 150), Image.ANTIALIAS)
header_img = ImageTk.PhotoImage(header_img)
ttk.Label(header, image = header_img).grid(row=0, column=0, rowspan=2, padx=5)
ttk.Label(header, text="Welcome to One Command Weather!").grid(row=0, column=1, padx=5)
ttk.Label(header, text="Type \"help\" to view a list of commands.").grid(row=1, column=1, padx=5)

#Body area of GUI
body = ttk.Frame(root)
body.pack()
ttk.Label(body, text="Query:").grid(row=0, column=0, columnspan=2, padx=5)
ttk.Label(body, text="Result:").grid(row=2, column=0, columnspan=2, padx=5)
query = ttk.Entry(body, width = 60)
query.grid(row=1, column=0, columnspan=2, padx=5)

container = ttk.Frame(body)
container.grid(row=3, column=0, columnspan=2, padx=5)
feedback = tk.Text(container, width=124, height = 25)
feedback.pack(side=tk.LEFT, fill=tk.BOTH)
feedback.config(wrap='word')
feedback.config(state='disabled')
scroll = tk.Scrollbar(container, orient = tk.VERTICAL, command = feedback.yview)
scroll.pack(side=tk.RIGHT, fill=tk.Y)
feedback.config(yscrollcommand = scroll.set)
		
ttk.Button(body, text="Submit", command = submitQuery).grid(row=4, column=0, padx=5)
ttk.Button(body, text="Clear", command = clearGUI).grid(row=4, column=1, padx=5)

#Footer area of GUI
footer = ttk.Frame(root)
footer.pack()
ttk.Label(footer, text="Created by Benjamin Petrick @2021").grid(row=0, column=0, padx=5)

# create TCP/IP socket and stablish connection to server
try:
    client.connect(ADDRESS)
except:
    updateFeedback("ERROR: Unable to connect to server. Program terminated.")
    validConnection[0] = 'False'

# start client process
if (validConnection[0] == 'True'):
    # prints my laptop ip address to show two IP addresses are being used (my laptop (192.168.56.1) and the loopback address (127.0.0.1))
    #print("Device IP Address: " + str(socket.gethostbyname(socket.gethostname())))    
    command = f"Connection secured to {SERVER}. Type \"help\" to see definitions of commands."
    print(command)
    updateFeedback(command)
    root.mainloop()
    
    #If user exits out of window, this closes the connection
    if (validConnection[0] == 'True'):
        send_message(DIS_MSG)
        response = client.recv(2048).decode(MSG_FMT)
        print(response)
