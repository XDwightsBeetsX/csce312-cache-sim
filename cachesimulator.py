# File: cachesimulator.py
# Author(s): Cameron Herring & John Gutierrez
# Date: 11/30/2021
# Section: 504
# E-mail(s): cameronherring@tamu.edu 
# Description:
# Implementing a cache simulator


import sys

# from menu import simulator_menu


if __name__ == "__main__":
    args = sys.argv[1:]
    filename = args[0].strip()

    if filename != "input.txt":
        print("Invalid filename. Expected: 'input.txt'")
        print("quitting...")
        quit()
    
    # 1. Initialize the physical memory
    # + byte-addressable
    print("*** Welcome to the cache simulator ***")
    init = input("initialize the RAM:\n").split(" ")  # expected command is 'init-ram 0x# 0x#'
    ramStart, ramEnd = int(init[1], 0), int(init[2], 0)
    cacheSize = ramEnd - ramStart + 1
    print(cacheSize)

    # simulator_menu()
    # [set][line][char]
