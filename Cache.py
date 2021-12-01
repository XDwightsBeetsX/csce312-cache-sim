
from math import log


class Cache(object):
    def __init__(self):
        print("configure the cache:")
        cacheSize = int(input("cache size: "))
        blockSize = int(input("data block size: "))
        associativity = int(input("associativity: "))
        replacementPolicy = int(input("replacement policy: "))
        writeHitPolicy = int(input("write hit policy: "))
        writeMissPolicy = int(input("write miss policy: "))
        
        S = int(cacheSize / (blockSize * associativity))
        s = int(log(cacheSize, 2))
        b = int(log(blockSize, 2))

        self.ReplacementPolicy = replacementPolicy
        self.WriteHitPolicy = writeHitPolicy
        self.WriteMissPolicy = writeMissPolicy
        self.S = S
        self.C = cacheSize
        self.B = blockSize
        self.E = associativity
        self.s = s
        self.b = b
        # TODO find m
        # self.t = m - (s + b)

        # TODO is this how to initialize Contents?
        self.Contents = [[[]]]  # updated below
        print("cache successfully configured!")

    
    def cache_flush(self):
        self.Contents = [[[0] * self.B] * self.E] * self.S
        print(self.Contents)
    

    def menu(self):
        command = ""
        while (command != "quit"):
            print("*** Cache simulator menu ***")
            print("type one command: ")
            print("1. cache-read")
            print("2. cache-write")
            print("3. cache-flush")
            print("4. cache-view")
            print("5. memory-view")
            print("6. cache-dump")
            print("7. memory-dump")
            print("8. quit")
            print("****************************")
            
            command = input("").strip()
            if (command == "cache-read"):
                pass
            elif (command == "cache-write"):
                pass
            elif (command == "cache-flush"):
                self.cache_flush()
            elif (command == "cache-view"):
                pass
            elif (command == "memory-view"):
                pass
            elif (command == "cache-dump"):
                pass
            elif (command == "memory-dump"):
                pass
            else:
                print("Please type a command from the menu.")
