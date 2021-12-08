

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
        self.S = int(cacheSize / (blockSize * associativity))   # can assume divisible
        self.s = int(log(self.S, 2))
        self.b = int(log(blockSize, 2))
        self.m = self.ADDRESS_WIDTH
        self.t = self.m - (self.s + self.b)
        self.C = cacheSize
        self.B = blockSize
        self.E = associativity

        # set the Cache contents to be initially 0s
        self.Contents = self.getEmptyContents()
        print("cache successfully configured!")

        # prompt menu for operations like cache-read, memory-dump, etc...
        self.menu()


    def getEmptyContents(self):
        """
        returns a cleared Cache Contents Lists object with dims B x E x S
        """
        contents = []
        for s in range(self.S):
            contents.append([])
            for e in range(self.E):
                contents[s].append([])
                for i in range(self.B + 4):     # add 4 for valid, dirty, replacement, tag+data...
                    # valid bit
                    if i == 0:
                        contents[s][e].append("0")
                    # dirty bit
                    elif i == 1:
                        contents[s][e].append("0")
                    # replacement policy
                    elif i == 2:
                        contents[s][e].append("0")
                    # tag policy
                    elif i == 3:
                        contents[s][e].append("00")
                    # data
                    else:
                        contents[s][e].append("00")
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
                args.append(c.strip()[2:])
            
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

        # tag from command
        readTagString = binaryCommandString[0:self.t-1]
        
        # determine if cache hit
        isHit = False
        value = "-1"
        if readTagString != "":
            block = self.Contents[readSet]
            for line in block:
                if line[3] == readTagString:
                    value = line[4 + readOffset]
                    break
            if value != "":
                isHit = True
        else:
            readTagString = "00"

        # HIT
        if isHit:
            self.CacheHits += 1
            print(f"set:{readSet}")
            print(f"tag:{readTagString}")
            print(f"hit:yes")
            print(f"eviction_policy:-1")
            print(f"ram_address:-1")
            print(f"data:0x{value}")
        
        # MISS
        else:
            self.CacheMisses += 1
            
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
                    evictionLine = np.random.randint(1, self.E+1)  # +1 for index -> int
            
            # least recently used
            # TODO
            elif self.ReplacementPolicy == 2:
                if self.E == 1:
                    evictionLine = 1
                
                elif self.E == 2:
                    # see if the first line was most recently used
                    if self.Contents[readSet][0][2] == "0":
                        evictionLine = 1
                    # otherwise it was the second line
                    else:
                        evictionLine = 2
                        self.Contents[readSet][0][2] = "0"
                
                # if more than 2 lines, need to iterate to check least recent
                else:
                    for l in range(self.E):
                        # if the last line is lest recently used, reset all replacement bits to 0
                        if l == self.E - 1:
                            for line in self.Contents[readSet]:
                                line[2] = "0"
                            evictionLine = l+1
                            break

                        # first line with 0 is the least recently used
                        elif self.Contents[readSet][l][2] == "0":
                            evictionLine = l+1
                            self.Contents[readSet][l][2] = "1"
                            break
            
            # least frequently used
            # TODO
            elif self.ReplacementPolicy == 3:
                pass

            
            # fetch the requested address value from RAM
            ramAddress = hex(int(binaryCommandString, 2))
            ramIndex = int(ramAddress, 16) // self.ADDRESS_WIDTH    # can expect this to always be whole integer regardless
            value = self.RAM[ramIndex]
            
            print(f"set:{readSet}")
            print(f"tag:{readTagString}")
            print(f"hit:no")
            print(f"eviction_line:{evictionLine}")            
            print(f"ram_address:{ramAddress}")            
            print(f"data:0x{value}")


    def cache_write(self, binaryCommandString, dataToWrite):
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

        readTagString = binaryCommandString[0:self.t-1]
        
        # determine if cache hit
        isHit = False
        value = "-1"
        dirtyBit = "-1"
        lineIndex = -1
        if readTagString != "":
            # find the index of the line in the block to write to
            block = self.Contents[readSet]
            for i, line in enumerate(block):
                if line[3] == readTagString:
                    value = line[4 + readOffset]
                    dirtyBit = line[2]
                    lineIndex = i
                    break
        else:
            readTagString = "00"

        
        # HIT
        if isHit:
            self.CacheHits += 1
            self.Contents[readSet][lineIndex][4 + readOffset] = dataToWrite
            
            # get the RAM index from the command
            ramAddress = hex(int(binaryCommandString, 2))
            ramIndex = int(ramAddress, 16) // self.ADDRESS_WIDTH
            
            # when cache hit & policy is set, write data to ram (as well)
            if self.WriteHitPolicy == 1:
                self.RAM[ramIndex] = dataToWrite
            
            
            print(f"set:{readSet}")
            print(f"tag:{readTagString}")
            print(f"hit:yes")
            print(f"eviction_policy:-1")
            print(f"ram_address:-1")
            print(f"data:{value}")
            print(f"dirty_bit:{dirtyBit}")
        
        
        # MISS
        else:
            self.CacheMisses += 1

            # REPLACEMENT POLICY
            evictionLine = -1
            
            # random
            if self.ReplacementPolicy == 1:
                # check if all lines in set are valid
                allValid = True
                for i, line in enumerate(self.Contents[readSet]):
                    if line[0] != "1":
                        allValid = False
                        evictionLine = i + 1
                        break
                
                if allValid:
                    # pick a random eviction line
                    evictionLine = np.random.randint(1, self.E+1)  # +1 for index -> int
            
            # least recently used
            elif self.ReplacementPolicy == 2:
                if self.E == 1:
                    evictionLine = 1
                
                elif self.E == 2:
                    # see if the first line was most recently used
                    if self.Contents[readSet][0][2] == "0":
                        evictionLine = 1
                    # otherwise it was the second line
                    else:
                        evictionLine = 2
                        self.Contents[readSet][0][2] = "0"
                
                # if more than 2 lines, need to iterate to check least recent
                else:
                    for l in range(self.E):
                        # if the last line is lest recently used, reset all replacement bits to 0
                        if l == self.E - 1:
                            for line in self.Contents[readSet]:
                                line[2] = "0"
                            evictionLine = l+1
                            break

                        # first line with 0 is the least recently used
                        elif self.Contents[readSet][l][2] == "0":
                            evictionLine = l+1
                            self.Contents[readSet][l][2] = "1"
                            break
            
            # least frequently used
            # TODO
            elif self.ReplacementPolicy == 3:
                pass


            if self.WriteMissPolicy == 1:
                # set the valid bit of eviction line to 1
                self.Contents[readSet][evictionLine - 1][0] = "1"

                # get the RAM index from the command
                ramAddress = hex(int(binaryCommandString, 2))
                ramIndex = int(ramAddress, 16) // self.ADDRESS_WIDTH
                
                # set the next self.B cache bytes from RAM
                for i in range(self.B):
                    self.Contents[readSet][evictionLine - 1][4 + i] = self.RAM[ramIndex + i]

                # now overrite the copied data with the dataToWrite
                self.Contents[readSet][evictionLine - 1][4 + readOffset] = dataToWrite

                # write the data to RAM if theres also a writeHitPolicy, otherwise set the dirty bit to 1
                if self.WriteHitPolicy == 1:
                    self.RAM[ramIndex] = dataToWrite
                else:
                    self.Contents[readSet][evictionLine - 1][1] = "1"


            # fetch the requested address value from RAM
            ramAddress = hex(int(binaryCommandString, 2))
            ramAddressString = ""
            if ramAddress == 0:
                ramAddressString = "0x00"
            elif ramAddress == 8:
                ramAddressString = "0x08"
            else:
                ramAddressString = str(ramAddress)
            
            print(f"set:{readSet}")
            print(f"tag:{readTagString}")
            print(f"hit:no")
            print(f"eviction_line:{evictionLine}")            
            print(f"ram_address:{ramAddressString}")            
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
        with open("cache.txt", 'w') as cacheFile:
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
        
        # again assuming constant address width of 8
        # stored in instance @ self.ADDRESS_WIDTH
        print("memory_content:")
        print("address:data")

        firstLine = True
        for i, r in enumerate(self.RAM):
            if firstLine:
                print(f"0x00:", end="")
                firstLine = False
            elif i % self.ADDRESS_WIDTH == 0:
                if i == 8:
                    print(f"\n0x08:", end="")
                else:
                    print(f"\n{str(hex(i)).upper()}:", end="")
            
            print(r, end=" ")


    def memory_dump(self):
        """
        writes the current RAM data to the file 'ram.txt'
        """
        # will create or overrite the 'ram.txt' file
        with open("ram.txt", 'w') as ramWrite:
            for i, r in enumerate(self.RAM):
                # cast numbers to strings and write
                ramWrite.write(r)
                
                # no newline at end of file
                if i < len(self.RAM):
                    ramWrite.write('\n')
