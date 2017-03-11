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
f = open("/home/pi/Documents/uCode/hiberus/log.txt", "a")
f.write("Welcome to Raspberry WiFi notifier for drones [SERVER] \n")
f.flush()
f.flush()
f.write("Interface for drone is %s \n" % (INTERFACE_DRON))
f.flush()

# Get IP
interface_dron_addrs = ni.ifaddresses(INTERFACE_DRON)
interface_dron_ip = interface_dron_addrs[2][0]['addr']
f.write("Address in the drone interface: %s \n" % interface_dron_ip)
f.flush()

# Set server
f.write("Creating socket \n")
f.flush()
s = socket(AF_INET, SOCK_STREAM)
f.write("Binding socket \n")
f.flush()
s.bind((interface_dron_ip, SERVER_PORT))


def handle_connection(conn, addr):
    closed_con = False
    addr_str = str(addr)
    f.write(addr_str)
    f.flush()
    try:
        f.write("Device connected \n", addr_str)
        f.flush()
        while not closed_con:
            f.write("[%s] Waiting for opcode \n" % addr_str)
            f.flush()
            opcode = conn.recv(1)
            opcode_hex = bytes_to_hex(opcode)
            f.write("[%s] Received opcode: %s \n" % (addr_str, opcode_hex))
            f.flush()
            if opcode_hex == "00":
                f.write("[%s] OPCODE is WIFI REQ \n" % addr_str)
                f.flush()
                wif = scanwifi("wlan1")
                reply = struct.pack("Q"+str(len(wif))+"s", len(wif), wif)
                f.write("[%s] Sending reply \n" % addr_str)
                f.flush()
                conn.sendall(reply)
            elif opcode_hex == "ff" or opcode_hex == "":
                if opcode == "":
                    f.write("[%s] No more data \n" % addr_str)
                    f.flush()
                else:
                    f.write("[%s] OPCODE is close \n" % addr_str)
                    f.flush()
                conn.close()
                closed_con = True
                f.write("[%s] Closed connection \n" % addr_str)
                f.flush()
    except Exception as e:
        f.write("[%s] Exception occurred %s \n" % (addr_str, str(e)))
        f.flush()
    finally:
        if not closed_con:
            f.write("[%s] Client exited before expected \n" % addr_str)
            f.flush()
            conn.close()
            closed_con = True
            f.write("[%s] Closed connection \n" % addr_str)
            f.flush()


def connection_handled_ok(res):
    f.write("connection was handled properly \n")
    f.flush()


def connection_handled_fail(exc):
    f.write("connection was unable to be handled \n")
    f.flush()


# Listen for connections
f.write("Creating thread pool \n")
f.flush()
pool = multiprocessing.Pool()
while True:
    f.write("Listening")
    f.flush()
    s.listen(1)
    f.write("Waiting for connections \n")
    f.flush()
    pool.apply_async(handle_connection,  s.accept(), {}, connection_handled_ok,
                     connection_handled_fail)
f.close()
