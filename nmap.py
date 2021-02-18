# Developer: Kevin F. Stanley
# Class: CSC4281 - Pen Testing

# Description - This tool mimicks nmap. Using python3, we import sockets to check for connection errors to port ranges between 1 and 65535;
# System is imported to accept arguments from the command line.

# Usage - this script must be called with python 3.   EX: python3 -i 127.0.0.1
#         -i must be followed by an ip address.

import socket
import sys

# Corrects the issue of nothing being entered as an argument
try:
    sys.argv[1]
except IndexError:
    print("Invalid argument. Try: -i (ip address)")
    sys.exit()

# If the argument isnt -i then alert the use of the correct usage
if(sys.argv[1] != "-i"):
    print("Invalid argument. Try: -i (ip address)")
    exit()


# Corrects the issue if nothing is entered for the ip address for the -i argument
try:
    sys.argv[2]
except IndexError:
    print("You must enter an IP address. Try: -i (ip address)")
    sys.exit()

host = sys.argv[2]

# Checks if the host is just a number... Alert the user to enter an ip address
if host.isdecimal():
    print("You must enter an IP address. Try: -i (ip address)")
    sys.exit()

print("-----------------------------------------------\n", "Scanning Host:", host, "\n","-----------------------------------------------\n")

# catches keyboard interrupt while trying to scan ports
try:
    # main loop to scan all known ports by creating sockets and displaying if port is listed as open.
    for x in range(1,65535):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Sets socket timeout to prevent socket connection from hanging.
            sock.settimeout(2)

            result = sock.connect_ex((host, x))
            if result == 0:
                print("port", x, ": open")
            sock.close()
        except socket.gaierror:
            print("Connection failed...")
            sys.exit()

# Catches keyboard interrupt
except KeyboardInterrupt:
    print("\nKeyboard Interrupt Signal Detected. Exiting Program...")
    sys.exit()
