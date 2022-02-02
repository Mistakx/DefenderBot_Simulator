# cesar.dias@olx.com
# Stand virtual, Imo virtual, Propria OLX
import random

import attack


#! Helper functions

# * There is still an enemy attacking next turn
def enemyIsAttackingNextTurn(gameInfo, enemyArrayPosition):
    enemy = gameInfo.enemySlots[enemyArrayPosition]
    return (
        (enemy != "")
        and (enemy != "No bottle")
        and (enemy != "Dead")
        and (enemy["n_attacks"] > 0)
    )

#! Game functions

# * Checks if the game isn't over
def gameIsStillOn(gameInfo):

    gameInfo.currentTurn += 1

    if gameInfo.currentTurn <= 6:

        #? print("Current turn: " + str(gameInfo.currentTurn))

        i = 0

        while i < 6:

            currentEnemy = gameInfo.enemySlots[i]

            if (currentEnemy == "") or (
                currentEnemy == "No bottle"
            ):  # Slot still hasn't had enemy, so the game is still on
                return True

            elif enemyIsAttackingNextTurn(gameInfo, i):
                return True

            i += 1
    
    #? print(gameInfo.enemySlots)
    return False

# * Horn regains 50% of it's current energy, never exceeding 500
def regainEnergy(gameInfo):

    #? print("Regaining energy.")

    gameInfo.hornEnergy = gameInfo.hornEnergy + 0.5 * gameInfo.hornEnergy
    if gameInfo.hornEnergy > 500:
        gameInfo.hornEnergy = 500

    #? print("Horn Energy:", gameInfo.hornEnergy)

