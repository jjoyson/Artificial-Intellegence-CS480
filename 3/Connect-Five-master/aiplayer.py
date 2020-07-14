import random
from player import Player
from connect5 import *
from options import *
import logging


class AlphaBeta(object):
    """ Minimax object that takes a current connect five board state
    """
    evaluated = 0
    board = None
    colors = ["x", "o"]
    
    def __init__(self, board):
        # copy the board to self.board
        self.board = [x[:] for x in board]
            
    def bestMove(self, evaluation, depth, state, curr_player, search):
        """ Returns the best move (as a column number) and the associated alpha
            Calls search()
        """
        alpha = -99999999
        beta = 99999999
        
        # determine opponent's color
        if curr_player == self.colors[0]:
            opp_player = self.colors[1]
        else:
            opp_player = self.colors[0]
        
        # enumerate all legal moves
        legal_moves = {} # will map legal move states to their alpha values
        for col in range(options.getCols()):
            # if column i is a legal move...
            if self.isLegalMove(col, state):
                # make the move in column 'col' for curr_player
                temp = self.makeMove(state, col, curr_player)
                if(search == "Minimax"):
                    legal_moves[col] = -self.search(evaluation, depth-1, temp, opp_player)
                else:
                    legal_moves[col] = -self.searchAlpha(evaluation, depth-1, temp, opp_player, alpha, beta)
        #log = logging
        log = logging.getLogger("Computer")
        log.info(curr_player)
        log1 = logging.getLogger("Evaluated")
        log1.info(self.evaluated)
        best_alpha = -99999999
        best_move = None
        moves = legal_moves.items()
        random.shuffle(list(moves))
        for move, alpha in moves:
            if alpha >= best_alpha:
                best_alpha = alpha
                best_move = move
        
        return best_move, best_alpha
        
    def search(self, evaluation, depth, state, curr_player):                                            # Minimax Search
        self.evaluated += 1
        """ Searches the tree at depth 'depth'
            By default, the state is the board, and curr_player is whomever 
            called this search
            
            Returns the alpha value
        """
        # enumerate all legal moves from this state
        legal_moves = []
        for i in range(options.getCols()):
            # if column i is a legal move...
            if self.isLegalMove(i, state):

                # make the move in column i for curr_player
                temp = self.makeMove(state, i, curr_player)
                legal_moves.append(temp)
        
        # if this node (state) is a terminal node or depth == 0...
        if depth == 0 or len(legal_moves) == 0 or self.gameIsOver(state):
            # return the heuristic value of node
            if(evaluation == "Basic"):
                return self.valueBase(state, curr_player)
            else:

                return self.value(state, curr_player)
        alpha = -999999
        # determine opponent's color
        if curr_player == self.colors[0]:
            opp_player = self.colors[1]
        else:
            opp_player = self.colors[0]

        for child in legal_moves:
            if child == None:
                print("child == None (search)")
            value = -self.search(evaluation, depth-1, child, opp_player)
            alpha = max(alpha, value)
        return alpha

    def searchAlpha(self, evaluation, depth, state, curr_player, alpha, beta):                      # Alpha Beta Search
        self.evaluated += 1
        """ Searches the tree at depth 'depth'
            By default, the state is the board, and curr_player is whomever 
            called this search
            
            Returns the alpha value
        """
        # enumerate all legal moves from this state
        legal_moves = []
        for i in range(options.getCols()):
            # if column i is a legal move...
            if self.isLegalMove(i, state):

                # make the move in column i for curr_player
                temp = self.makeMove(state, i, curr_player)
                legal_moves.append(temp)
        
        # if this node (state) is a terminal node or depth == 0...
        if depth == 0 or len(legal_moves) == 0 or self.gameIsOver(state):
            # return the heuristic value of node
            if(evaluation == "Basic"):
                return self.valueBase(state, curr_player)
            else:
                return self.value(state, curr_player)
        # alpha = -999999
        # determine opponent's color
        if curr_player == self.colors[0]:
            opp_player = self.colors[1]
        else:
            opp_player = self.colors[0]

        for child in legal_moves:
            if child == None:
                print("child == None (search)")
            value = -self.searchAlpha(evaluation, depth-1, child, opp_player, -beta, -alpha)    # Swap and negate alpha, beta
            alpha = max(alpha, value)   
            if alpha >= beta:                                                                   # Prune check
                return value
        return alpha

    def isLegalMove(self, column, state):
        """ Boolean function to check if a move (column) is a legal move
        """
        
        for i in range(options.getRows()):
            if state[i][column] == ' ':
                # once we find the first empty, we know it's a legal move
                return True
        
        # if we options.get here, the column is full
        return False
    
    def gameIsOver(self, state):
        if self.checkForStreak(state, self.colors[0], 5) >= 1:
            return True
        elif self.checkForStreak(state, self.colors[1], 5) >= 1:
            return True
        else:
            return False
        
    
    def makeMove(self, state, column, color):
        """ Change a state object to reflect a player, denoted by color,
            making a move at column 'column'
            
            Returns a copy of new state array with the added move
        """
        
        temp = [x[:] for x in state]
        for i in range(options.getRows()):
            if temp[i][column] == ' ':
                temp[i][column] = color
                return temp

    def value(self, state, color):
        """ Simple heuristic to evaluate board configurations
            Heuristic is (5-in-a-rows)*10000 + (4-in-a-rows)*100 + (3-in-a-rows)*10
            Or -10000 if opponent has any 5-in-a-rows
        """
        if color == self.colors[0]:
            o_color = self.colors[1]
        else:
            o_color = self.colors[0]
        mw = [10000,1000,10]
        ow = [100000,10000,100]

        my_fours = self.checkForStreak(state, color, 5)
        my_threes = self.checkForStreak(state, color, 4)
        my_twos = self.checkForStreak(state, color, 3)

        opp_fours = self.checkForStreak(state, o_color, 5)
        opp_threes = self.checkForStreak(state, o_color, 4)
        opp_twos = self.checkForStreak(state, o_color, 3)

        my_score = my_fours*mw[0] + my_threes*mw[1] + my_twos*mw[2]
        opp_score = opp_fours*ow[0] + opp_threes*ow[1] + opp_twos*ow[2]

        for i in range (len(state)):
            for j in range (len(state[i])):
                if(j == 0 or i == 7 or j == 8):
                    if( state[i][j] == color):
                        my_score += 20
                    if( state[i][j] == o_color):
                        opp_score += 20
                elif(j == 1 or i == 6 or j == 7):
                    if( state[i][j] == color):
                        my_score += 40
                    if( state[i][j] == o_color):
                        opp_score += 40
                elif(j == 2 or i == 5 or j == 6):
                    if( state[i][j] == color):
                        my_score += 60
                    if( state[i][j] == o_color):
                        opp_score += 60
                elif(j == 3 or i == 4 or j == 5):
                    if( state[i][j] == color):
                        my_score += 80
                    if( state[i][j] == o_color):
                        opp_score += 80
                else:
                    if( state[i][j] == color):
                        my_score += 100
                    if( state[i][j] == o_color):
                        opp_score += 100
            
        return my_score - opp_score

    def valueBase(self, state, color):
        """ Simple heuristic to evaluate board configurations
            Heuristic is (5-in-a-rows)*10000 + (4-in-a-rows)*100 + (3-in-a-rows)*10
            Or -10000 if opponent has any 5-in-a-rows
        """
        if color == self.colors[0]:
            o_color = self.colors[1]
        else:
            o_color = self.colors[0]
        
        my_fours = self.checkForStreak(state, color, 5)
        my_threes = self.checkForStreak(state, color, 4)
        my_twos = self.checkForStreak(state, color, 3)
        opp_fours = self.checkForStreak(state, o_color, 5)
        if opp_fours > 0:
            return -100000
        else:
            return my_fours*10000 + my_threes*100 + my_twos*10

    def checkForStreak(self, state, color, streak):
        count = 0
        # for each piece in the board...
        for i in range(options.getRows()):
            for j in range(options.getCols()):
                # ...that is of the color we're looking for...
                if state[i][j].lower() == color.lower():
                    # check if a vertical streak starts at (i, j)
                    count += self.verticalStreak(i, j, state, streak)
                    
                    # check if a horizontal four-in-a-row starts at (i, j)
                    count += self.horizontalStreak(i, j, state, streak)
                    
                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    count += self.diagonalCheck(i, j, state, streak)
        # return the sum of streaks of length 'streak'
        return count
            
    def verticalStreak(self, row, col, state, streak):
        consecutiveCount = 0
        for i in range(row, options.getRows()):
            if state[i][col].lower() == state[row][col].lower():
                consecutiveCount += 1
            else:
                break
    
        if consecutiveCount >= streak:
            return 1
        else:
            return 0
    
    def horizontalStreak(self, row, col, state, streak):
        consecutiveCount = 0
        for j in range(col, options.getCols()):
            if state[row][j].lower() == state[row][col].lower():
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= streak:
            return 1
        else:
            return 0
    
    def diagonalCheck(self, row, col, state, streak):

        total = 0
        # check for diagonals with positive slope
        consecutiveCount = 0
        j = col
        for i in range(row, options.getRows()):
            if j > options.getRows():
                break
            elif state[i][j].lower() == state[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1 # increment column when row is incremented
            
        if consecutiveCount >= streak:
            total += 1

        # check for diagonals with negative slope
        consecutiveCount = 0
        j = col
        for i in range(row, -1, -1):
            if j > options.getRows():
                break
            elif state[i][j].lower() == state[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1 # increment column when row is incremented

        if consecutiveCount >= streak:
            total += 1

        return total


class AIPlayer(Player):
    """ AIPlayer object that extends Player
        The AI algorithm is minimax, the difficulty parameter is the depth to which 
        the search tree is expanded.
    """
    
    difficulty = None
    def __init__(self, name, color, difficulty=5, search = "Minimax", evaluation = "Basic"):
        self.type = "AI"
        self.name = name
        self.color = color
        self.difficulty = difficulty
        self.search = search
        self.eval = evaluation
        
    def setcolor(self,color):
        self.color=color

    def move(self, state):
        print("{0}'s turn. {0} is {1}. {0} is using {2} search. {0} is using {3} eval function.".format(self.name, self.color, self.search, self.eval))
        
        # sleeping for about 1 second makes it looks like he's thinking
        #time.sleep(random.randrange(8, 17, 1)/10.0)
        #return random.randint(0, 6)
        
        m = AlphaBeta(state)
        best_move, value = m.bestMove(self.eval, self.difficulty, state, self.color, self.search)
        return best_move