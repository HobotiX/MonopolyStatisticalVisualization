import random
#import plotly.graph_objects as go
GO = 0
TOJAIL = 30
JAIL = 10
CHANCE01 = 7
CHANCE02 = 22
CHANCE03 = 36
COMMUNITYCHEST01 = 2
COMMUNITYCHEST02 = 18
COMMUNITYCHEST03 = 33

PROPERTY_ROI = [[-60,-50,2,4,10,30,90,160,250],
                [-60,-50,4,8,20,60,180,320,450],
                [-100,-50,6,12,30,90,270,400,550],
                [-100,-50,6,12,30,90,270,400,550],
                [-120,-50,8,16,40,100,300,460,600],
                [-140,-100,10,20,50,150,450,625,740],
                [-140,-100,10,20,50,150,450,625,740],
                [-160,-100,12,24,60,180,500,700,900],
                [-180,-100,14,28,70,200,550,750,950],
                [-180,-100,14,28,70,200,550,750,950],
                [-200,-100,16,32,80,220,600,800,1000],
                [-220,-150,18,36,90,250,700,875,1050],
                [-220,-150,18,36,90,250,700,875,1050],
                [-240,-150,20,40,100,300,750,925,1100],
                [-260,-150,22,44,110,330,800,975,1150],
                [-260,-150,22,44,110,330,800,975,1150],
                [-280,-150,24,48,120,360,850,1025,1200],
                [-300,-200,26,52,130,390,900,1100,1275],
                [-300,-200,26,52,130,390,900,1100,1275],
                [-320,-200,28,56,150,450,1000,1200,1400],
                [-350,-200,35,70,175,500,1100,1300,1500],
                [-400,-200,50,100,200,600,1400,1700,2000]]
RAILROAD_ROI = [[-200,25,50,100,200],
                [-200,25,50,100,200],
                [-200,25,50,100,200],
                [-200,25,50,100,200]]
UTILITY_ROI =  [[-150,28,70],
                [-150,28,70]]

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
def newGame(countLandSpace,passingGo,players):
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

    while lap < passingGo:
        # ROLL DICE
        move,doubles = roll()
        # DICE ROLLING RULES ################
        # ROLL DOUBLES
        if doubles == True:
            countDoubles += 1
            inJail = False
        # ROLL FOR DOUBLES IN JAIL
        elif inJail == True and jailRolls < 3:
            jailRolls += 1
            countDoubles = 0
        # STANDARD ROLL
        else:
            inJail = False
            jailRolls = 0
            countDoubles = 0
        
        #print "Player " + str(thisPlayer+1) + ": ROLLED "+ str(move) + " - CURRENT SPACE " + str(space[thisPlayer])

        # SPACE MOVEMENT RULES
        # CHECK IF PLAYER GOT 3 DOUBLES
        if countDoubles == 3:
            space[thisPlayer] = ToJail()
            #playerSpace[thisPlayer][space[thisPlayer]] += 1 
            countLandSpace[thisPlayer][space[thisPlayer]] += 1
            inJail = True
        # IF PLAYER CAN MOVE
        elif inJail == False:
            space[thisPlayer] += move
            #playerSpace[thisPlayer][space[thisPlayer]] += 1
            # PASSING GO
            space[thisPlayer],lap = passGo(space[thisPlayer],lap)
            
            # LAND ON GO TO JAIL ##############################################################################################
            if space[thisPlayer] == TOJAIL:
                countLandSpace[thisPlayer][space[thisPlayer]] += 1
                #graph[j][space] += 1
                space[thisPlayer] = ToJail()
                #playerSpace[thisPlayer][space[thisPlayer]] += 1 
                countLandSpace[thisPlayer][space[thisPlayer]] += 1
                #graph[j][space] += 1
                inJail = True
            # LANDING ON COMMUNITY CHEST SPACE #################################################################################
            elif space[thisPlayer] == COMMUNITYCHEST01 or space[thisPlayer] == COMMUNITYCHEST02 or space[thisPlayer] == COMMUNITYCHEST03:
                countLandSpace[thisPlayer][space[thisPlayer]] += 1
                space[thisPlayer] = drawFromCommunityChest(countCCD,space[thisPlayer],communityChestDeck)
                #playerSpace[thisPlayer][space[thisPlayer]] += 1 
                if space[thisPlayer] != COMMUNITYCHEST01 or space[thisPlayer] != COMMUNITYCHEST02 or space[thisPlayer] != COMMUNITYCHEST03:
                    countLandSpace[thisPlayer][space[thisPlayer]] += 1
                    #graph[j][space] += 1
                if space[thisPlayer] == JAIL:
                    inJail = True
                countCCD += 1
                countCCD, communityChestDeck = shuffleDeck(countCCD, communityChestDeck)
            # LANDING ON CHANCE SPACE #########################################################################################
            elif space[thisPlayer] == CHANCE01 or space[thisPlayer] == CHANCE02 or space[thisPlayer] == CHANCE03:
                countLandSpace[thisPlayer][space[thisPlayer]] += 1
                #graph[j][space] += 1
                space[thisPlayer] = drawFromChance(countCD,space[thisPlayer],chanceDeck)
                #playerSpace[thisPlayer][space[thisPlayer]] += 1 
                if space[thisPlayer] != CHANCE01 or space[thisPlayer] != CHANCE03 or space[thisPlayer] != CHANCE03:
                    countLandSpace[thisPlayer][space[thisPlayer]] += 1
                    #graph[j][space] += 1
                if space[thisPlayer] == JAIL:
                    inJail = True
                countCD += 1
                countCD, chanceDeck = shuffleDeck(countCD, chanceDeck)
            # LANDING ON NORMAL SPACE ##########################################################################################
            else:
                countLandSpace[thisPlayer][space[thisPlayer]] += 1
                #graph[j][space] += 1
        #print "thisPlayer: " + str(thisPlayer) + ", space: " + str(space[thisPlayer]) + ", sum: " + str(countLandSpace[thisPlayer][space[thisPlayer]])
        thisPlayer = playerTurnManager(thisPlayer,players,doubles)