# * Horn attacks the enemies according to the defined heuristics
def attackEnemies(gameInfo):

    # Detects if Horn needs to skip it's turn to regain energy
    def regainEnergyIfNecessary(gameInfo):

        if gameInfo.hornEnergy == 500:
            #? print("Horn has maximum energy, doesn't need to regain it.\n")
            return False

        elif (gameInfo.hornEnergy < 500) and (gameInfo.usingRemainingEnergy == True):
            #? print("Horn is is using it's remaining energy to attack.\n")
            return False

        elif (gameInfo.hornEnergy < 500) and (
            gameInfo.usingRemainingEnergy == False
        ):
            #? print("Horn is skipping it's turn to regain energy.\n")
            return True

    # If 4 enemies were killed or are out of attacks, crane attack the enemy on the board with more health
    def fourEnemiesKilled(gameInfo):

        # Counts the number of dead enemies
        numberOfDeadEnemies = 0
        i = 0
        while i < 6:
            currentEnemy = gameInfo.enemySlots[i]
            if currentEnemy == "Dead":
                numberOfDeadEnemies += 1
            i += 1

        # Counts the number of enemies out of attacks
        numberOfEnemiesOutOfAttacks = 0
        i = 0
        while i < 6:
            currentEnemy = gameInfo.enemySlots[i]
            if (
                (currentEnemy != "Dead")
                and (currentEnemy != "")
                and (currentEnemy != "No bottle")
                and (currentEnemy["n_attacks"] == 0)
            ):
                numberOfEnemiesOutOfAttacks += 1
            i += 1

        # Counts the number of enemies that are attacking next turn
        numberOfEnemiesAttackingNextTurn = 0
        i = 0
        while i < 6:
            currentEnemy = gameInfo.enemySlots[i]
            if enemyIsAttackingNextTurn(gameInfo, i):
                numberOfEnemiesAttackingNextTurn += 1
            i += 1

        #! If 4 enemies were killed or are out of attacks, crane attack the enemy on the board with more health if the board doesn't have two enemies with 50 health
        if ((numberOfDeadEnemies + numberOfEnemiesOutOfAttacks) >= 4) and (
            numberOfEnemiesAttackingNextTurn >= 1
        ):

            gameInfo.usingRemainingEnergy = True

            #? print("There are 4 dead or out of attack enemies. Using remaining energy.")
            #? print("Checking if a crane attack is viable.")

            # Counts the number of enemies alive that have 50 health
            numberOfEnemiesAttackingNextTurnWith50Health = 0
            i = 0
            while i < 6:
                currentEnemy = gameInfo.enemySlots[i]
                if enemyIsAttackingNextTurn(gameInfo, i) and (
                    currentEnemy["health"] == 50
                ):
                    numberOfEnemiesAttackingNextTurnWith50Health += 1
                i += 1

            #! If two enemies are attacking next turn and both have 50 life, Horn doesn't use the crane attack
            #! Using the crane attack in this situation would leave one of the enemies alive
            if numberOfEnemiesAttackingNextTurnWith50Health == 2:
                #? print(
                #     "There are 2 remaining enemies alive, but both have 50 health. Not using crane attack."
                # )
                return

            i = 0
            tempEnemyHealth = 0
            tempEnemyArrayPosition = 0

            # Changes temp variables to the variables corresponding to the enemy attacking next turn with more health
            while i < 6:

                currentEnemy = gameInfo.enemySlots[i]

                if (
                    enemyIsAttackingNextTurn(gameInfo, i)
                    and currentEnemy["health"] > tempEnemyHealth
                ):
                    tempEnemyHealth = currentEnemy["health"]
                    tempEnemyArrayPosition = i

                i += 1

            #? print(
            #     "Crane attacking remaining slot "
            #     + str(tempEnemyArrayPosition + 1)
            #     + ".\n"
            # )

            attack.craneAttack(
                gameInfo,
                tempEnemyArrayPosition,
            )
            gameInfo.alreadyAttackedThisTurn = True

    # If there are artilleries, sound attack them, and use the remaining energy to sound attack the remaining enemies
    def attackArtilleriesAndRemaining(gameInfo):

        #! Counts the number of artilleries
        numberOfArtilleriesReady = 0
        i = 0
        while i < 6:
            currentEnemy = gameInfo.enemySlots[i]
            if enemyIsAttackingNextTurn(gameInfo, i) and (
                currentEnemy["type"] == "Artillery"
            ):
                numberOfArtilleriesReady += 1
            i += 1

        #! Counts the number of non artilleries
        numberOfNonArtilleriesReady = 0
        i = 0
        while i < 6:
            currentEnemy = gameInfo.enemySlots[i]
            if enemyIsAttackingNextTurn(gameInfo, i) and (
                currentEnemy["type"] == "Infantry"
            ):
                numberOfNonArtilleriesReady += 1
            elif enemyIsAttackingNextTurn(gameInfo, i) and (
                currentEnemy["type"] == "Tank"
            ):
                numberOfNonArtilleriesReady += 1
            i += 1

        #! There are artilleries to attack this turn

        # Attacking with full energy
        if (numberOfArtilleriesReady >= 1) and (gameInfo.hornEnergy == 500):

            #? print("There are artilleries to attack. Attacking with full energy")

            # Horn can do up to 3 sound attacks per turn and still regain full energy.
            # The artilleries need to be prioritized, and always sound attacked attacked, regardless of energy.
            # If Horn has energy to attack all artilleries, and still sound attack one or more enemies, it sound attacks them.
            numberOfAttacksToNonArtilleries = (
                3 - numberOfArtilleriesReady
            )  # The number of non artilleries that can be sound attacked and still regain full energy
            numberOfNonArtilleriesAddedToArray = 0  # The number of non artilleries queued to be attacked the same turn as the artilleries
            slotsToSoundAttack = []

            #! Add non artilleries to be attacked to the array
            i = 0

            # Add to the array while:
            # Number of non artilleries added hasn't reached the number of attacks possible
            # Number of non artilleries added hasn't reached the number of total non artilleries in the board
            # TODO: Verify
            while (
                numberOfNonArtilleriesAddedToArray < numberOfAttacksToNonArtilleries
            ) and (numberOfNonArtilleriesAddedToArray < numberOfNonArtilleriesReady):
                currentEnemy = gameInfo.enemySlots[i]
                if enemyIsAttackingNextTurn(gameInfo, i) and (
                    currentEnemy["type"] != "Artillery"
                ):
                    # slotsToSoundAttack[numberOfNonArtilleriesAddedToArray] = i + 1
                    slotsToSoundAttack.append(i + 1)
                    #? print("Non Artillery queued to be attacked. Slot: " + str(i + 1))
                    numberOfNonArtilleriesAddedToArray += 1

                i += 1

            #! Added artilleries to be attacked to the array
            i = 0
            currentArrayIndex = numberOfNonArtilleriesAddedToArray
            while i < 6:

                currentEnemy = gameInfo.enemySlots[i]

                if enemyIsAttackingNextTurn(gameInfo, i) and (
                    currentEnemy["type"] == "Artillery"
                ):
                    # slotsToSoundAttack[currentArrayIndex] = i + 1
                    slotsToSoundAttack.append(i + 1)
                    #? print("Artillery queued to be attacked. Slot: " + str(i + 1))
                    currentArrayIndex += 1

                i += 1

            #? print()  # Space after the last artillery queued print

            #! Sort the array that contains the slots to attack, so they are attacked in the correct order
            slotsToSoundAttack.sort()

            #! Sound attack the queued enemies
            for slotToAttack in slotsToSoundAttack:

                attack.soundAttack(gameInfo, slotToAttack - 1)
                gameInfo.alreadyAttackedThisTurn = True

        elif (
            (numberOfArtilleriesReady >= 1)
            and (gameInfo.hornEnergy > 0)
            and (gameInfo.usingRemainingEnergy)
        ):

            #? print("There are artilleries to attack. Attacking with remaining energy.")

            # Horn can do up to 3 sound attacks per turn and still regain full energy.
            # The artilleries need to be prioritized, and always sound attacked attacked, regardless of energy.
            # If Horn has energy to attack all artilleries, and still sound attack one or more enemies, it sound attacks them.
            numberOfAttacksToNonArtilleries = (
                gameInfo.hornEnergy / 50
            ) - numberOfArtilleriesReady  # The number of non artilleries that can be sound attacked and still regain full energy
            numberOfNonArtilleriesAddedToArray = 0  # The number of non artilleries queued to be attacked the same turn as the artilleries
            slotsToSoundAttack = []

            #! Add non artilleries to be attacked to the array
            i = 0

            # Add to the array while:
            # Number of non artilleries added hasn't reached the number of attacks possible
            # Number of non artilleries added hasn't reached the number of total non artilleries in the board
            # TODO: Verify
            while (
                numberOfNonArtilleriesAddedToArray < numberOfAttacksToNonArtilleries
            ) and (numberOfNonArtilleriesAddedToArray < numberOfNonArtilleriesReady):

                currentEnemy = gameInfo.enemySlots[i]
                if enemyIsAttackingNextTurn(gameInfo, i) and (
                    currentEnemy["type"] != "Artillery"
                ):
                    # slotsToSoundAttack[numberOfNonArtilleriesAddedToArray] = i + 1
                    slotsToSoundAttack.append(i + 1)
                    #? print("Non Artillery queued to be attacked. Slot: " + str(i + 1))
                    numberOfNonArtilleriesAddedToArray += 1

                i += 1

            #! Added artilleries to be attacked to the array
            i = 0
            currentArrayIndex = numberOfNonArtilleriesAddedToArray
            while i < 6:

                currentEnemy = gameInfo.enemySlots[i]

                if enemyIsAttackingNextTurn(gameInfo, i) and (
                    currentEnemy["type"] == "Artillery"
                ):
                    # slotsToSoundAttack[currentArrayIndex] = i + 1
                    slotsToSoundAttack.append(i + 1)
                    #? print("Artillery queued to be attacked. Slot: " + str(i + 1))
                    currentArrayIndex += 1

                i += 1

            #? print()  # Space after the last artillery queued print

            #! Sort the array that contains the slots to attack, so they are attacked in the correct order
            slotsToSoundAttack.sort()

            #! Sound attack the queued enemies
            for slotToAttack in slotsToSoundAttack:

                attack.soundAttack(gameInfo, slotToAttack - 1)
                gameInfo.alreadyAttackedThisTurn = True

    # If there are 2 or more enemies, sound attack them until energy reaches 350
    def attackTwoOrMoreEnemies(gameInfo):

        #! Counts the number of enemies
        numberOfEnemies = 0
        i = 0
        while i < 6:
            currentEnemy = gameInfo.enemySlots[i]
            if enemyIsAttackingNextTurn(gameInfo, i):
                numberOfEnemies += 1
            i += 1

        # Attack with full energy
        if (numberOfEnemies >= 2) and (gameInfo.hornEnergy == 500):

            #? print("There are 2 or more enemies to attack. Attacking with full energy.")


            i = 0
            while i < 6:

                if gameInfo.hornEnergy > 350:


                    currentEnemy = gameInfo.enemySlots[i]

                    if enemyIsAttackingNextTurn(gameInfo, i):

                        attack.soundAttack(gameInfo, i)
                        gameInfo.alreadyAttackedThisTurn = True

                i += 1

        # Attack with remaining energy
        elif (
            (numberOfEnemies >= 2)
            and (gameInfo.hornEnergy > 0)
            and (gameInfo.usingRemainingEnergy)
        ):

            #? print(
            #     "There are 2 or more enemies to attack. Attacking with remaining energy."
            # )


            i = 0
            while i < 6:

                if gameInfo.hornEnergy > 0:


                    currentEnemy = gameInfo.enemySlots[i]

                    if enemyIsAttackingNextTurn(gameInfo, i):

                        attack.soundAttack(gameInfo, i)
                        gameInfo.alreadyAttackedThisTurn = True


                    i += 1

    # Attack an enemy if non of the other conditions apply
    def attackOneEnemy(gameInfo):

        #! Counts the number of enemies
        numberOfEnemies = 0
        i = 0
        while i < 6:
            currentEnemy = gameInfo.enemySlots[i]
            if enemyIsAttackingNextTurn(gameInfo, i):
                numberOfEnemies += 1
            i += 1

        # * Attack with full energy
        if (numberOfEnemies == 1) and (gameInfo.hornEnergy == 500):

            #? print("There is only 1 enemy. Attacking with full energy.")

            # Attack one enemy with 100 or more health
            i = 0
            while i < 6:

                currentEnemy = gameInfo.enemySlots[i]

                if enemyIsAttackingNextTurn(gameInfo, i) and (
                    currentEnemy["health"] >= 100
                ):
                    #? print("The enemy has 100 or more health.")
                    #? print("Headbutting slot " + str(i + 1) + ".")

                    attack.headbutt(
                        gameInfo,
                        i
                    )
                    gameInfo.alreadyAttackedThisTurn = True


                    return

                i += 1

            # Attack one enemy with 50 health
            i = 0
            while i < 6:

                currentEnemy = gameInfo.enemySlots[i]

                if enemyIsAttackingNextTurn(gameInfo, i) and (
                    currentEnemy["health"] == 50
                ):

                    #? print("The enemy has 50 health.")
                    #? print("Sound attacking slot " + str(i + 1) + ".\n")

                    attack.soundAttack(gameInfo, i)
                    gameInfo.alreadyAttackedThisTurn = True

                    return

                i += 1

        # * Attack with remaining energy
        elif (numberOfEnemies == 1) and (gameInfo.usingRemainingEnergy):

            print("There is only 1 enemy. Attacking with remaining energy.")

            # Attack one enemy with 100 or more health
            i = 0
            while i < 6:

                currentEnemy = gameInfo.enemySlots[i]

                if (
                    enemyIsAttackingNextTurn(gameInfo, i)
                    and (currentEnemy["health"] >= 100)
                    and (gameInfo.hornEnergy >= 150)
                ):
                    #? print("The enemy has 100 or more health.")
                    #? print("Headbutting slot " + str(i + 1) + ".")

                    attack.headbutt(
                        gameInfo,
                        i
                    )
                    gameInfo.alreadyAttackedThisTurn = True

                    return

                i += 1

            # Attack one enemy with 50 health
            i = 0
            while i < 6:

                currentEnemy = gameInfo.enemySlots[i]

                if (
                    enemyIsAttackingNextTurn(gameInfo, i)
                    and (currentEnemy["health"] == 50)
                    and (gameInfo.hornEnergy >= 50)
                ):

                    #? print("The enemy has 50 health.")
                    #? print("Sound attacking slot " + str(i + 1) + ".\n")
                    attack.soundAttack(gameInfo, i)
                    gameInfo.alreadyAttackedThisTurn = True
     
                    return

                i += 1

    if regainEnergyIfNecessary(gameInfo):
        return True
    gameInfo.alreadyAttackedThisTurn = False

    if gameInfo.alreadyAttackedThisTurn == False:
        fourEnemiesKilled(gameInfo)
    if gameInfo.alreadyAttackedThisTurn == False:
        attackArtilleriesAndRemaining(gameInfo)
    if gameInfo.alreadyAttackedThisTurn == False:
        attackTwoOrMoreEnemies(gameInfo)
    if gameInfo.alreadyAttackedThisTurn == False:
        attackOneEnemy(gameInfo)

    #! Counts the number of enemies dead or out of attacks
    numberOfDeadOrOutOfAttacksEnemies = 0
    i = 0
    while i < 6:
        currentEnemy = gameInfo.enemySlots[i]
        if currentEnemy == "Dead":
            numberOfDeadOrOutOfAttacksEnemies += 1
        elif (
            (currentEnemy != "")
            and (currentEnemy != "No bottle")
            and (currentEnemy["n_attacks"] == 0)
        ):
            numberOfDeadOrOutOfAttacksEnemies += 1

        i += 1

    if numberOfDeadOrOutOfAttacksEnemies == 6:
        return True

