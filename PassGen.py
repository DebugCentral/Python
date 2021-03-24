#Developer: Kevin F. Stanley
#Class: ITP 270 Python Programming
#Description: Password Generator
#Python Version used in Development: Python3.8

#   This program take in command line parameters to generate a password based on user
#   Specification. The command line parameters are listed below with example input and
#    output.
#
#    -l (input legnth) : The -l (lowercase L) option specifies the length. if not set, the default is 12
#     -U                : This option specifices to add uppercase letters to the generated password.
#     -L                : If this parameter is set, The password will add Lowercase letters to the password.
#     -N                : If this parameter is set, Numbers will be added to the generated password (0-9).
#     -S                : If this parameter is set, Special characters will be added to the generated password (  !@#$%^&*()-_=+<>?:";',./  )

# Note: If no parameters are set, the options are randomized to either enable or disable the options above.
#       If atleast 1 parameter is set, then you must enable the other options.

#Example 1: ./PassGen.py    : This will randomize the options and generate a default password of default length of 12

#Example 2: ./PassGen.py -L 15   : This will generate a random password of 15 with all other options disabled by default.

#Example 3: ./PassGen.py -L 15 -U   : This option generates a password of legnth 15 just using Uppercase letters.

#Example 4: ./PassGen.py -l 15 -U -L    : This option generates a Password of length 15 using uppercase letters and lowercase letters.

import random
import string
import sys
import getopt

#Function to randomize the options in the instance the user doesnt choose an option other than just length
def generateOpts():
    #Defines exiting the while loop
    exitLevel = 0
    #This loop exists in the case the function generates no options. It will re-generate until atleast 1 option exists
    while exitLevel == 0:
        opts = []
        #Generates random options
        for x in range(0, 4):
            if random.randint(1, 100) % 2 == 1:
                opts.append(1)
            else:
                opts.append(0)
        #If all options generated doesnt contain a 1, dont exit the while loop
        for y in opts:
            if y == 1:
                exitLevel = 1
    #Return the options back to the generate password function
    return opts

#Function to generate the password. Takes a character set and length
def generatePass(set, length):
    charset = set
    password = ""
    #If no characters exists in the set then no options were selected. generate options and extend list based on the options
    if len(set) == 0:
        print("\nUsing randomized options because no options were set. \n")
        #Sets generated arguments
        args = generateOpts()
        if args[0] == 1:
            charset.extend(string.ascii_uppercase)
        if args[1] == 1:
            charset.extend(string.ascii_lowercase)
        if args[2] == 1:
            charset.extend(string.digits)
        if args[3] == 1:
            charset.extend(string.punctuation)
    #Print out the character set being used
    print("Using the character set: ", charset, "\n")

    #Generate a random string based on the character set
    for x in range(0,length):
        password += charset[random.randrange(0,len(charset))]
    print("Generated Password: ",password, "\n\nThank you for using PassGen")





#Get system arguments and parse through
CharLength = int(12)
CharList = []
#Print out the usage in the case the options we're not properly set.
usage =("Usage: This program has 5 different options...\n"
    "-l (num)    : This option allows the user to specify a password length. Default is 12\n"
    "-U          : This option adds uppercase letters to the character set.\n"
    "-L          : This option adds lowercase letters to the character set.\n"
    "-N          : This option adds numbers to the character set.\n"
    "-S          : This option adds special symbols to the character set.\n\n"
    "If no options are set, then the specificed options are randomized with a default length of 12.\n")

#Try Except block to check getopt errors in the case an illegal option is selected
try:
    opts, args = getopt.getopt(sys.argv[1:], "ULNSl:")
    #Loops through the options set by the user from the arguments
    for opt, arg in opts:

        #Checks the defined options to see if they are selected.
        if opt in ['-U']:
            CharList.extend(string.ascii_uppercase)
            print("Adding Uppercase to character set...")
        elif opt in ['-L']:
            CharList.extend(string.ascii_lowercase)
            print("Adding Lowercase to character set...")
        elif opt in ["-N"]:
            CharList.extend(string.digits)
            print("Adding numbers to character set...")
        elif opt in ['-S']:
            CharList.extend(string.punctuation)
            print("Adding special symbols to character set...\n")
        #Set the length of password to generate in the instance the length is specified
        elif opt in ['-l']:
            try:
                if int(arg) > 0 and isinstance(int(arg), int) == True:
                    CharLength = int(arg)
                else:
                    raise Exception
            except:
                    print("There is an error with you argument for -l. Are you using a positive integer?\n")
                    print(usage)
                    sys.exit(2)

#Catch the errors from command line arguments, print out the errors and usage case, and exit in an error state.
except getopt.GetoptError as err:
    print(err)
    print(usage)
    sys.exit(2)

#function to generate the password
generatePass(CharList, CharLength)
