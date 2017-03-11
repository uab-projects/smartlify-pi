import binascii


def bytes_to_hex(b):
    return str(binascii.hexlify(b))[2:-1]


if __name__ == "__main__":
    print("hexa string: %s" % bytes_to_hex(bytes().fromhex("aabb")))
