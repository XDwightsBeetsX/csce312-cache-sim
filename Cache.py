
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
        
        # TODO find m and t
        m = len(ram)
        self.m = 8
        self.t = m - (s + b)

        self.CacheHits = 0
        self.CacheMisses = 0

        self.Contents = self.getEmptyContents()

        print("cache successfully configured!")
    

    def getEmptyContents(self):
        c = [[[0] * self.B] * self.E] * self.S
        print(c)
        for s in range(self.S):             # Not totally sure if this is correct. But it is how I understood it
            for e in range(self.E):
                for i in range(self.B):
                    if i == 0:
                        c[s][e][i] = "0"    # This is the Valid bit
                    elif i == 1:
                        c[s][e][i] = "0"    # This is the Dirty Bit
                    elif i == 2:
                        c[s][e][i] = "0"    # This is the LRU/LFU bit
                        # TODO issues w/ rep policy here?
                        # 1 -> Random Replacement
                        # 2 -> Least Recently Used
                    else:
                        c[s][e][i] = "00" # Tag and Data Amount (hex)
        return c


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
                binaryCommand = bin(args[0]).replace('0b', '')
                dataToWrite = args[1]
                self.cache_write(binaryCommand, dataToWrite)
            elif (command == "cache-flush"):
                self.cache_flush()
            elif (command == "cache-view"):
                self.cache_view()
            elif (command == "memory-view"):
                self.memory_view()
            elif (command == "cache-dump"):
                self.cache_dump()
            elif (command == "memory-dump"):
                self.memory_dump()
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
            
            ramAddy = hex(int(binaryCommandStr))
            print(f"ram_address:{ramAddy}")
            
            ramIndex = int(ramAddy) / 8
            ramData = self.RAM[ramIndex]
            print(f"data:{ramData}")


    def cache_write(self, binaryCommand, dataToWrite):
        # binaryCommand is BITS: [tag, set, offset]
        cacheTag = binaryCommand[4:self.t]
        cacheSetIndex = binaryCommand[4+self.t:4+self.t+self.s]
        
        isHit = False
        dirtyBit = 1
        for line in self.Contents[cacheSetIndex]:
            if line[4:self.t] == str(hex(int(cacheTag))):
                foundLine = line[4:self.t]
                if foundLine[0] == 1:               # valid bit check
                    isHit = True
                    dirtyBit = foundLine[1]

                    # check the WriteHitPolicy to see if data gets written
                    if self.WriteHitPolicy == 1:
                        foundLine[4:] = dataToWrite
                    else:
                        foundLine[1] = 1            # set dirty bit to 1
                else:
                    # ==========================
                    # TODO
                    # ==========================
                    if self.WriteHitPolicy == 1:    # random
                        count = 0
                        for i in range(self.E):
                            if self.Contents[cacheSetIndex][i][0] == "1": # check to see if lines are valid
                                count += 1
                            if count != 4: # if all lines aren't valid, we remove those lines
                                while True:
                                    eviction_line = random.randint(1, E)
                                    if (self.Contents[cacheSetIndex][eviction_line-1][0] == "0"):
                                        break
                            else:
                                eviction_line = random.randint(1, E) # else if all lines are valid, we remove one at random
                    elif self.WriteHitPolicy == 2:  # least recently used
                        if self.E == "1":
                            eviction_line = 1
                        elif self.E == "2":
                            if self.Contents[cacheSetIndex][0][2] == "0": # TODO String or Int compare?
                                eviction_line = 1
                                self.Contents[cacheSetIndex][0][2] = "1"
                            else: 
                                eviction_line = 2
                                self.Contents[cacheSetIndex][0][2] = "0"
                        else: # Goes through checking which bit is LFU and sets the eviction line accordingly
                            if self.Contents[cacheSetIndex][0][2] == "0":
                                eviction_line = 1
                                self.Contents[cacheSetIndex][0][2] = "1"
                                self.Contents[cacheSetIndex][1][2] = "0"
                            elif self.Contents[cacheSetIndex][1][2] == "0":
                                eviction_line = 2
                                self.Contents[cacheSetIndex][1][2] = "1"
                                self.Contents[cacheSetIndex][2][2] = "0"
                            elif self.Contents[cacheSetIndex][2][2] == "0":
                                eviction_line = 3
                                self.Contents[cacheSetIndex][2][2] = "1"
                                self.Contents[cacheSetIndex][3][2] = "0"
                            else: 
                                eviction_line = 4
                                self.Contents[cacheSetIndex][3][2] = "1"
                                self.Contents[cacheSetIndex][0][2] = "0"
                    else:
                        pass  
                        
        
        print(f"set:{cacheSetIndex}")
        print(f"tag:{cacheTag}")

        if isHit:
            self.CacheHits += 1
            print("write_hit:yes")
            print("eviction_line:-1")
            print("ram_address:-1")

        else:
            self.CacheMisses += 1
            print("write_hit:no")
            print(f"eviction_line:{evictionLine}")
            print(f"ram_address:{str(hex(binaryCommand))}")
        
        print(f"data:{dataToWrite}")
        print(f"dirty_bit:{dirtyBit}")

    
    def cache_flush(self):
        """
        clears the cache contents, replacing all data with '0's
        """
        self.Contents = self.getEmptyContents()
        print("cache_cleared")
    

    def cache_view(self):
        if self.ReplacementPolicy == 1:
            replacementString = "random_replacement"
        else:
            replacementString = "least_recently_used"
        if self.WriteHitPolicy == 1:
            writeHitString = "write_though"
        else:
            writeHitString = "write_back"
        if self.WriteMissPolicy == 1:
            writeMissString = "write_allocate"
        else:
            writeMissString = "no_write_allocate"
        print(f"cache_size:{self.C}")
        print(f"data_block_size:{self.B}")
        print(f"associativity:{self.E}")
        print(f"replacement_policy:{replacementString}")
        print(f"write_hit_policy:{writeHitString}")
        print(f"write_miss_policy:{writeMissString}")
        print(f"number_of_cache_hits:{self.CacheHits}")
        print(f"number_of_cache_misses:{self.CacheMisses}")
        
        print("cache_content:")
        
        # similar to getEmptyContents
        for i in range(self.S):
            for f in range(self.E):
                for g in range(self.B + 4):
                    if g != 2: # We need this to skip the LFU index bc we don't print it
                        print(self.Contents[i][f][g], end=" ")
                print()
                

    def cache_dump(self):
        with open("cache.txt", 'a') as cacheFile:
            for set in range(self.S):
                for line in range(self.E):
                    for i in range(self.B + 4):
                        # not sure how indexing past the valid and tag parts goes...
                        cacheFile.write(self.Contents[set][line][i + 4] + " ")
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
