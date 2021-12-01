# File: cachesimulator.py
# Author(s): Cameron Herring & John Gutierrez
# Date: 11/30/2021
# Section: 504
# E-mail(s): cameronherring@tamu.edu 
# Description:
# Implementing a cache simulator


def simulator_menu():
    command = "n/a"
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
        
        command = input("")
        if (command == "cache-read"):

        elif (command == "cache-write"):

        elif (command == "cache-flush"):
        
        elif (command == "cache-view"):

        elif (command == "memory-view"):

        elif (command == "cache-dump"):

        elif (command == "memory-dump"):

        else:
            if (command != "quit"):
                print("Please type a command from the menu.")
