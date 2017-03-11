"""
Basic server that will run in a Raspberry Pi that will allow to communicate
information to a remote host (in this case an Android application)

Usage:
    python -m server <BIND_INTERFACE>

Runs a multithreaded server that will listen for TCP clients and serve them
in parallel using multiple threads and following the established protocol
"""
# Libraries
import sys
from socket import *
import netifaces as ni
import struct
from common import OP_CLOSE, OP_WIFI_REQ, PORT
from helpers import bytes_to_hex
from wmod import scanwifi
import multiprocessing

# Constants
INTERFACE_DRONE = "wlan0" if len(sys.argv) <= 1 else sys.argv[1]
"""
    str: interface to bind the server to
"""
INTERFACE_SCAN = "wlan1"
"""
    str: interface to use to look for wifi networks
"""
LOG_FILE = open("/home/pi/Documents/uCode/hiberus/log.txt", "a")
"""
    file: file to append logs to
"""


# Methods
def log(msg):
    """
    Logs the given message, depending on the implementation will log to the
    console or to a file, etc...
    """
    LOG_FILE.write(msg + "\n")
    LOG_FILE.flush()


# Welcome
log("Welcome to Raspberry WiFi notifier for drones [SERVER]")
log("Interface for drone is %s" % (INTERFACE_DRONE))

# Get IP to bind
interface_dron_addrs = ni.ifaddresses(INTERFACE_DRONE)
interface_dron_ip = interface_dron_addrs[2][0]['addr']
log("Address in the drone interface: %s" % interface_dron_ip)

# Set server
log("Creating socket")
s = socket(AF_INET, SOCK_STREAM)
log("Binding socket")
s.bind((interface_dron_ip, PORT))


def handle_connection(conn, endpoint):
    """
    Given a connection identified by the connection object and endpoint tuple
    (IP and port), handles the connection according to the protocol until a
    close command is received or the communication is closed
    """
    closed_con = False
    endpoint_str = str(endpoint)
    log(endpoint_str)
    try:
        log("Device connected %s" % endpoint_str)
        while not closed_con:
            # Receive opcode
            log("[%s] Waiting for opcode" % endpoint_str)
            opcode = conn.recv(1)
            log("[%s] Received opcode: %s" % (endpoint_str,
                bytes_to_hex(opcode)))
            # Switch opcode
            if opcode == OP_WIFI_REQ:
                # Serve wifi networks
                log("[%s] OPCODE is WIFI REQ" % endpoint_str)
                wif = scanwifi(INTERFACE_SCAN)
                reply = struct.pack("Q"+str(len(wif))+"s", len(wif), wif)
                log("[%s] Sending reply" % endpoint_str)
                conn.sendall(reply)
            elif opcode == OP_CLOSE or opcode == bytes():
                # Close connection
                if opcode == "":
                    log("[%s] No more data" % endpoint_str)
                else:
                    log("[%s] OPCODE is close" % endpoint_str)
                conn.close()
                closed_con = True
                log("[%s] Closed connection" % endpoint_str)
    except Exception as e:
        log("[%s] Exception occurred %s" % (endpoint_str, str(e)))
    finally:
        # Close if exception occurs
        if not closed_con:
            log("[%s] Client exited before expected" % endpoint_str)
            conn.close()
            closed_con = True
            log("[%s] Closed connection" % endpoint_str)
    return endpoint_str


def connection_handled_ok(res):
    """
    Callback to execute when a connection has been handled succesfully
    """
    log("Connection was handled properly: %s" % str(res))


def connection_handled_fail(exc):
    """
    Callback to execute when a connection has been handled with an error
    """
    log("Connection was unable to be handled: %s" % str(exc))


# Listen for connections
log("Creating thread pool")
pool = multiprocessing.Pool()
while True:
    log("Listening")
    s.listen(0)
    log("Waiting for connections")
    pool.apply_async(handle_connection,  s.accept(), {}, connection_handled_ok,
                     connection_handled_fail)
# Close log file
LOG_FILE.close()
