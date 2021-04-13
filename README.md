# MONOPOLY STATISTICAL VISUALIZATION
 A visualization of the game of monopoly, visualizing the not so random patterns that emerge from playing hundreds and thousands of games. This program recreated the movement rules of the game of Monopoly (subtracting the games economy), where you can have any number of players you desire, randomized Chance and Risk decks that shuffle after the end of each deck, and specify the number of times the players travel around go. These results will be printed to the console, and in later programs, generate a chart.
 ![Monopoly Board](/src/monopolyBoard.jpg)

 ## VERSION 1.0: Monopoly.py 
 Proof of concept that simply prints the results of X number of games with Y number of players, and passing go Z number of times. These variables can be manipulated to view the statistical likelyhood of landing on a particular space depending on the number of revolutions around the board. If you wish to manipulate these variables yourself, change the value of the numbers below.
	Line ..... Variable
	327 ...... passingGo = Z
	328 ...... games = X
	329 ...... players = Y
 The results will be printed to the console.

 ## VERSION 2.0: MonopolyV2.py
 In addition to the features listed above in version 1.0, version 2.0 includes a return on investment calculator (outside the normal contraints of the games economy). Additionally, streamlined some of the variable to make for easier manipulation.
 	Line ..... Variable
    386 ...... games = X
    387 ...... players = Y
    388 ...... passingGo = Z * players

 ## VERSION 3.0: MonopolyV3.py
