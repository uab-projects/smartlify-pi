"""
Basic client to query in Python a raspberry to communicate its neighbor
networks.

Usage:
    python -m client [HOST]

Connects to the HOST and performs all available client operations several times
"""
# Libraries
import sys
from socket import *
import netifaces as ni
import struct
from common import PORT, OP_WIFI_REQ, OP_CLOSE

# Constants
HOST = "192.168.2.200" if len(sys.argv) <= 1 else sys.argv[1]
"""
    str: ip of the Raspberry server to connect
"""
TESTS_NUMBER = 1 if len(sys.argv) <= 2 else int(sys.argv[2])
"""
    int: number of tests to perform
"""

# Welcome
print("Welcome to Raspberry WiFi notifier for drones [CLIENT]")
print("IP Address of the raspberry server to query: %s" % (HOST))

# Set client
for i in range(TESTS_NUMBER):
    if(TESTS_NUMBER > 1):
        print("CONNECTION TEST [%02d]" % (i, HOST))
        print("================================================")
    print(" 01. Creating socket")
    s = socket(AF_INET, SOCK_STREAM)
    print(" 02. Connecting socket")
    s.connect((HOST, PORT))
    # Socket connected
    print(" 03. Connected to socket")
    print(" 04. Testing features")
    print("     -> Testing OP_WIFI_REQ")
    # Ask for networks
    s.send(OP_WIFI_REQ)
    print("     --> Sent opcode")
    print("     --> Waiting for size response")
    size_response = s.recv(8)
    size_json = struct.unpack("Q", size_response)[0]
    print("     --> Response size is %d bytes" % size_json)
    print("     --> Receiving networks in JSON format")
    json = s.recv(size_json)
    print("     --> Received JSON is")
    print(json)
    print("     --> Feature tested")
    # Close connection
    print("     -> Testing OP_CLOSE")
    s.send(OP_CLOSE)
    print("     --> Sent close opcode")
    s.close()
    print(" 05. Closed communications")
