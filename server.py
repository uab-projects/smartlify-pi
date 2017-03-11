# Libraries
import sys
from socket import *
import netifaces as ni
import struct

# Constants
if len(sys.argv) == 1:
    INTERFACE_DRON = "wlan0"
else:
    INTERFACE_DRON = sys.argv[1]
SERVER_PORT = 7000

# Welcome
print("Welcome to Raspberry WiFi notifier for drones [SERVER]")
print("Interface for drone is %s" % (INTERFACE_DRON))

# Get IP
interface_dron_addrs = ni.ifaddresses(INTERFACE_DRON)
interface_dron_ip = interface_dron_addrs[2][0]['addr']
print("Address in the drone interface: %s" % interface_dron_ip)

# Set server
print("Creating socket")
s = socket(AF_INET, SOCK_STREAM)
print("Binding socket")
s.bind((interface_dron_ip, SERVER_PORT))
closed_con = False
# Listen for connections
try:
    print("Listenining")
    s.listen(1)
    print("Waiting for connections")
    conn, addr = s.accept()
    print("Device connected", addr)
    while not closed_con:
        print("Waiting for opcode")
        opcode = conn.recv(1)
        opcode_hex = opcode.hex()
        print("Received opcode: %s", opcode_hex)
        if opcode_hex == "00":
            reply = struct.pack("Q", 1000)
            conn.sendall(reply)
        elif opcode_hex == "ff":
            conn.close()
            closed_con = True
finally:
    if not closed_con:
        conn.close()
