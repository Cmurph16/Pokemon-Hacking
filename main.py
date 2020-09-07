# normal imports
import struct
import sys
import string

# imports from other files I wrote
import party
import pokemon

# Helper for writeName
# Creates a dict that pairs all uppercase letters with the number that the pokemon games use for encoding
# Returns: letter and number paired dictionary
def getLetterValuePairing():
    letterDict = {}
    counter=0
    for i in range(0x80,0x99):
        letterDict[string.ascii_uppercase[counter]] = i
        counter += 1
    return letterDict

# Updates the player name in the game
def writeName(name,rival=False):
    if (len(name) > 10):
        print('[!] Error: length of name to write is too long. Max length is 10')
        sys.exit(1)

    if (len(name) < 1):
        print('[!] Error: length of name to write is too short. Name must be at least one character')
        sys.exit(1)

    letterPairing = getLetterValuePairing()
    name = name.upper()
    bytesToAdd = bytearray()
    # gets the number used for each letter 
    for letter in name:
        bytesToAdd.append(letterPairing[letter])

    # add in terminating character
    bytesToAdd.append(0x50)

    # add in trailing zeroes in the name buffer
    while (len(bytesToAdd) < 11):
        bytesToAdd.append(0x00)

    # bytes where the name is saved in memory
    nameBytes = []
    firstNameByte = 0x2598
    if (rival == True):
        firstNameByte = 0x25f6
    lengthOfNameBuffer = 0xb
    for offset in range(0x0, lengthOfNameBuffer):
        nameBytes.append(firstNameByte+offset)

    print(nameBytes)
    
    if (writeToRam(getFilename(), nameBytes, bytesToAdd) == 0):
        print('{} written as name to game'.format(name))
    else:
        print('[!] Name not updated')

# Sets the player's money to the value supplied
# Value can not be more than 3 bytes (6 numbers), so max value is 999999
def setMoney(value):
    if (len(str(value)) > 6):
        print('[!] Money value is too high. Max value is 999999')
        sys.exit(1)
    valueString = str(value)

    # makes sure money value is 6 characters so it can be broken up into groups of 2
    while (len(valueString) != 6):
        valueString = '0' + valueString

    # creates a byte array, then loops through the supplied value and for every two numbers, convert into decimal and add to array
    suppliedBytes = bytearray()
    for start in range(0, len(valueString), 2):
        groupOfTwoNumbers = valueString[start:start+2]
        suppliedBytes.append(int(groupOfTwoNumbers, 16))
    
    moneyBytes = [0x25f3, 0x25f4, 0x25f5]

    if (writeToRam(getFilename(), moneyBytes, suppliedBytes) == 0):
        print('Money set to {}'.format(value))
    else:
        print('[!] Money not set')

# Function to write information to ram
# Will write the bytes sup plied as valuesToWrite into the spots supplied in placesToWrite in the file supplied as fileName
def writeToRam(fileName, placesToWrite, valuesToWrite):
    # the number of bytes you are trying to write has to be the same as the size of the location you are writing to in RAM
    if (len(valuesToWrite) != len(placesToWrite)):
        print('[!] Error: The number of values to write is different than the number of places to write to')
        sys.exit(1)
    # open file in byte read plus mode 
    with open(fileName, 'rb+') as f:
        ram = bytearray(f.read())
        # for every byte in the values you are writing, copy this byte into the correct location in the RAM
        for byte in range(len(valuesToWrite)):
            ram[placesToWrite[byte]] = valuesToWrite[byte]
        # go back to beginning of RAM and rewrite with new RAM
        f.seek(0,0)
        f.write(ram)
    return 0
    
# updates the checksum at the end of the ram
# watch liveoverflow video or look at https://bulbapedia.bulbagarden.net/wiki/Save_data_structure_in_Generation_I#Checksum for more info
def fixChecksum():
    fileName = getFilename()
    with open(fileName, 'rb+') as f:
        ram = bytearray(f.read())
        checksum = 255
        for byte in ram[0x2598:0x3523]:
            checksum -= byte
            
        # the & 0xff makes sure it only takes the last 8 bits
        ram[0x3523] = checksum & 0xff

        # seek selects the position in the file to go to
        f.seek(0,0)
        f.write(ram)
        print('Checksum of {} written'.format(checksum & 0xff))

# returns the save file to edit
def getFilename():
    return sys.argv[1]

def main(): 
    if(len(sys.argv) == 1):
        print('Usage: main.py <name of gameboy file>')
        sys.exit(1)
    party.init(getFilename())
    pokemon.init(getFilename())
    writeName('C')
    # writeName('JennieF', True)
    setMoney("999999")
    pokemon.setMaxHealth(1,999)
    pokemon.fullyRecoverHealth(1)
    pokemon.healStatus(1)
    pokemon.setPerfectIVs(1)
    fixChecksum()

if __name__ == '__main__':
    main()
    

