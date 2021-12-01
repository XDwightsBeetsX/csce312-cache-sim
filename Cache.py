
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
        self.CacheHits = 0
        self.CacheMisses = 0
        # TODO find m and t
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
            
            # read input
            # if a command was correctly input, 
            #   use the next arguments to execute the method
            c = input("").split()
            command = c[0].strip()
            args = []
            for c in c[1:]:
                args.append(c.strip())
            
            if (command == "cache-read"):
                binaryCommand = bin(args[0]).replace('0b', '')
                self.cache_read(binaryCommand)
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


    def cache_read(self, binaryCommandStr):
        """
        Determines if the binaryCommandStr results in a hit or miss in the cache
        
        Displays intermediate info such as set and tag numbers
        """
        readTag = int(binaryCommandStr[0:self.t])
        readSet = int(binaryCommandStr[self.t:-self.b])
        readOffset = int(binaryCommandStr[-self.b:])

        value = '-1'  # see TODO below
        isHit = False
        try:
            # see if cache hit
            # searching Contents will throw error if indexing is wrong
            value = self.Contents[readSet][readTag][readOffset]
            isHit = True
            self.CacheHits += 1
        except Exception:
            # cache miss
            self.CacheMisses += 1

        print(f"set:{readSet}")
        print(f"tag:{readTag}")
        if isHit:
            print(f"hit:yes")
            print(f"eviction_policy:-1")
            print(f"ram_address:-1")
            print(f"data:{value}")
        else:
            print(f"hit:no")
            print(f"eviction_line:{self.ReplacementPolicy}")
            print(f"ram_address:{hex(int(binaryCommandStr))}")
            # TODO: idk what we put in for data if theres a cache miss
            print(f"data:")


    def cache_write(self):
        pass

    
    def cache_flush(self):
        """
        clears the cache contents, replacing all data with '0's
        """
        self.Contents = [[[0] * self.B] * self.E] * self.S
        print("cache_cleared")
    

    def cache_view(self):
        print(f"cache_size:{self.C}")
        print(f"data_block_size:{self.B}")
        print(f"associativity:{self.E}")
        print(f"replacement_policy:{self.ReplacementPolicy}")
        print(f"write_hit_policy:{self.WriteHitPolicy}")
        print(f"write_miss_policy:{self.WriteMissPolicy}")
        print(f"number_of_cache_hits:{self.CacheHits}")
        print(f"number_of_cache_misses:{self.CacheMisses}")
        
        print("cache_content:")
        for s in len(self.Contents):
            for line in self.Contents[s]:
                # TODO idk how we add valid/dirty bits
                # print(validBit, dirtyBit, line, end=" ")
                pass
            print()

    
    def cache_dump(self):
        with open("cache.txt", 'a') as cacheFile:
            for set in range(self.S):
                for line in range(self.E):
                    for i in range(self.B):
                        # not sure how indexing past the valid and tag parts goes...
                        cacheFile.write(self.Contents[set][line][1+self.t+i] + " ")
                cacheFile.write('\n')

    
    def memory_view(self):
        """
        Displays the RAM content and status
        """
        print(f"memory_size:{len(self.RAM)}")
        
        print("memory_content:")
        print("address:data")
        
        # TODO this is just a quick thing from the sample view
        # im not sure ab the rowLength
        start = 0x00
        rowLength = 8
        for r in range(len(self.RAM)):
            print(f"{start}:", end="")
            for i in range(rowLength):
                print(self.RAM[r*rowLength + i], end=" ")
            
            start += hex(rowLength)
            print()


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
