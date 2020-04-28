# functions that deal with the party itself

pokemonPartyDataStart = 0x2f34
lengthPokemonData = 44

fileName = None

def init(inputFile):
    global fileName
    fileName = inputFile

def getNumberOfPartyMembers():
    maxPartyMembers = 6
    numPartyMembers = 1
    with open(fileName, 'rb+') as f:
        ram = bytearray(f.read())
        for orderNumber in range(1,maxPartyMembers):
            possiblePokemon = ram[pokemonPartyDataStart + (lengthPokemonData * orderNumber)]
            if (possiblePokemon == int('00', 16) or numPartyMembers == maxPartyMembers):
                return numPartyMembers
            numPartyMembers += 1
