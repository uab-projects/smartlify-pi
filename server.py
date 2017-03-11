# Libraries
import sys
from socket import *
import netifaces as ni
import struct
from helpers import bytes_to_hex
from wmod import scanwifi
import multiprocessing

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


def handle_connection(conn, addr):
    closed_con = False
    addr_str = str(addr)
    print(addr_str)
    try:
        print("Device connected", addr_str)
        while not closed_con:
            print("[%s] Waiting for opcode" % addr_str)
            opcode = conn.recv(1)
            opcode_hex = bytes_to_hex(opcode)
            print("[%s] Received opcode: %s" % (addr_str, opcode_hex))
            if opcode_hex == "00":
                print("[%s] OPCODE is WIFI REQ" % addr_str)
                wif = scanwifi()
                reply = struct.pack("Q"+str(len(wif))+"s", len(wif), wif)
                print("[%s] Sending reply" % addr_str)
                conn.sendall(reply)
            elif opcode_hex == "ff" or opcode_hex == "":
                if opcode == "":
                    print("[%s] No more data" % addr_str)
                else:
                    print("[%s] OPCODE is close" % addr_str)
                conn.close()
                closed_con = True
                print("[%s] Closed connection" % addr_str)
    except Exception as e:
        print("[%s] Exception occurred %s" % (addr_str, str(e)))
    finally:
        if not closed_con:
            print("[%s] Client exited before expected" % addr_str)
            conn.close()
            closed_con = True
            print("[%s] Closed connection" % addr_str)


def connection_handled_ok(res):
    print("connection was handled properly")


def connection_handled_fail(exc):
    print("connection was unable to be handled")


# Listen for connections
print("Creating thread pool")
pool = multiprocessing.Pool()
while True:
    print("Listening")
    s.listen(1)
    print("Waiting for connections")
    pool.apply_async(handle_connection,  s.accept(), {}, connection_handled_ok,
                     connection_handled_fail)
