
from math import log


class Cache(object):
    def __init__(self, ram):
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

        self.RAM = ram
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
    

    def menu(self):
        """
        This is like the game loop or whatever, but is not yet called.
        """
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
        quit()


    def cache_read(self):
        pass


    def cache_write(self):
        pass

    
    def cache_flush(self):
        """
        clears the cache contents, replacing all data with '0's
        """
        self.Contents = [[[0] * self.B] * self.E] * self.S
    

    def cache_view(self):
        pass

    
    def cache_dump(self):
        pass


    def memory_dump(self):
        """
        writes the current RAM data to the file 'ram.txt'
        """
        # will create or overrite the 'ram.txt' file
        with open("ram.txt", 'a') as ramWrite:
            for i, r in enumerate(self.RAM):
                # cast numbers to strings and write
                ramWrite.write(f"{str(r)}")
                
                # no newline at end of file
                if i < len(self.RAM):
                    ramWrite.write('\n')
