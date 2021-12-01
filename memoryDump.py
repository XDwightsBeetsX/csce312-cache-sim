def memoryDump(Ram):
    ramWrite = open("ram.txt", "a")
    for i in range(len(Ram)):
        ramWrite.write(i)
    ramWrite.close()
