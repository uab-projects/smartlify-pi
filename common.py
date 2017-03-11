"""
Defines common constants
"""
# Connection
PORT = 3000

# Opcodes
OP_WIFI_REQ = bytes().fromhex("00")
"""
    bytes: opcode to request wifi networks
"""
OP_CLOSE = bytes().fromhex("ff")
"""
    bytes: opcode to close the connection to server
"""
