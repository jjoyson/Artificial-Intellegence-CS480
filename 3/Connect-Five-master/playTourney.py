from connect5 import *
from random import shuffle
import random
from A123456 import *
from A20349472 import *

def main():
    """ Play a tournament!
    """
    
    allPlayers = [A123456(),
                  A20349472()]


    brackets = setupBrackets(allPlayers)
    
    winner,log = playBrackets(brackets)
    print("Tournament:")
    for match in log:
        print("   {}".format(match))
    print("Overall tournament winner: {}!".format(winner.name))
    print("CONGRATULATIONS!")

def setupBrackets(playerList):
    if playerList is None:
        return None
    elif len(playerList) == 1:
        return [playerList[0],None]
    elif len(playerList) == 2:
        return playerList
    else:
        shuffle(playerList)
        halfpoint = int(len(playerList)/2)
        playerList1 = playerList[:halfpoint]
        playerList2 = playerList[halfpoint:]
        b1 = setupBrackets(playerList1)
        b2 = setupBrackets(playerList2)
        return [b1,b2]
    

def playBrackets(brackets):
    bracketLog = []
    if type(brackets) is list:
        p1,log1 = playBrackets(brackets[0])
        p2,log2 = playBrackets(brackets[1])
        if p1 is None:
            return p2,log2
        elif p2 is None:
            return p1,log1
        else:
            winner = playRound(p1,p2)
            log = []
            log.extend(log1)
            log.extend(log2)
            log.append("{} played {} and {} won".format(p1.name,p2.name,winner.name))
            return winner,log
    elif brackets is None:
        return None,[]
    else:
        return brackets,[]


roundLen = 3
def playRound(player1,player2,ifTieRandom=False):
    g = Game((player1,player2))
    g.printState()

    win_counts = [0, 0, 0] # [p1 wins, p2 wins, ties]
    for i in range(roundLen):
        if roundLen % 2 == 0:
            player1.setcolor("x")
            player2.setcolor("o")
        else:
            player1.setcolor("o")
            player2.setcolor("x")

        winner = g.playGame(printGameState=True)
        
        if winner == None:
            win_counts[2] += 1
            
        elif winner == player1:
            win_counts[0] += 1
            
        elif winner == player2:
            win_counts[1] += 1
            
    printStats(player1, player2, win_counts)
    if win_counts[0] > win_counts[1]:
        return player1
    elif win_counts[0] < win_counts[1]:
        return player2
    elif ifTieRandom:
        if random.randint(1, 2)==1:
            return player1
        else:
            return player2
    else:
        return playRound(player1,player2,True)


def printStats(player1, player2, win_counts):
    print("{0}: {1} wins, {2}: {3} wins, {4} ties".format(player1.name,
        win_counts[0], player2.name, win_counts[1], win_counts[2]))
        
if __name__ == "__main__": # Default "main method" idiom.
    main()
