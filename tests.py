
from Cache import Cache

if __name__ == "__main__":

    ram = ["00", "FF", "10"]
    
    C = Cache(ram)

    print("S, C, B, E")
    print(C.S, C.C, C.B, C.E)

    print("s, b, t")
    print(C.s, C.b, C.t)
