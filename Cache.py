

import numpy as np
from math import log

from utils import getBinaryStringFromHexString


class Cache(object):
    def __init__(self, ram):
        """
        Cache Initialization.
        performs prompts to set cache variables, and initializes the Cache.Contents
        """
        valid_associativities = [1, 2, 4]
        valid_cacheSize = [8, 256]
        valid_replacementPolicies = [1, 2]
        valid_writeHitPolicies = [1, 2]
        valid_writeMissPolicies = [1, 2]

        # assume constant address width of 8
        self.ADDRESS_WIDTH = 8


        def isValidInputCacheSize(inputCacheSize):
            """Helper method to determine user input Cache Size"""
            return valid_cacheSize[0] <= inputCacheSize and inputCacheSize <= valid_cacheSize[1]
        
        def isValidBlockSizeSize(inputBlockSize):
            """Helper method to determine user input Block Size"""
            return valid_cacheSize[0] <= inputBlockSize and inputBlockSize <= valid_cacheSize[1]
        
        # ==============================================================
        # ========================= CACHE SETUP ========================
        # ==============================================================
        print("configure the cache:")

        # CACHE SIZE
        cacheSize = 0
        while not isValidInputCacheSize(cacheSize):
            cacheSize = int(input("cache size: "))
            if not isValidInputCacheSize(cacheSize):
                print(f"ERROR: invalid cache size. Must be in range {valid_cacheSize} (incl).")
        
        # BLOCK SIZE
        blockSize = 0
        while not isValidBlockSizeSize(blockSize):
            blockSize = int(input("block size: "))
            if not isValidBlockSizeSize(blockSize):
                print(f"ERROR: invalid block size. Must be in range {valid_cacheSize} (incl).")

        # ASSOCIATIVITY
        associativity = 0
        while associativity not in valid_associativities:
            associativity = int(input("associativity: "))
            if associativity not in valid_associativities:
                print(f"ERROR: invalid associativity. Must be in {valid_associativities}")
        
        # REPLACEMENT POLICY
        replacementPolicy = 0
        while replacementPolicy not in valid_replacementPolicies:
            replacementPolicy = int(input("replacement policy: "))
            if replacementPolicy not in valid_replacementPolicies:
                print(f"ERROR: invalid replacement policy. Must be in {valid_replacementPolicies}")
        
        # WRITE HIT POLICY
        writeHitPolicy = 0
        while writeHitPolicy not in valid_writeHitPolicies:
            writeHitPolicy = int(input("write hit policy: "))
            if writeHitPolicy not in valid_writeHitPolicies:
                print(f"ERROR: invalid write hit policy. Must be in {valid_writeHitPolicies}")
        
        # WRITE MISS POLICY
        writeMissPolicy = 0
        while writeMissPolicy not in valid_writeMissPolicies:
            writeMissPolicy = int(input("write miss policy: "))
            if writeMissPolicy not in valid_writeMissPolicies:
                print(f"ERROR: invalid write hit policy. Must be in {valid_writeMissPolicies}")
        
        # cache vars
        self.RAM = ram
        self.CacheHits = 0
        self.CacheMisses = 0

        self.ReplacementPolicy = replacementPolicy
        self.WriteHitPolicy = writeHitPolicy
        self.WriteMissPolicy = writeMissPolicy
        

        # CALCULATE CACHE PARAMS
        self.S = int(log(cacheSize, 2))                         # can assume will always be divisible
        self.s = int(log(self.S, 2))                            # can assume will always be divisible
        self.b = int(log(blockSize, 2))                         # can assume will always be divisible
        self.m = self.ADDRESS_WIDTH
        self.t = self.m - (self.S + self.b)
        self.C = cacheSize
        self.B = blockSize
        self.E = associativity

        self.Contents = self.getEmptyContents()
        
        print("cache successfully configured!")

        # for error checking
        # print(f"\ns:{self.s} b:{self.b} t:{self.t} m:{self.m}")
        # print(f"S:{self.S} C:{self.C} B:{self.B} E:{self.E}\n")

        print(f"contents:\n{self.Contents}")

        # prompt menu for operations like cache-read, memory-dump, etc...
        self.menu()


    def getEmptyContents(self):
        """
        returns a cleared Cache Contents Lists object with dims B x E x S
        """
        contents = [[[""] * (self.B + 4)] * self.E] * self.S
        for s in range(self.S):
            for e in range(self.E):
                for i in range(self.B + 4):     # add 4 for valid, dirty, replacement, tag+data...
                    # valid bit
                    if i == 0:
                        contents[s][e][i] = "0"
                    # dirty bit
                    elif i == 1:
                        contents[s][e][i] = "0"
                    # replacement policy
                    elif i == 2:
                        contents[s][e][i] = "0"
                    # tag policy
                    elif i == 3:
                        contents[s][e][i] = "00"
                    # data
                    else:
                        contents[s][e][i] = "00"
        return contents


    def menu(self):
        """
        This is like the game loop or whatever, but is not yet called.
        """
        command = ""
        while (command != "quit"):
            print("\n*** Cache simulator menu ***")
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
            
            # parse input into 'args'
            # if a command was correctly input, 
            #   use the next arguments to execute the method
            c = input("").split()
            command = c[0].strip()
            args = []
            for c in c[1:]:
                args.append(c.strip())
            
            # MENU COMMANDS
            if (command == "cache-read"):
                # pass in the hexadecimal cache read address string
                binaryCommandString = getBinaryStringFromHexString(args[0])
                self.cache_read(binaryCommandString)

            elif (command == "cache-write"):
                binaryCommandString = getBinaryStringFromHexString(args[0])
                hexDataToWriteStr = args[1]
                self.cache_write(binaryCommandString, hexDataToWriteStr)

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

            elif (command == "quit"):
                quit()

            else:
                print("Please type a command from the menu.")


    def tryGetCacheValue(self, setIndex, tag, offset):
        """
        Attempts to read the Contents
        if hit, return[0] = True, return[1] = 'value'
        else    return[0] = False, return[1] = '-1'
        """
        isHit = False
        value = "-1"

        block = self.Contents[setIndex]
        for line in block:
            if line[3] == tag:
                value = line[3][offset]
        
        if value != "":
            isHit = True
        
        return isHit, value


    def cache_write2(self, hexAddressStr, hexDataToWriteStr):
        binaryAddress = (bin(int(hexAddressStr[2:], 16))[2:].zfill(8)) # Converts address into binary address
        binaryOffset = binaryAddress[self.t + self.s:]
        tag = binaryAddress[:self.t]

        if self.cache_hit(hexAddressStr):
            self.CacheHits += 1
            print(f"hit:yes")
            print(f"eviction_policy:-1")
            print(f"ram_address:-1")
            print(f"data:{hexDataToWriteStr}")
            self.Contents[setIndex][d_e][int(binaryOffset, 2) + 4] = hexDataToWriteStr[2:]
            if self.write_hit_policy == 1:
                self.RAM[hexAddressStr] = hexDataToWriteStr[2:]
            else: 
                self.Contents[setIndex][d_e][1] = "1"
            print(f"dirty_bit:{self.Contents[setIndex][d_e][1]}")
        
        else: 
            self.CacheMisses += 1
            print("write_hit:no")
            if self.ReplacementPolicy == "1":
                count = 0
                for i in range(self.E):
                    if self.Contents[cacheSetIndex][i][0] == "1": # check to see if lines are valid
                        count += 1
                if count != 4: # if all lines aren't valid, we remove those lines
                    while True:
                        eviction_line = np.random.randint(1, self.E)
                        if (self.Contents[cacheSetIndex][eviction_line-1][0] == "0"):
                            break
                else:
                    eviction_line = np.random.randint(1, self.E)
            else:  # least recently used
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
            
            if self.write_miss_policy == "1":
                print(f"eviction_line:{eviction_line}")
                self.Contents[setIndex][eviction_line - 1][0] = "1" # Setting Valid bit to 1
                if tag != "":
                    self.Contents[setIndex][eviction_line - 1][3] = str(hex(int(tag, 2)))[2:].zfill(2).upper()
                for b in range(4, B + 4):
                    self.Contents[setIndex][eviction_line - 1][b] = self.RAM["0x" + (hex((int(address[2:], 16) - int(binaryOffset, 2))+(b-4))[2:].zfill(2)).upper()]
                self.Contents[setIndex][eviction_line - 1][int(binaryOffset, 2) + 4] = dataToWrite[2:]
                if self.write_hit_policy == "1":
                    self.RAM[address] = dataToWrite[2:]
                else:
                    self.Contents[setIndex][eviction_line - 1][1] = 1
                print(f"ram_address:{address}")
                print(f"data:0x"+ self.RAM[address])
                print(f"dirty_bit:{self.Contents[setIndex][eviction_line - 1][1]}")
            else:
                print(f"eviction_line:{eviction_line}")
                print(f"ram_address:{address}")
                print(f"data:0x"+ self.RAM[address])
                print(f"dirty_bit:0")
                self.RAM[address] = data[2:]
    
    
    def cache_read(self, binaryCommandString):
        """
        Determines if the binaryCommandString results in a hit or miss in the cache
        
        Displays intermediate info such as set and tag numbers
        """
        # offset will always be present
        readOffset = int(binaryCommandString[-self.b:], 2)

        # check set associativity
        readSet = int(binaryCommandString[self.t:-self.b], 2)
        if readSet == "":
            readSet = 0

        # check if tag present
        readTagString = binaryCommandString[0:self.t]
        isHit = False
        value = "-1"
        if readTagString != "":
            isHit, value = self.tryGetCacheValue(readSet, readTagString, readOffset)
        else:
            readTagString = "0"

        print(f"set:{readSet}")
        print(f"tag:{readTagString}")
        if isHit:
            self.CacheHits += 1
            print(f"hit:yes")
            print(f"eviction_policy:-1")
            print(f"ram_address:-1")
            print(f"data:{value}")
        
        # MISS
        else:
            self.CacheMisses += 1
            print(f"hit:no")

            # REPLACEMENT POLICY
            evictionLine = -1
            # random
            if self.ReplacementPolicy == 1:
                # check if all lines in set are valid
                validCheck = [True, 0]
                for i, line in enumerate(self.Contents[readSet]):
                    if line[0] != "1":
                        validCheck[0] = False
                        validCheck[1] = i
                
                if not validCheck[0]:
                    # pick the first invalid line
                    evictionLine = validCheck[1]
                
                else:
                    # pick a random eviction line
                    evictionLine = np.random.randint(0, self.E)
            
            # least frequently used
            # TODO
            elif self.ReplacementPolicy == 2:
                if self.E == 1:
                    evictionLine = 1
                elif self.E == 2:
                    evictionLine = 2
                else:
                    pass
            
            # least recently used
            # TODO
            elif self.ReplacementPolicy == 3:
                pass

            
            # fetch the requested address value from RAM
            ramAddress = hex(int(binaryCommandString, 2))
            ramIndex = int(ramAddress, 16) // self.ADDRESS_WIDTH    # can expect this to always be whole integer regardless
            value = self.RAM[ramIndex]
            
            print(f"eviction_line:{evictionLine}")            
            print(f"ram_address:{ramAddress}")            
            print(f"data:{value}")


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
        # does NOT reset hits/missed
        # resets all replacement policies to "1"
        self.Contents = self.getEmptyContents()
        print("cache_cleared")
    

    def cache_view(self):
        """
        Shows the cache setup params and current contents
        """
        # REPLACEMENT POLICY
        if self.ReplacementPolicy == 1:
            replacementString = "random_replacement"
        elif self.ReplacementPolicy == 2:
            replacementString = "least_recently_used"
        elif self.ReplacementPolicy == 3:
            replacementString = "least_frequently_used"
        else:
            replacementString = "NONE SET"
        
        # WRITE HIT POLICY
        if self.WriteHitPolicy == 1:
            writeHitString = "write_though"
        else:
            writeHitString = "write_back"

        # WRITE MISS POLICY
        if self.WriteMissPolicy == 1:
            writeMissString = "write_allocate"
        else:
            writeMissString = "no_write_allocate"
        
        # PRINT CACHE INFO
        print(f"cache_size:{self.C}")
        print(f"data_block_size:{self.B}")
        print(f"associativity:{self.E}")
        print(f"replacement_policy:{replacementString}")
        print(f"write_hit_policy:{writeHitString}")
        print(f"write_miss_policy:{writeMissString}")
        print(f"number_of_cache_hits:{self.CacheHits}")
        print(f"number_of_cache_misses:{self.CacheMisses}")
        
        # PRINT CACHE CONTENT (skips replacemenrPolicy[2] tag[3])
        print("cache_content:")
        
        for s in range(self.S):
            for e in range(self.E):
                for i in range(self.B + 4):
                    if i != 2 or i != 3:
                        print(self.Contents[s][e][i], end=" ")
                print()
                

    def cache_dump(self):
        """
        Write the cache DATA to file cache.txt
        sep=" "
        newline='\n'
        """
        with open("cache.txt", 'a') as cacheFile:
            for s in range(self.S):
                for e in range(self.E):
                    for i in range(4, self.B):
                        cacheFile.write(self.Contents[s][e][i] + " ")
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
