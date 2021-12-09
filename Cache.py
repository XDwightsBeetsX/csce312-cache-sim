

from math import log
from utils import getBinaryStringFromHexString

import random as rand

class Cache(object):
    """
    Cache object stores the Cache.Contents

    Initialized from a 1-D array of RAM

    The size and dimensions of the contents are set by prompts in __init__

    Able to perform operations offered in the 'menu()' loop such as cache-read and memory-dump

    Tracks the number of CacheHits and CacheMisses
    """
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
        Helper method for initialization and flushing.

        returns a cleared lists object with dims (4+B) x E x S

        ** NOTE: initial tags are set to None, printed as '00'
        this fixes issues with an initial cache-read 0x00 -> hit **
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
                        contents[s][e].append(None)  # "00" but issue w/ cache-read "00" -> Hit
                    # data
                    else:
                        contents[s][e].append("00")
        return contents


    def setContentsFromRam(self, ramIndex, setIndex, evictionLine, targetTagBinStr):
        """
        Helper function to set a Cache line from RAM
        
        Sets:
            valid bit to "1"
            tag to input tag
            contents from RAM
        """
        # set the tag to the hexadecimal requested tag
        tagHexString = str(hex(int(targetTagBinStr, 2)))[2:].zfill(2).upper()
        self.Contents[setIndex][evictionLine-1][3] = tagHexString

        # set the valid bit to "1"
        self.Contents[setIndex][evictionLine-1][0] = "1"

        # set the next self.B cache bytes from RAM
        for i in range(self.B):
            self.Contents[setIndex][evictionLine - 1][4 + i] = self.RAM[ramIndex + i]
    

    def isCacheHit(self, setIndex, targetTagBinStr, targetOffsetIndex):
        """
        Determines if cache Hit/Miss
        
        Returns Hit/Miss (bool), value/"-1", lineIndex/-1, dirtyBit/-1
        """
        # if one block per set, no need to check tag (0 anyway)
        if self.E == self.S:
            return True, self.Contents[setIndex][0][targetOffsetIndex], -1, -1
        
        # otherwise, need to find the block line with matching tag
        targetTagInt = int(hex(int(targetTagBinStr, 2)), 16)
        block = self.Contents[setIndex]
        for i, line in enumerate(block):
            # see if any of the lines in the set block match the tag
            thisTagRaw = line[3]

            # check if this block has not been set ever
            if thisTagRaw is None:
                return False, "-1", -1, -1

            # this block has a tag, see if it matches
            else:
                if int(thisTagRaw, 16) == targetTagInt:
                    # this line in the setIndex matches the tag -> HIT
                    return True, line[4 + targetOffsetIndex], i, line[1]
        
        return False, "-1", -1, -1
    

    def menu(self):
        """
        Command loop takes input command and directs operation to the corresponding class method
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
                args.append(c.strip()[2:].upper())
            

            # =====================================
            # =========== MENU COMMANDS ===========
            # =====================================
            # use getBinaryStringFromHexString helper method to parse hex instructions
            if (command == "cache-read"):
                binaryCommandString = getBinaryStringFromHexString(args[0])
                self.cache_read(binaryCommandString)

            elif (command == "cache-write"):
                binaryCommandString = getBinaryStringFromHexString(args[0])
                hexDataToWriteStr = str(args[1]).upper()
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
        offsetIndex = int(binaryCommandString[-self.b:], 2)

        # check set associativity
        s = binaryCommandString[self.t:-self.b]
        setIndex = 0
        if s != "":
            setIndex = int(s, 2)

        # tag from command
        targetTagBinStr = binaryCommandString[0:self.t]
        
        # pre-set some vars to update if a cache hit
        isHit, value, _lineIndex, _dirtyBit = self.isCacheHit(setIndex, targetTagBinStr, offsetIndex)

        # ====================================
        # ============== HIT =================
        # ====================================
        if isHit:
            self.CacheHits += 1
            print(f"set:{setIndex}")
            print(f"tag:{str(hex(int(targetTagBinStr, 2)))[2:].zfill(2).upper()}")
            print(f"hit:yes")
            print(f"eviction_line:-1")
            print(f"ram_address:-1")
            print(f"data:0x{value}")
        
        # ====================================
        # ============== MISS ================
        # ====================================
        else:
            self.CacheMisses += 1

            # pre-set the evition line to be overriten based on the ReplacementPolicy
            evictionLine = -1

            # REPLACEMENT POLICY
            # random
            if self.ReplacementPolicy == 1:
                # check if all lines in set are valid
                validCheck = [True, 0]
                for i, line in enumerate(self.Contents[setIndex]):
                    if line[0] != "1":
                        validCheck[0] = False
                        validCheck[1] = i + 1
                        break
                
                if not validCheck[0]:
                    print("not all valid: ", validCheck)
                    # pick the first invalid line
                    evictionLine = validCheck[1]
                
                else:
                    # pick a random eviction line
                    evictionLine = rand.randint(1, self.E+1)  # +1 for index -> int
            
            # least recently used
            elif self.ReplacementPolicy == 2:
                if self.E == 1:
                    evictionLine = 1
                
                elif self.E == 2:
                    # see if the first line was most recently used
                    if self.Contents[setIndex][0][2] == "0":
                        evictionLine = 1
                    # otherwise it was the second line
                    else:
                        evictionLine = 2
                        self.Contents[setIndex][0][2] = "0"
                
                # if more than 2 lines, need to iterate to check least recent
                else:
                    for l in range(self.E):
                        # if the last line is lest recently used, reset all replacement bits to 0
                        if l == self.E - 1:
                            for line in self.Contents[setIndex]:
                                line[2] = "0"
                            evictionLine = l+1
                            break

                        # first line with 0 is the least recently used
                        elif self.Contents[setIndex][l][2] == "0":
                            evictionLine = l+1
                            self.Contents[setIndex][l][2] = "1"
                            break
            
            # least frequently used
            # TODO
            elif self.ReplacementPolicy == 3:
                pass

            
            # fetch the requested address value from RAM
            ramAddress = hex(int(binaryCommandString, 2))
            ramIndex = int(ramAddress, 16) // self.ADDRESS_WIDTH    # can expect this to always be whole integer regardless

            # set the valid bit, tag, and data
            self.setContentsFromRam(ramIndex, setIndex, evictionLine, targetTagBinStr)

            value = self.RAM[ramIndex]
            
            print(f"set:{setIndex}")
            print(f"tag:{str(hex(int(targetTagBinStr, 2)))[2:].zfill(2).upper()}")
            print(f"hit:no")
            print(f"eviction_line:{evictionLine}")            
            print(f"ram_address:0x{ramAddress[2:].zfill(2).upper()}")            
            print(f"data:0x{value}")


    def cache_write(self, binaryCommandString, dataToWrite):
        """
        Determines if the binaryCommandString results in a hit or miss in the cache
        
        Displays intermediate info such as set and tag numbers
        """
        # offset will always be present
        offsetIndex = int(binaryCommandString[-self.b:], 2)

        # check set associativity
        s = binaryCommandString[self.t:-self.b]
        setIndex = 0
        if s != "":
            setIndex = int(s, 2)

        # tag from command
        targetTagBinStr = binaryCommandString[0:self.t]
        
        # pre-set some vars to update if a cache hit
        # if there is a hit, safe to use lineIndex, otherwise lineIndex=-1
        isHit, value, lineIndex, dirtyBit = self.isCacheHit(setIndex, targetTagBinStr, offsetIndex)

        
        # =====================================
        # =============== HIT =================
        # =====================================
        if isHit:
            self.CacheHits += 1
            self.Contents[setIndex][lineIndex][4 + offsetIndex] = dataToWrite
            
            # get the RAM index from the command
            ramAddress = hex(int(binaryCommandString, 2))
            ramIndex = int(ramAddress, 16) // self.ADDRESS_WIDTH
            
            # WRITE HIT (THROUGH)
            # write the data to RAM if theres also a writeHitPolicy
            if self.WriteHitPolicy == 1:
                self.RAM[ramIndex] = dataToWrite
            # otherwise set the dirty bit to 1
            else:
                self.Contents[setIndex][lineIndex][1] = "1"
            
            # print the results
            print(f"set:{setIndex}")
            print(f"tag:{str(hex(int(targetTagBinStr, 2)))[2:].zfill(2).upper()}")
            print(f"hit:yes")
            print(f"eviction_policy:-1")
            print(f"ram_address:-1")
            print(f"data:0x{value}")
            print(f"dirty_bit:{dirtyBit}")
        
        
        # =====================================
        # ============== MISS =================
        # =====================================
        else:
            self.CacheMisses += 1

            # REPLACEMENT POLICY
            evictionLine = -1
            
            # random
            if self.ReplacementPolicy == 1:
                # check if all lines in set are valid
                allValid = True
                for i, line in enumerate(self.Contents[setIndex]):
                    if line[0] != "1":
                        allValid = False
                        evictionLine = i + 1
                        break
                
                if allValid:
                    # pick a random eviction line
                    evictionLine = rand.randint(1, self.E+1)  # +1 for index -> int
            
            # least recently used
            elif self.ReplacementPolicy == 2:
                if self.E == 1:
                    evictionLine = 1
                
                elif self.E == 2:
                    # see if the first line was most recently used
                    if self.Contents[setIndex][0][2] == "0":
                        evictionLine = 1
                    # otherwise it was the second line
                    else:
                        evictionLine = 2
                        self.Contents[setIndex][0][2] = "0"
                
                # if more than 2 lines, need to iterate to check least recent
                else:
                    for l in range(self.E):
                        # if the last line is lest recently used, reset all replacement bits to 0
                        if l == self.E - 1:
                            for line in self.Contents[setIndex]:
                                line[2] = "0"
                            evictionLine = l+1
                            break

                        # first line with 0 is the least recently used
                        elif self.Contents[setIndex][l][2] == "0":
                            evictionLine = l+1
                            self.Contents[setIndex][l][2] = "1"
                            break
            
            # least frequently used
            # TODO
            elif self.ReplacementPolicy == 3:
                pass

            
            # WRITE MISS POLICY (BACK)
            if self.WriteMissPolicy == 1:
                # fetch the requested address value from RAM
                ramAddress = hex(int(binaryCommandString, 2))
                ramIndex = int(ramAddress, 16) // self.ADDRESS_WIDTH    # can expect this to always be whole integer regardless

                # on a write miss, copy data from RAM to this line of Cache.Contents
                self.setContentsFromRam(ramIndex, setIndex, evictionLine, targetTagBinStr)

                # now overrite the copied data with the dataToWrite
                self.Contents[setIndex][evictionLine - 1][4 + offsetIndex] = dataToWrite

            # WRITE HIT (THROUGH)
            # write the data to RAM if theres also a writeHitPolicy
            if self.WriteHitPolicy == 1:
                self.RAM[ramIndex] = dataToWrite
            # otherwise set the dirty bit to 1
            else:
                self.Contents[setIndex][evictionLine - 1][1] = "1"


            # fetch the requested address value from RAM
            ramAddress = hex(int(binaryCommandString, 2))
            ramAddressString = ""
            # add leading 0x'0'# for addresses 0x0 and 0x8
            if ramAddress == '0x0':
                ramAddressString = "0x00"
            elif ramAddress == '0x8':
                ramAddressString = "0x08"
            else:
                ramAddressString = "0x" + str(ramAddress)[2:].upper()
            
            # print the results
            print(f"set:{setIndex}")
            print(f"tag:{str(hex(int(targetTagBinStr, 2)))[2:].zfill(2).upper()}")
            print(f"hit:no")
            print(f"eviction_line:{evictionLine}")
            print(f"ram_address:{ramAddressString}")
            print(f"data:0x{dataToWrite}")
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
                    cacheValue = self.Contents[s][e][i]
                    if cacheValue == None:
                        cacheValue = "00"

                    if i != 2:
                        print(cacheValue, end=" ")
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
                        cacheValue = self.Contents[s][e][i]
                        if cacheValue == None:
                            cacheValue = "00"
                        cacheFile.write(cacheValue + " ")
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
                    print(f"\n{str(hex(i))}:", end="")
            
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
