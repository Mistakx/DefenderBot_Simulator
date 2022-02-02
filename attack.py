#!/usr/bin/env pybricks-micropython
from threading import Thread


def printEnemyTypeAndHealth(gameInfo, enemyArrayPosition):

    enemy = gameInfo.enemySlots[enemyArrayPosition]

    if enemy == "Dead":
        print("Enemy health (Dead): " + str(0))

    else:
        print(
            "Enemy Type: "
            + enemy["type"]
            + " | "
            + "Enemy health: "
            + str(enemy["health"])
        )


# * Horn goes backwards until it is in a position to attack with the crane, then keeps attacking until the enemy falls.
def craneAttack(
    gameInfo,
    enemyToAttackArrayPosition,
):

    print("Starting attack - Crane.")

    currentEnemy = gameInfo.enemySlots[enemyToAttackArrayPosition]
    gameInfo.hornEnergy = gameInfo.hornEnergy - 300
    currentEnemy["health"] = currentEnemy["health"] - 200

    if currentEnemy["health"] <= 0:
        gameInfo.enemySlots[enemyToAttackArrayPosition] = "Dead"

    printEnemyTypeAndHealth(gameInfo, enemyToAttackArrayPosition)
    print("Crane attack used. New energy: " + str(gameInfo.hornEnergy))
    print()
    return


# * Horn headbutts the bottle and goes backwards
def headbutt(gameInfo, enemyToAttackArrayPosition):

    print("Starting attack - Headbutt.")

    enemyToAttack = gameInfo.enemySlots[enemyToAttackArrayPosition]

    gameInfo.hornEnergy = gameInfo.hornEnergy - 150
    enemyToAttack["health"] = enemyToAttack["health"] - 100

    if (enemyToAttack["health"]) <= 0:
        gameInfo.enemySlots[enemyToAttackArrayPosition] = "Dead"

    printEnemyTypeAndHealth(gameInfo, enemyToAttackArrayPosition)

    print("Headbutt attack used. New energy: " + str(gameInfo.hornEnergy))
    print()
    return


# * Horn plays a sound effect
def soundAttack(gameInfo, enemyToAttackArrayPosition):

    print("Starting attack - Sound.")

    enemyToAttack = gameInfo.enemySlots[enemyToAttackArrayPosition]

    gameInfo.hornEnergy = gameInfo.hornEnergy - 50
    enemyToAttack["health"] = enemyToAttack["health"] - 50

    if (enemyToAttack["health"]) <= 0:
        gameInfo.enemySlots[enemyToAttackArrayPosition] = "Dead"

    printEnemyTypeAndHealth(gameInfo, enemyToAttackArrayPosition)
    print("Sound attack used. New energy: " + str(gameInfo.hornEnergy))
    print()
