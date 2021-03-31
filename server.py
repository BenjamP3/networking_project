# Server file
# load modules
import socket
import threading
import time
import configparser
from geopy.geocoders import Nominatim
import requests
import logging
import datetime as dt

logging.basicConfig(filename="server_logging.log", level=logging.INFO, format="%(message)s")
geolocator = Nominatim(user_agent="local_server_app")
LENGTH = 64
MSG_FMT = "utf-8"
DIS_MSG = "|STOP|"
WEEKDAYS = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")

# create TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# read in server, port, and valid commands from config file to define server socket
parser = configparser.ConfigParser()
parser.read('sys_defaults.ini')
list_of_cmds = parser.get('commands', 'cmd')
COMMANDS = list_of_cmds.split(' ')
SERVER = parser.get('server_info', 'address') # Should be loop back address
PORT = int(parser.get('server_info', 'port'))
ADDRESS = (SERVER, PORT)
server.bind(ADDRESS)

logging.info("----------------------------------")
logging.info(f"{time.ctime(time.time())} [SERVER - {SERVER}] STARTING UP ON PORT {PORT}")

# Gathers current weather information
def currentWeather(conn, addr, data, loc):
    msg_response = ""
    current = data['current']
    conditions = current['weather'][0]['description']
    temp = current['temp']
    feels_temp = current['feels_like']
    cloud_pct = current['clouds']
    msg_response = f"Current Conditions for {loc}:\n---Weather: {conditions}\n---Temperature: {temp}F\n---Feels Like: {feels_temp}F\n---Cloud Cover: {cloud_pct}%\n"
    conn.send(msg_response.encode(MSG_FMT))
    print(f"{time.ctime(time.time())} {addr} requested current weather for \"{loc}\".")

# Gathers the next 12 hours of weather information
def hourWeather(conn, addr, data, loc):
    msg_response = f"12 Hour Forecast for {loc}:\n"
    hourly = data['hourly'][0]
    conditions = hourly['weather'][0]['description']
    temp = hourly['temp']
    feels_temp = hourly['feels_like']
    cloud_pct = hourly['clouds']
    msg_response = msg_response + f"{dt.datetime.now().hour}:00: (Currently)\n---Weather: {conditions}\n---Temperature: {temp}F\n---Feels Like: {feels_temp}F\n---Cloud Cover: {cloud_pct}%\n"
    for i in range(12):
        hourly = data['hourly'][i+1]
        conditions = hourly['weather'][0]['description']
        temp = hourly['temp']
        feels_temp = hourly['feels_like']
        cloud_pct = hourly['clouds']
        msg_response = msg_response + f"\n{(dt.datetime.now().hour + i + 1) % 24}:00: (Hour {i+1})\n---Weather: {conditions}\n---Temperature: {temp}F\n---Feels Like: {feels_temp}F\n---Cloud Cover: {cloud_pct}%\n"

    conn.send(msg_response.encode(MSG_FMT))
    print(f"{time.ctime(time.time())} {addr} requested 12 hour forecast for \"{loc}\".")

# Gathers today's weather forecast
def todayWeather(conn, addr, data, loc):
    daily = data['daily'][0]
    conditions = daily['weather'][0]['description']
    max_temp = daily['temp']['max']
    min_temp = daily['temp']['min']
    precip = float(daily['pop']) * 100.0
    cloud_pct = daily['clouds']
    msg_response = f"Today's Forecast for {loc}:\n---Weather: {conditions}\n---Temperature: High - {max_temp}F, Low - {min_temp}F\n---Cloud Cover: {cloud_pct}%\n---Chance of Precipitation: {precip}%\n"
    conn.send(msg_response.encode(MSG_FMT))
    print(f"{time.ctime(time.time())} {addr} requested today's forecast for \"{loc}\".")

# Gathers tomorrow's weather forecast
def tomorrowWeather(conn, addr, data, loc):
    tmr = data['daily'][1]
    conditions = tmr['weather'][0]['description']
    max_temp = tmr['temp']['max']
    min_temp = tmr['temp']['min']
    precip = float(tmr['pop']) * 100.0
    cloud_pct = tmr['clouds']
    msg_response = f"Tomorrow's Forecast for {loc}:\n---Weather: {conditions}\n---Temperature: High - {max_temp}F, Low - {min_temp}F\n---Cloud Cover: {cloud_pct}%\n---Chance of Precipitation: {precip}%\n"
    conn.send(msg_response.encode(MSG_FMT))
    print(f"{time.ctime(time.time())} {addr} requested tomorrows's forecast for \"{loc}\".")

