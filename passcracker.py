# Developer: Kevin F. Stanley
# Class: CSC4281 - Pen Testing

# Description - This tool is used to crack passwords in the shadow file. It takes the parameters
#               (Shadowfile) (wordlist) Optional (-m)

# Usage - This script must be called with python 3.
#         EX: python3 passcracker.py /etc/shadow /wordlist/list -m


import socket
import sys
import os
import crypt

#Mangling rule 1: reverse first char case
def crackWithMangling1(ePass, wL):
    #split string on the '$' divider
    test = ePass.split("$")
    #build back the salt and store in a variable
    salt = "$" + test[1] + "$" + test[2]

    #Loop through each word in wordlist
    for line in wL:
        #Strip the new line char off each word
        sLine = line.strip('\n')
        #Only attempt to hash / compare if something exists on that line in the wordlist
        if sLine != "":
            #Swap first char. if upper make lower and vise versa.
            sLine = sLine[0].swapcase() + sLine[1:]
            #Check if hash is equal.
            if crypt.crypt(sLine, salt) == (salt + "$" + test[3]):
                print("Password Found: ", sLine)
                return 1




#Mangling rule 2: Try symbols attached to end. ASCII numbers 33 - 47
def crackWithMangling2(ePass, wL):
    #split string on the '$' divider
    test = ePass.split("$")
    #build back the salt and store in a variable
    salt = "$" + test[1] + "$" + test[2]

    #Loop through each word in wordlist
    for line in wL:
        #Strip the new line char off each word
        sLine = line.strip('\n')
        #Only attempt to hash / compare if something exists on that line in the wordlist
        if sLine != "":
            #Add a blank char at the end of word to fix issue of the swap inside the loop
            sLine = sLine + " "
            #Loop through 33-47 and try the ASCII char's at the end of the word
            for z in range(33,48):
                sLine = sLine[:-1]
                sLine = sLine + chr(z)
                if crypt.crypt(sLine, salt) == (salt + "$" + test[3]):
                    print("Password Found: ", sLine)
                    return 1


#Try Both rules together
def crackWithMangling3(ePass, wL):
    #split string on the '$' divider
    test = ePass.split("$")
    #build back the salt and store in a variable
    salt = "$" + test[1] + "$" + test[2]

    #Loop through each word in wordlist
    for line in wL:
        #Strip the new line char off each word
        sLine = line.strip('\n')
        #Only attempt to hash / compare if something exists on that line in the wordlist
        if sLine != "":
            #Swap upper with lower and vise versa of first char on word
            sLine = sLine[0].swapcase() + sLine[1:]
            #add blank char
            sLine = sLine + " "
            #Loop through 33-47 and try the ASCII char's at the end of the word
            for z in range(33,48):
                sLine = sLine[:-1]
                sLine = sLine + chr(z)
                if crypt.crypt(sLine, salt) == (salt + "$" + test[3]):
                    print("Password Found: ", sLine)
                    return 1









def crackWithoutMangling(ePass, wL):
    #split string on the '$' divider
    test = ePass.split("$")
    #build back the salt and store in a variable
    salt = "$" + test[1] + "$" + test[2]

    for line in wL:
        sLine = line.strip('\n')
        if sLine != "":
            if crypt.crypt(sLine, salt) == (salt + "$" + test[3]):
                print("Password Found: ", sLine)
                return





# Corrects the issue of nothing being entered as an argument
try:
    sys.argv[1]
except IndexError:
    print("Invalid argument. Try: passcracker.py (shadow file path) (path to wordlist)\n Example: python3 passcracker.py /etc/shadow.txt /wordlists/common.txt [optional] -m")
    sys.exit()

# Checks if the entered shadow file exists
if(os.path.exists(sys.argv[1]) == 0):
    print("Shadow file doesn't exists.")
    sys.exit()
else:
    print("Shadow file found\n")
    file1 = sys.argv[1]

# Corrects the issue if nothing is entered for the wordlist file
try:
    sys.argv[2]
except IndexError:
    print("Invalid argument. Try: passcracker.py (shadow file path) (path to wordlist)\n Example: python3 passcracker.py /etc/shadow.txt /wordlists/common.txt [optional] -m")
    sys.exit()

# Checks if the entered shadow file exists
if(os.path.exists(sys.argv[2]) == 0):
    print("Wordlist file doesn't exists.")
    exit()
else:
    print("Wordlist file found.\n")
    file2 = sys.argv[2]

try:
    sys.argv[3]
    if sys.argv[3] == "-m":
        print("Mangling option enabled.\n")
        m = 1;
    else:
        print("Invalid argument. Try: passcracker.py (shadow file path) (path to wordlist)\n Example: python3 passcracker.py /etc/shadow.txt /wordlists/common.txt [optional] -m")

except IndexError:
    print("Not Mangling.\n")
    m = 0;


#Attempt to open wordlist file and shadow file
sFile = open(file1,'r')
wFile = open(file2,'r')
wLines = wFile.readlines()


#Loops through shadowfile
for line in sFile:
    test = line.split(":")
    #If password field contains just a '!' or '*' then ignore
    if test[1] != '!' and test[1] != '*':
        print("*********************************************")
        print("User: " + test[0])
        #If mangling is enabled loop through different mangling methods.
        if m == 1:
            if(crackWithMangling1(test[1], wLines) != 1):

                if(crackWithMangling2(test[1], wLines) != 1):

                    if(crackWithMangling3(test[1], wLines) != 1):
                        print("Mangling failed. Try without -m.")
        else:
            crackWithoutMangling(test[1], wLines)

print("*********************************************")
print("Done...")



# Catches keyboard interrupt
#except KeyboardInterrupt:
#    print("\nKeyboard Interrupt Signal Detected. Exiting Program...")
#    sys.exit()