def enemiesAttack(gameInfo):

    i = 5
    while i >= 0:

        currentEnemy = gameInfo.enemySlots[i]

        # Horn goes to all alive enemies, with or without attacks left
        if (
            (currentEnemy != "")
            and (currentEnemy != "Dead")
            and (currentEnemy != "No bottle")
        ):


            # * Horn gets attacked
            # TODO: Different sound for each enemy
            if currentEnemy["n_attacks"] > 0:

                # Infantry gives as much damage as its health
                if currentEnemy["type"] == "Infantry":

                    gameInfo.hornHealth = (
                        gameInfo.hornHealth - currentEnemy["health"]
                    )
                    currentEnemy["n_attacks"] = currentEnemy["n_attacks"] - 1
                    #? print("Horn was attacked by infantry.\n")

                # Tank gives as much damage as its health
                if currentEnemy["type"] == "Tank":
                    gameInfo.hornHealth = (
                        gameInfo.hornHealth - currentEnemy["health"]
                    )
                    currentEnemy["n_attacks"] = currentEnemy["n_attacks"] - 1
                    #? print("Horn was attacked by tank.\n")

                # If artillery attacks, it always gives 500 damage
                elif currentEnemy["type"] == "Artillery":
                    gameInfo.hornHealth = gameInfo.hornHealth - 500
                    currentEnemy["n_attacks"] = currentEnemy["n_attacks"] - 1
                    #? print("Horn was attacked by artillery.\n")



                #? print("Horn Health:", gameInfo.hornHealth)
                # print()

                if gameInfo.hornHealth <= 0:
                    return True


        i -= 1