#def nextthisPlayer():

# PRINT RESULTS FROM GAMES #####################################################
def printResults(results,runs,players,go):
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
    while j < players:
        print " - PLAYER: " + str(j+1) + " ------------------------------------------"
        k = 0
        sum = 0
        while k < 40:
            sum += (results[j][k] / runs)
            k += 1
        percentage = [0] * 40
        k = 0
        while k < 40:
            percentage[k] = float(float(float(results[j][k] / runs) / sum) * 100)
            k += 1
        print "MONOPOLY: " + str(go / players) + " TIMES AROUND THE BOARD"
        k = 0
        while k < 40:
            print str(gameProperty[k]) + ":\t" + str(results[j][k] / runs) + "\t" + str("%.2f"%percentage[k]) + "%"
            k += 1
        print "\nCHANCE OF LANDING ON SPECIFIC MONOPOLIES"
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
        print "COMMUNITY CHEST SPACE:\t" + str("%.2f"%communitychest) + "%\n"
        j += 1


#def makeGraph(graph):
#    fig = go.Figure(go.Bar(x=x, y=[2,5,1,9], name='Montreal'))
#    fig.add_trace(go.Bar(x=x, y=[1, 4, 9, 16], name='Ottawa'))
#    fig.add_trace(go.Bar(x=x, y=[6, 8, 4.5, 8], name='Toronto'))
#
#    fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
#    fig.show()

################################################################################
if __name__ == '__main__':
    again = 0
    
    games = 200
    players = 1
    passingGo = 200 * players
    
    #graph = [[0]*games] * 20
    #propertyAverage = [[0] * 40] * 20
    #countLandSpace = [[0] * 40] * players
    countLandSpace = [[0]*40 for _ in range(players)]
#    f = open("monopoly_network.edges", "a")


    while again < games:
        newGame(countLandSpace,passingGo,players)
        again += 1
    printResults(countLandSpace,games,players,passingGo)
    
    #makeGraph(graph)
