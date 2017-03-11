# Libraries
import sys
from socket import *
import netifaces as ni
import struct

# Constants
if len(sys.argv) <= 1:
    INTERFACE_DRON = "wlan0"
else:
    INTERFACE_DRON = sys.argv[1]
if len(sys.argv) <= 2:
    IP_SERVER = "192.168.2.200"
else:
    IP_SERVER = sys.argv[2]
SERVER_PORT = 7000

# Welcome
print("Welcome to Raspberry WiFi notifier for drones [CLIENT]")
print("Interface for drone is %s" % (INTERFACE_DRON))

# Set client
print("Creating socket")
s = socket(AF_INET, SOCK_STREAM)
print("Connecting socket")
s.connect((IP_SERVER, SERVER_PORT))
# Socket connected
print("Connected to socket, sending request for wifis")
# Ask for something
s.send(bytes().fromhex("00"))
# Wait response size
print("Waiting for size response")
size_response = s.recv(8)
size_json = struct.unpack("Q", size_response)[0]
print("I'll receive a JSON of size %d" % size_json)
# Close connection
s.send(bytes().fromhex("ff"))
s.close()
