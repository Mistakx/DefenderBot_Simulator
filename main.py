#!/usr/bin/env pybricks-micropython
import random 
import attack
import game


#! Initialization

class Game:
    currentTurn = 0
    hornHealth = 750
    hornEnergy = 500
    enemySlots = []
    usingRemainingEnergy = False
    alreadyAttackedThisTurn = True
    firstTurn = []
    secondTurn = []
    thirdTurn = []
    fourthTurn = []
    fifthTurn = []
    sixthTurn = []

totalGames = 0
gamesWon = 0

for x in range(1):

    gameInfo = Game()

    #! Generate enemies
    randomEnemies = []
    for x in range(6):
        randomNumber = random.randint(1,6)
        if (randomNumber == 1 or randomNumber == 2): # Tank

            tank = {
                "type": "Tank",
                "n_attacks": 2,
                "health": 200,
            }
            randomEnemies.append(tank)
        if (randomNumber == 3 or randomNumber == 4): # Artillery

            artillery = {
                "type": "Artillery",
                "strength": 500,
                "n_attacks": 1,
                "health": 50,
            }
            randomEnemies.append(artillery)
        if (randomNumber == 5 or randomNumber == 6): # Infantry

            infantry = {
                "type": "Infantry",
                "n_attacks": 3,
                "health": 100,
            }
            randomEnemies.append(infantry)

    #! Generate turns for the enemies
    for x in range(6):
        randomNumber = random.randint(1,6)
        if randomNumber == 1:
            (gameInfo.firstTurn).append(randomEnemies[x])

        if randomNumber == 2:
            (gameInfo.secondTurn).append(randomEnemies[x])

        if randomNumber == 3:
            (gameInfo.thirdTurn).append(randomEnemies[x])

        if randomNumber == 4:
            (gameInfo.fourthTurn).append(randomEnemies[x])

        if randomNumber == 5:
            (gameInfo.fifthTurn).append(randomEnemies[x])

        if randomNumber == 6:
            (gameInfo.thirdTurn).append(randomEnemies[x])


    # print("First turn:")
    # print(gameInfo.firstTurn)
    # print("Second turn:")
    # print(gameInfo.secondTurn)
    # print("Third turn:")
    # print(gameInfo.thirdTurn)
    # print("Fourth turn:")
    # print(gameInfo.fourthTurn)
    # print("Fifth turn:")
    # print(gameInfo.fifthTurn)
    # print("Sixth turn:")
    # print(gameInfo.sixthTurn)

    #! Play game
    if game.playGame(gameInfo):
        gamesWon += 1
        totalGames += 1

print("totalGames:", totalGames)
print("gamesWon:", gamesWon)

# TODO: If there is only one enemy that can be left, scan it and immediately attack it.
# TODO: Horn wins at the exact same moment of the attack.
