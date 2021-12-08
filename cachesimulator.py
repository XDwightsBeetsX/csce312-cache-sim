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
    args = sys.argv[1:]
    filename = args[0].strip()

    if filename != "input.txt":
        print("Invalid filename. Expected: 'input.txt'")
        print("quitting...")
        quit()
    
    # 1. Initialize the physical memory
    print("*** Welcome to the cache simulator ***")

    init = input("initialize the RAM:\n").split(" ")  # expected command is 'init-ram 0x# 0x#'
    ramStart, ramEnd = 0, 255  # int(init[1], 16), int(init[2], 16)
    ramSize = ramEnd - ramStart + 1

    # init RAM by reading first bytes into list
    ram = []
    with open(filename, "r+") as inputFile:
        lines = inputFile.read().splitlines()
        ram = lines[0:ramSize]

    print("RAM successfully initiated!")
    
    cache = Cache(ram)
