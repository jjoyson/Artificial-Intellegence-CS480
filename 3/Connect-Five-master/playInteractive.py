from connect5 import *
import logging

def main():
    """ Play a game!
    """
    logging.basicConfig(level=logging.DEBUG, filename="playInteractive.log")
    with open('playInteractive.log', 'w'):
        pass
    
    g = Game()
    g.printState()
    player1 = g.players[0]
    player2 = g.players[1]
    search = g.search
    
    win_counts = [0, 0, 0] # [p1 wins, p2 wins, ties]
    
    exit = False
    while not exit:
        while not g.finished:
            g.nextMove()
        
        g.findFives()
        g.printState()
        
        if g.winner == None:
            win_counts[2] += 1
        
        elif g.winner == player1:
            win_counts[0] += 1
            
        elif g.winner == player2:
            win_counts[1] += 1
        
        printStats(player1, player2, win_counts, search)
        
        while True:
            play_again = str(input("Would you like to play again? "))
            
            if play_again.lower() == 'y' or play_again.lower() == 'yes': 
                g.newGame()
                g.printState()
                break
            elif play_again.lower() == 'n' or play_again.lower() == 'no':
                print("Thanks for playing!")
                exit = True
                break
            else:
                print("I don't understand... "),
        
def printStats(player1, player2, win_counts, search):
    print("Search Type: {5} {0}: {1} wins, {2}: {3} wins, {4} ties".format(player1.name,
        win_counts[0], player2.name, win_counts[1], win_counts[2], search))
        
if __name__ == "__main__": # Default "main method" idiom.
    main()