
import party
import sys
import main

fileName = None

def init(inputFile):
    global fileName
    fileName = inputFile

def fullyRecoverHealth(orderInParty):
    if (orderInParty > party.getNumberOfPartyMembers() or orderInParty < 1):
        print('[!] Can only set max health on a pokemon in the party. Supply a number between {} and 1'.format(party.getNumberOfPartyMembers()))
        sys.exit(1)
    # set offset variables and other constants
    maxHPoffset = 0x22
    currentHPoffset = 0x01
    pokemonPartyDataStart = 0x2f34
    lengthPokemonData = 44

    # goes to the start of the pokemon data that was inputted
    pokemonPartyDataStart = pokemonPartyDataStart + ((orderInParty - 1) * lengthPokemonData)

    # get location of max and current hps for the pokemon (both are 2 bytes)
    maxHPlocation = pokemonPartyDataStart + maxHPoffset
    currrentHPlocation = pokemonPartyDataStart + currentHPoffset

    with open(fileName, 'rb+') as f:
        ram = bytearray(f.read())
        maxhp = ram[maxHPlocation:maxHPlocation+2]

        ram[currrentHPlocation] = maxhp[0]
        ram[currrentHPlocation+1] = maxhp[1]
        
        f.seek(0,0)
        f.write(ram)
        print('HP of pokemon {} was set to max value'.format(orderInParty))
    
def setMaxHealth(orderInParty, value):
    if (orderInParty > party.getNumberOfPartyMembers() or orderInParty < 1):
        print('[!] Can only set max health on a pokemon in the party. Supply a number between {} and 1'.format(party.getNumberOfPartyMembers()))
        sys.exit(1)
    
    pokemonPartyDataStart = 0x2f34
    maxHPoffset = 0x22
    lengthPokemonData = 44

    pokemonPartyDataStart = pokemonPartyDataStart + ((orderInParty - 1) * lengthPokemonData)

    firstMaxHPByte = pokemonPartyDataStart + maxHPoffset
    secondMaxHPByte = firstMaxHPByte + 1

    hpBytes = [firstMaxHPByte, secondMaxHPByte]

    strHex = hex(value)[2:]
    while (len(strHex) != 4):
        strHex = "0" + strHex

    newHealthBytes = [int(strHex[:2], 16), int(strHex[2:], 16)]

    if(main.writeToRam(main.getFilename(), hpBytes, newHealthBytes) == 0):
        print('Max HP of pokemon {} set to {}'.format(orderInParty, value))
    else:
        print('[!] Error: Max HP of pokemon {} not set'.format(orderInParty))

def add_xp(orderInParty, amountToAdd):
    if (orderInParty > party.getNumberOfPartyMembers() or orderInParty < 1):
        print("[!] Can't add XP to Pokemon not in party. Supply a number between {} and 1".format(party.getNumberOfPartyMembers()))
        sys.exit(1)
    
    