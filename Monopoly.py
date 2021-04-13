import random
#import plotly.graph_objects as go

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
        return 0
    # ADVANCE TO JAIL
    elif deck[i] == 1:
        return 10
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
    elif deck[i] == 5 or deck[i] == 9:
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
        return 0
    # ADVANCE TO JAIL
    elif deck[i] == 1:
        return 10
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
    return 10

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
def playerTurnManager(turn,players):
    if turn < players:
        return (turn + 1)
    else:
        return 0

# NEW GAME #####################################################################
def newGame(countLandSpace,passingGo,players):
    inJail = False
    space = 0
    #playerSpace = [[0] * 40] * players
    pTurn = 0
    countDoubles = 0
    jailRolls = 0
    chanceDeck = [0] * 16
    chanceDeck = randomizeDeck(16)
    countCD = 0
    communityChestDeck = [0] * 16
    communityChestDeck = randomizeDeck(16)
    countCCD = 0
    lap = 0

    while lap < passingGo:
        # ROLL DICE
        move, doubles = roll()
        # DICE ROLLING RULES
        if doubles:
            countDoubles += 1
            inJail = False
        elif inJail == True and jailRolls < 3:
            jailRolls += 1
            countDoubles = 0
            pTurn = playerTurnManager(pTurn,players)
        else:
            inJail = False
            jailRolls = 0
            countDoubles = 0
            pTurn = playerTurnManager(pTurn,players)

        # SPACE MOVEMENT RULES
        # CHECK IF PLAYER GOT 3 DOUBLES
        if countDoubles == 3:
            countLandSpace[ToJail()] += 1
            #playerSpace[pTurn][ToJail()] += 1 
            inJail = True
        # IF PLAYER CAN MOVE
        elif inJail == False:
            #playerSpace[pTurn][] += move
            space += move
            # PASSING GO
            space,lap = passGo(space,lap)
            # LAND ON GO TO JAIL
            if space == 30:
                countLandSpace[space] += 1
                #graph[j][space] += 1
                space = ToJail()
                countLandSpace[space] += 1
                #graph[j][space] += 1
                inJail = True
            # LANDING ON COMMUNITY CHEST SPACE
            elif space == 2 or space == 18 or space == 33:
                countLandSpace[space] += 1
                space = drawFromCommunityChest(countCCD,space,communityChestDeck)
                if space != 2 or space != 18 or space != 33:
                    countLandSpace[space] += 1
                    #graph[j][space] += 1
                elif space == 10:
                    inJail = True
                countCCD += 1
                countCCD, communityChestDeck = shuffleDeck(countCCD, communityChestDeck)
            # LANDING ON CHANCE SPACE
            elif space == 7 or space == 22 or space == 36:
                countLandSpace[space] += 1
                #graph[j][space] += 1
                space = drawFromChance(countCD,space,chanceDeck)
                if space != 7 or space != 22 or space != 36:
                    countLandSpace[space] += 1
                    #graph[j][space] += 1
                elif space == 10:
                    inJail = True
                countCD += 1
                countCD, chanceDeck = shuffleDeck(countCD, chanceDeck)
            else:
                countLandSpace[space] += 1
                #graph[j][space] += 1

#def nextTurn():

