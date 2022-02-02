#!/usr/bin/env pybricks-micropython
import random 
import attack
import game
import time

#! Initialization

class Game:

    def __init__(self):

        self.currentTurn = 0
        self.hornHealth = 750
        self.hornEnergy = 500
        self.enemySlots = ["","","","","",""]
        self.usingRemainingEnergy = False
        self.alreadyAttackedThisTurn = True
        self.firstTurn = []
        self.secondTurn = []
        self.thirdTurn = []
        self.fourthTurn = []
        self.fifthTurn = []
        self.sixthTurn = []
        self.lastEnemySlotModified = 0

totalGames = 0
gamesWon = 0

for x in range(100):

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
            (gameInfo.sixthTurn).append(randomEnemies[x])


    # time.sleep(1)

    #! Play game
    if game.playGame(gameInfo):
        gamesWon += 1
    totalGames += 1
    

print("totalGames:", totalGames)
print("gamesWon:", gamesWon)
print("SANDRA:", gamesWon/totalGames)


# TODO: If there is only one enemy that can be left, scan it and immediately attack it.
# TODO: Horn wins at the exact same moment of the attack.
