


def getBinaryStringFromHexString(hexString, stringWidth=8):
    """
    returns the string representation of a hexadecimal number in binary
    """
    return str(bin(int(hexString, 16))).split("0b")[1].zfill(stringWidth)