def playGame(gameInfo):

    while gameIsStillOn(gameInfo):

        if gameInfo.currentTurn == 1:
            for enemy in gameInfo.firstTurn:
                gameInfo.enemySlots[gameInfo.lastEnemySlotModified] = enemy
                gameInfo.lastEnemySlotModified += 1

        if gameInfo.currentTurn == 2:
            for enemy in gameInfo.secondTurn:
                gameInfo.enemySlots[gameInfo.lastEnemySlotModified] = enemy
                gameInfo.lastEnemySlotModified += 1

        if gameInfo.currentTurn == 3:
            for enemy in gameInfo.thirdTurn:
                gameInfo.enemySlots[gameInfo.lastEnemySlotModified] = enemy
                gameInfo.lastEnemySlotModified += 1
                
        if gameInfo.currentTurn == 4:
            for enemy in gameInfo.fourthTurn:
                gameInfo.enemySlots[gameInfo.lastEnemySlotModified] = enemy
                gameInfo.lastEnemySlotModified += 1

        if gameInfo.currentTurn == 5:
            for enemy in gameInfo.fifthTurn:
                gameInfo.enemySlots[gameInfo.lastEnemySlotModified] = enemy
                gameInfo.lastEnemySlotModified += 1

        if gameInfo.currentTurn == 6:
            for enemy in gameInfo.sixthTurn:
                gameInfo.enemySlots[gameInfo.lastEnemySlotModified] = enemy
                gameInfo.lastEnemySlotModified += 1


        #! Energy regain
        regainEnergy(gameInfo)
        #? print("Horn Health:", gameInfo.hornHealth)
        #? print()

        #! Horn attacks
        # * Finds if there are enemies to attack
        thereAreEnemiesToAttack = False
        i = 0
        while i < 6:

            currentEnemy = gameInfo.enemySlots[i]

            if enemyIsAttackingNextTurn(gameInfo, i):
                thereAreEnemiesToAttack = True
                break

            i += 1

        if thereAreEnemiesToAttack:
            #? print("There are enemies to attack.")
            if attackEnemies(gameInfo):
                return True


        #! Horn gets attacked
        # * Checks if there are enemies that will attack or warn Horn
        thereAreEnemiesThatAttackHorn = False
        i = 0
        while i < 6:

            currentEnemy = gameInfo.enemySlots[i]

            if enemyIsAttackingNextTurn(
                gameInfo, i
            ):  # Enemy is attacking horn next turn
                thereAreEnemiesThatAttackHorn = True

            i += 1

        if (
            thereAreEnemiesThatAttackHorn
        ):  #! Horn goes to be warned or attacked


            # print("Enemies started attacking and warning.")
            if enemiesAttack(gameInfo):
                return False

    return True