# PRINT RESULTS FROM GAMES #####################################################
def printResults(results, runs):
    gameProperty = ["                   GO",
                    " Mediterranean Avenue",
                    "      Community Chest",
                    "        Baltic Avenue",
                    "           Income Tax",
                    "     Reading Railroad",
                    "      Oriental Avenue",
                    "               Chance",
                    "       Vermont Avenue",
                    "   Connecticut Avenue",
                    "                 Jail",
                    "     St.Charles Place",
                    "     Electric Company",
                    "        States Avenue",
                    "      Virginia Avenue",
                    "Pennsylvania Railroad",
                    "       St.James Place",
                    "      Community Chest",
                    "     Tennessee Avenue",
                    "      New York Avenue",
                    "         Free Parking",
                    "      Kentucky Avenue",
                    "               Chance",
                    "       Indiana Avenue",
                    "      Illinois Avenue",
                    "         B&O Railroad",
                    "      Atlantic Avenue",
                    "       Ventnor Avenue",
                    "          Water Works",
                    "       Marvin Gardens",
                    "           Go to Jail",
                    "       Pacific Avenue",
                    "North Carolina Avenue",
                    "      Community Chest",
                    "  Pennsylvania Avenue",
                    "  Short Line Railroad",
                    "               Chance",
                    "           Park Place",
                    "           Luxury Tax",
                    "            Boardwalk"]

    j = 0
    sum = 0
    while j < 40:
        sum += (results[j] / runs)
        j += 1
    percentage = [0] * 40
    k = 0
    while k < 40:
        percentage[k] = float(float(float(results[k] / runs) / sum) * 100)
        k += 1
    print "MONOPOLY: 200 TIMES AROUND THE BOARD"
    i = 0
    while i < 40:
        print str(gameProperty[i]) + ":\t" + str(results[i]/runs) + "\t" + str("%.2f"%percentage[i]) + "%"
        i += 1
    print "CHANCE OF LANDING ON SPECIFIC MONOPOLIES"
    n = 0
    browns = 0.0
    lightBlues = 0.0
    purples = 0.0
    oranges = 0.0
    reds = 0.0
    yellows = 0.0
    greens = 0.0
    darkBlues = 0.0
    railRoads = 0.0
    utilities = 0.0
    chance = 0.0
    communitychest = 0.0
    while n < 40:
        if n == 1 or n == 3:
            browns += percentage[n]
        elif n == 6 or n == 8 or n == 9:
            lightBlues += percentage[n]
        elif n == 11 or n == 13 or n == 14:
            purples += percentage[n]
        elif n == 16 or n == 18 or n == 19:
            oranges += percentage[n]
        elif n == 21 or n == 23 or n == 24:
            reds += percentage[n]
        elif n == 26 or n == 27 or n == 29:
            yellows += percentage[n]
        elif n == 31 or n == 32 or n == 34:
            greens += percentage[n]
        elif n == 37 or n == 39:
            darkBlues += percentage[n]
        elif n == 5 or n == 15 or n == 25 or n == 35:
            railRoads += percentage[n]
        elif n == 12 or n == 28:
            utilities += percentage[n]
        elif n == 7 or n == 22 or n == 36:
            chance += percentage[n]
        elif n == 2 or n == 17 or n == 33:
            communitychest += percentage[n]
        n += 1

    print "       BROWN MONOPOLY:\t" + str("%.2f"%browns) + "%"
    print "  LIGHT BLUE MONOPOLY:\t" + str("%.2f"%lightBlues) + "%"
    print "      PURPLE MONOPOLY:\t" + str("%.2f"%purples) + "%"
    print "      ORANGE MONOPOLY:\t" + str("%.2f"%oranges) + "%"
    print "         RED MONOPOLY:\t" + str("%.2f"%reds) + "%"
    print "      YELLOW MONOPOLY:\t" + str("%.2f"%yellows) + "%"
    print "       GREEN MONOPOLY:\t" + str("%.2f"%greens) + "%"
    print "   DARK BLUE MONOPOLY:\t" + str("%.2f"%darkBlues) + "%"
    print "    RAILROAD MONOPOLY:\t" + str("%.2f"%railRoads) + "%"
    print "     UTILITY MONOPOLY:\t" + str("%.2f"%utilities) + "%"
    print "         CHANCE SPACE:\t" + str("%.2f"%chance) + "%"
    print "COMMUNITY CHEST SPACE:\t" + str("%.2f"%communitychest) + "%"

#def makeGraph(graph):
#    fig = go.Figure(go.Bar(x=x, y=[2,5,1,9], name='Montreal'))
#    fig.add_trace(go.Bar(x=x, y=[1, 4, 9, 16], name='Ottawa'))
#    fig.add_trace(go.Bar(x=x, y=[6, 8, 4.5, 8], name='Toronto'))
#
#    fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
#    fig.show()

################################################################################
if __name__ == '__main__':
    countLandSpace =[0] * 40
    again = 0
    passingGo = 35
    games = 100000
    players = 4
    #graph = [[0]*games] * 20
    #propertyAverage = [[0] * 40] * 20

    while again < games:
        newGame(countLandSpace,passingGo,players)
        again += 1
    graph = printResults(countLandSpace,games)
    #makeGraph(graph)
