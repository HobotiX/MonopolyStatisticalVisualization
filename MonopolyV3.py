import random
import matplotlib.pyplot as plt

GO = 0
TOJAIL = 30
JAIL = 10
CHANCE01 = 7
CHANCE02 = 22
CHANCE03 = 36
COMMUNITYCHEST01 = 2
COMMUNITYCHEST02 = 18
COMMUNITYCHEST03 = 33
PROPERTY = [    "                       GO",
                "     Mediterranean Avenue",
                "     Community Chest (GO)",
                "            Baltic Avenue",
                "               Income Tax",
                "         Reading Railroad",
                "          Oriental Avenue",
                "              Chance (GO)",
                "           Vermont Avenue",
                "       Connecticut Avenue",
                "                     Jail",
                "         St.Charles Place",
                "         Electric Company",
                "            States Avenue",
                "          Virginia Avenue",
                "    Pennsylvania Railroad",
                "           St.James Place",
                "   Community Chest (Jail)",
                "         Tennessee Avenue",
                "          New York Avenue",
                "             Free Parking",
                "          Kentucky Avenue",
                "    Chance (Free Parking)",
                "           Indiana Avenue",
                "          Illinois Avenue",
                "             B&O Railroad",
                "          Atlantic Avenue",
                "           Ventnor Avenue",
                "              Water Works",
                "           Marvin Gardens",
                "               Go to Jail",
                "           Pacific Avenue",
                "    North Carolina Avenue",
                "Community Chest (To Jail)",
                "      Pennsylvania Avenue",
                "      Short Line Railroad",
                "         Chance (To Jail)",
                "               Park Place",
                "               Luxury Tax",
                "                Boardwalk"]
PCOLOR = [  '#cde6d0',
            '#955436',
            '#02aef0',
            '#955436',
            '#cde6d0',
            '#0c0d12',
            '#aae0fa',
            '#f37125',
            '#aae0fa',
            '#aae0fa',
            '#cde6d0',
            '#d93a96',
            '#9419a6',
            '#d93a96',
            '#d93a96',
            '#0c0d12',
            '#f7941d',
            '#02aef0',
            '#f7941d',
            '#f7941d',
            '#cde6d0',
            '#ed1b24',
            '#f37125',
            '#ed1b24',
            '#ed1b24',
            '#0c0d12',
            '#fef200',
            '#fef200',
            '#9419a6',
            '#fef200',
            '#cde6d0',
            '#21b15a',
            '#21b15a',
            '#02aef0',
            '#21b15a',
            '#0c0d12',
            '#f37125',
            '#0072bb',
            '#cde6d0',
            '#0072bb']

# SHUFFLE DECK #################################################################
def randomizeDeck(n):
    temp = [22] * n
    notFound = True
    i = 0
    while i < n:
        while notFound == True:
            rando = random.randrange(n)
            j = 0
            while j <= i:
                if temp[j] == rando:
                    break
                elif j == i:
                    temp[i] = rando
                    notFound = False
                j += 1
        notFound = True
        i += 1
    return temp

# PULL CARD FROM CHANCE DECK ###################################################
def drawFromChance(i,space,deck):
    # ADVANCE TO GO
    if deck[i] == 0:
        return GO
    # ADVANCE TO JAIL
    elif deck[i] == 1:
        return JAIL
    # ADVANCE TO ST CHARLES PLACE
    elif deck[i] == 2:
        return 11
    # ADVANCE TO ILLINOIS AVENUE
    elif deck[i] == 3:
        return 26
    # ADVANCE TO NEAREST NEAREST UTILITY
    elif deck[i] == 4:
        return nearestUtility(space)
    # ADVANCE TO NEAREST NEAREST UTILITY
    elif deck[i] == 5:
        return nearestRailroad(space)
    # ADVANCE TO READING RAILROAD
    elif deck[i] == 6:
        return 5
    # ADVANCE TO BOARDWALK
    elif deck[i] == 7:
        return 39
    # GO BACK 3 SPACES
    elif deck[i] == 8:
        return (space - 3)
    else:
        return space

# PULL CARD FROM COMMUNITY CHEST ###############################################
def drawFromCommunityChest(i,space,deck):
    # ADVANCE TO GO
    if deck[i] == 0:
        return GO
    # ADVANCE TO JAIL
    elif deck[i] == 1:
        return JAIL
    else:
        return space

# CHECK IF DECK NEEDS SHUFFLING ################################################
def shuffleDeck(i,deck):
    if i == len(deck):
        deck = randomizeDeck(len(deck))
        i = 0
    return i, deck

# ROLL DICE ####################################################################
def roll():
     # ROLL DICE
     d1 = random.randrange(6) + 1
     d2 = random.randrange(6) + 1
     # IS DOUBLES?
     if d1 == d2:
         doubles = True
     else:
         doubles = False
     # RETURN VALUE OF THE ROLL + IS DOUBLES
     return (d1+d2), doubles

# GO TO JAIL ###################################################################
def ToJail():
    return JAIL

# FIND NEAREST RAILROAD ########################################################
def nearestRailroad(space):
    if space == 7:
        return 15
    elif space == 22:
        return 25
    else:
        return 5

# FIND NEAREST UTILITY #########################################################
def nearestUtility(space):
    if space == 18:
        return 28
    else:
        return 12

# PASS GO ######################################################################
def passGo(space, lap):
    if space > 39:
        space = space - 40
        lap += 1
    return space, lap

