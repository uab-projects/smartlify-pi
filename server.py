# Libraries
import sys
from socket import *
import netifaces as ni
import struct
from helpers import bytes_to_hex

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
# Listen for connections
while True:
    try:
        closed_con = False
        print("Listenining")
        s.listen(1)
        print("Waiting for connections")
        conn, addr = s.accept()
        print("Device connected", addr)
        while not closed_con:
            print("Waiting for opcode")
            opcode = conn.recv(1)
            opcode_hex = bytes_to_hex(opcode)
            print("Received opcode: %s" % opcode_hex)
            if opcode_hex == "00":
                print("OPCODE is WIFI REQ")
                reply = struct.pack("Q", 1000)
                print("Sending reply")
                conn.sendall(reply)
            elif opcode_hex == "ff" or opcode_hex == "":
                if opcode == "":
                    print("No more data")
                else:
                    print("OPCODE is close")
                conn.close()
                closed_con = True
                print("Closed connection")
    except Exception as e:
        print("Exception occurred %s" % str(e))
    finally:
        if not closed_con:
            print("Client exited before expected")
            conn.close()
            closed_con = True
            print("Closed connection")
