# File: cachesimulator.py
# Author(s): Cameron Herring & John Gutierrez
# Date: 11/30/2021
# Section: 504
# E-mail(s): cameronherring@tamu.edu 
# Description:
# Implementing a cache simulator


import sys

from .menu import simulator_menu


if __name__ == "__main__":
    args = sys.argv[1:]
    filename = args[0].strip()

    print("*** Welcome to the cache simulator ***")
    init = input("initialize the RAM:\n")

    # simulator_menu()
