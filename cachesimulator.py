# File: cachesimulator.py
# Author(s): Cameron Herring & John Gutierrez
# Date: 11/30/2021
# Section: 504
# E-mail(s): cameronherring@tamu.edu 
# Description:
# Implementing a cache simulator


import sys
from Cache import Cache


if __name__ == "__main__":
    """
    (python default entry location)

    Prompts the user to initialize the RAM size, reading in data from 'input.txt'
    """
    # parse the input.txt from the command line argument: 
    #   '>python cachesimulator.py input.txt'
    args = sys.argv[1:]
    filename = args[0].strip()

    # only 'input.txt' files are allowed
    if filename != "input.txt":
        print("Invalid filename. Expected: 'input.txt'")
        print("quitting...")
        quit()
    
    # title heading
    print("*** Welcome to the cache simulator ***")

    # initialize the physical memory
    # expected command is 'init-ram 0x# 0x#'
    init = input("initialize the RAM:\n").split(" ")
    ramStart, ramEnd = int(init[1], 16), int(init[2], 16)
    ramSize = ramEnd - ramStart + 1  # inclusive

    # init RAM by reading bytes into list from 'input.txt'
    ram = []
    with open(filename, "r") as inputFile:
        lines = inputFile.read().splitlines()
        ram = lines[0:ramSize]
    
    # RAM has been set, use this to make the Cache
    # the Cache takes care of prompting user input from menu() and performing operations
    print("RAM successfully initiated!")
    cache = Cache(ram)