# PLAYER TURN MANAGER ##########################################################
def playerTurnManager(thisPlayer,players,doubles):
    if thisPlayer + 1 < players and doubles != True:
        return (thisPlayer + 1)
    elif doubles == True:
        return thisPlayer
    else:
        return 0

# NEW GAME #####################################################################
def newGame(countLandSpace,rolls,players,f):
    inJail = False
    space = [0] * players
    #playerSpace = [[0] * 40] * players
    thisPlayer = 0
    countDoubles = 0
    jailRolls = 0
    # SET CHANCE DECK
    chanceDeck = [0] * 16
    chanceDeck = randomizeDeck(16)
    countCD = 0
    # SET COMMUNITY CHEST DECK
    communityChestDeck = [0] * 16
    communityChestDeck = randomizeDeck(16)
    countCCD = 0
    lap = 0
    n = 0
    numCol = 0


    while lap < rolls:

        # ROLL DICE
        move,doubles = roll()
        # DICE ROLLING RULES ###################################################
        # ROLL DOUBLES
        if doubles == True:
            countDoubles += 1
            inJail = False
            f.write(str(space[thisPlayer]) + " ")
        # ROLL FOR DOUBLES IN JAIL
        elif inJail == True and jailRolls < 3:
            jailRolls += 1
            countDoubles = 0
        # STANDARD ROLL
        else:
            inJail = False
            jailRolls = 0
            countDoubles = 0
            f.write(str(space[thisPlayer]) + " ")
        lap += 1
        # SPACE MOVEMENT RULES #################################################
        # CHECK IF PLAYER GOT 3 DOUBLES
        if countDoubles == 3:
            space[thisPlayer] = ToJail()
            countLandSpace[thisPlayer][space[thisPlayer]] += 1
            f.write(str(space[thisPlayer]) + "\n")
            inJail = True
        # IF PLAYER CAN MOVE
        elif inJail == False:
            space[thisPlayer] += move
            # PASSING GO
            space[thisPlayer],lap = passGo(space[thisPlayer],lap)

            # LAND ON GO TO JAIL ###############################################
            if space[thisPlayer] == TOJAIL:
                countLandSpace[thisPlayer][space[thisPlayer]] += 1
                f.write(str(space[thisPlayer]) + "\n")
                f.write(str(space[thisPlayer]) + " ")
                #graph[j][space] += 1
                space[thisPlayer] = ToJail()
                #playerSpace[thisPlayer][space[thisPlayer]] += 1
                countLandSpace[thisPlayer][space[thisPlayer]] += 1
                f.write(str(space[thisPlayer]) + "\n")
                #graph[j][space] += 1
                inJail = True
            # LANDING ON COMMUNITY CHEST SPACE #################################################################################
            elif space[thisPlayer] == COMMUNITYCHEST01 or space[thisPlayer] == COMMUNITYCHEST02 or space[thisPlayer] == COMMUNITYCHEST03:
                countLandSpace[thisPlayer][space[thisPlayer]] += 1
                f.write(str(space[thisPlayer]) + "\n")
                temp = space[thisPlayer]
                space[thisPlayer] = drawFromCommunityChest(countCCD,space[thisPlayer],communityChestDeck)
                if space[thisPlayer] != COMMUNITYCHEST01 or space[thisPlayer] != COMMUNITYCHEST02 or space[thisPlayer] != COMMUNITYCHEST03:
                    countLandSpace[thisPlayer][space[thisPlayer]] += 1
                    f.write(str(temp) + " ")
                    f.write(str(space[thisPlayer]) + "\n")
                if space[thisPlayer] == JAIL:
                    inJail = True
                countCCD += 1
                countCCD, communityChestDeck = shuffleDeck(countCCD, communityChestDeck)
            # LANDING ON CHANCE SPACE #########################################################################################
            elif space[thisPlayer] == CHANCE01 or space[thisPlayer] == CHANCE02 or space[thisPlayer] == CHANCE03:
                countLandSpace[thisPlayer][space[thisPlayer]] += 1
                f.write(str(space[thisPlayer]) + "\n")
                temp = space[thisPlayer]
                space[thisPlayer] = drawFromChance(countCD,space[thisPlayer],chanceDeck)
                if space[thisPlayer] != CHANCE01 or space[thisPlayer] != CHANCE03 or space[thisPlayer] != CHANCE03:
                    countLandSpace[thisPlayer][space[thisPlayer]] += 1
                    f.write(str(temp) + " ")
                    f.write(str(space[thisPlayer]) + "\n")
                if space[thisPlayer] == JAIL:
                    inJail = True
                countCD += 1
                countCD, chanceDeck = shuffleDeck(countCD, chanceDeck)
            # LANDING ON NORMAL SPACE ##########################################################################################
            else:
                countLandSpace[thisPlayer][space[thisPlayer]] += 1
                f.write(str(space[thisPlayer]) + "\n")
        thisPlayer = playerTurnManager(thisPlayer,players,doubles)


def PlotMonopoly(data):
    plt.barh(PROPERTY,data[0],color=PCOLOR)
    #plt.invert_yaxis()
    #plt.ylabel(PROPERTY)
    plt.xlabel('Times Landed')
    plt.title('Monopoly')
    plt.show()

################################################################################
if __name__ == '__main__':
    again = 0
    rolls = 500
    games = 1
    players = 1
    f = open("monopoly_network.edges", "a")

    #graph = [[0]*games] * 20
    #propertyAverage = [[0] * 40] * 20
    #countLandSpace = [[0] * 40] * players
    countLandSpace = [[0]*40 for _ in range(players)]

    newGame(countLandSpace,rolls,players,f)
    f.close()
    PlotMonopoly(countLandSpace)