# Gathers 7-day forecast
def sevenDayWeather(conn, addr, data, loc):
    msg_response = f"7 Day Forecast for {loc}:\n"
    daily = data['daily'][0]
    conditions = daily['weather'][0]['description']
    max_temp = daily['temp']['max']
    min_temp = daily['temp']['min']
    precip = float(daily['pop']) * 100.0
    cloud_pct = daily['clouds']
    msg_response = msg_response + f"\n{WEEKDAYS[(dt.datetime.now().weekday()) % 7]}'s Forecast: (Today)\n---Weather: {conditions}\n---Temperature: High - {max_temp}F, Low - {min_temp}F\n---Cloud Cover: {cloud_pct}%\n---Chance of Precipitation: {precip}%\n"
    
    tmr = data['daily'][1]
    conditions = tmr['weather'][0]['description']
    max_temp = tmr['temp']['max']
    min_temp = tmr['temp']['min']
    precip = float(tmr['pop']) * 100.0
    cloud_pct = tmr['clouds']
    msg_response = msg_response + f"\n{WEEKDAYS[(dt.datetime.now().weekday() + 1) % 7]}'s Forecast: (Tomorrow)\n---Weather: {conditions}\n---Temperature: High - {max_temp}F, Low - {min_temp}F\n---Cloud Cover: {cloud_pct}%\n---Chance of Precipitation: {precip}%\n"
    for i in range(5):
        day = data['daily'][i+2]
        conditions = day['weather'][0]['description']
        max_temp = day['temp']['max']
        min_temp = day['temp']['min']
        precip = float(day['pop']) * 100.0
        cloud_pct = day['clouds']
        msg_response = msg_response + f"\n{WEEKDAYS[(dt.datetime.now().weekday() + i + 2) % 7]}'s Forecast:\n---Weather: {conditions}\n---Temperature: High - {max_temp}F, Low - {min_temp}F\n---Cloud Cover: {cloud_pct}%\n---Chance of Precipitation: {precip}%\n"


    conn.send(msg_response.encode(MSG_FMT))
    print(f"{time.ctime(time.time())} {addr} requested seven day forecast for \"{loc}\".")

# Gathers weather alert(s) information
def alertsWeather(conn, addr, data, loc):
    msg_response = ""
    try:
        for alert in data['alerts']:
            warning_type = alert['event']
            warning_desc = alert['description']
            msg_response = msg_response + f"Weather Alert(s) for {loc}:\n---{warning_type}: {warning_desc}\n"
    except:
        msg_response = f"No alerts for {loc}\n"
    conn.send(msg_response.encode(MSG_FMT))
    print(f"{time.ctime(time.time())} {addr} requested today's weather alert(s) for \"{loc}\".")

# Retrieves weather data by turning the location into coordinates to look up the weather information
def getWeather(loc):
    # Look up coordinates using given location
    try:
        location = geolocator.geocode(loc)
        lat = location.latitude
        lon = location.longitude
    except:
        return (-1) #invalid location
    # Retrieve json object for given coordinates
    try:
        weather_api_address = f"http://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=imperial&appid=c6bfff6ac43696f86f3da51a30f393f1&exclude=minutely"
        weather_data = requests.get(weather_api_address).json()
    except:
        return (-2) #trouble accessing url
    return weather_data

# receives client and handles each client's requests
def client_handler(connection, address):
    print(f"{time.ctime(time.time())} {address} connection started.")
    logging.info(f"{time.ctime(time.time())} [CLIENT - {address}] connection started.")
    client_alive = True
    while (client_alive):
        length = int(connection.recv(LENGTH).decode(MSG_FMT))
        message = connection.recv(length).decode(MSG_FMT)
        if (DIS_MSG == message):
            connection.send("Connection terminated.".encode(MSG_FMT))
            logging.info(f"{time.ctime(time.time())} [CLIENT - {address}] connection terminated.")
            client_alive = False
        else:
            command = message.split(' ')
            location = message[len(command[0])+1 : len(message)]
            weather_data = getWeather(location)
            if (len(command) == 1):
                msg_response = f"Missing element: {command[0]}\n---usage: {command[0]} <location>"
                connection.send(msg_response.encode(MSG_FMT))
                print(f"{time.ctime(time.time())} {address} misused \"{command[0]}\"")
            elif (weather_data == -1):
                connection.send("Invalid location. Please try again".encode(MSG_FMT))
            elif (weather_data == -2):
                connection.send("Error accessing weather data. Please try again".encode(MSG_FMT))
            else:
                logging.info(f"{time.ctime(time.time())} [CLIENT - {address}] command: {message}")
                if (command[0].lower() == COMMANDS[0]):
                    currentWeather(connection, address, weather_data, location)
                elif (command[0].lower() == COMMANDS[1]):
                    hourWeather(connection, address, weather_data, location)
                elif (command[0].lower() == COMMANDS[2]):
                    todayWeather(connection, address, weather_data, location)
                elif (command[0].lower() == COMMANDS[3]):
                    tomorrowWeather(connection, address, weather_data, location)
                elif (command[0].lower() == COMMANDS[4]):
                    sevenDayWeather(connection, address, weather_data, location)
                elif (command[0].lower() == COMMANDS[5]):
                    alertsWeather(connection, address, weather_data, location)

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
