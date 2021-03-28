Name: Benjamin Petrick
Date: 3/28/2021
Assignment: Networking Project - Client Server Socket Programming

server.py
- runs the server
- server is attached to loopback address (127.0.0.1)
- server sends logging of starting up, client connections starting and ending, and client commands to server_logging.log
- supports multiple clients
- uses sys_defaults.ini to gather server and command info

client.py
- runs the client
- runs off of device IP address
- connects to server socket
- uses sys_defaults.ini to gather server and command info

sys_defaults.ini
- holds the server IP address and port number
- also holds available commands and command definitions

server_logging.log
- holds the previous server startups, client connections, and client commands

README.txt (this document)
- provides extra explanation

Notes: 
- I am running my server on the loopback address, and I am running my client on my device IP address. The professor said this
would count as 2 different IP addresses
