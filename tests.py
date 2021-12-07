
from utils import getBinaryStringFromHexString


if __name__ == "__main__":
    print("===========================================")
    print("=============== Conversions ===============")
    print("===========================================")
    h1 = "0x00"
    print(f"{h1} -> {getBinaryStringFromHexString(h1)}")
    h2 = "0xFF"
    print(f"{h2} -> {getBinaryStringFromHexString(h2)}")
    h3 = "0x18"
    print(f"{h3} -> {getBinaryStringFromHexString(h3)}")
