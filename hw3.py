
from copy import deepcopy
from time import time
import random
import numpy as np

state = {
  "team-code": "eef8976e",
  "game": "connect_more",
  "opponent-name": "mighty_ducks",
  "columns": 6,
  "connect_n": 4,
  "your-token": "R",
  "board": [
    ["R"],
    ["R"],
    ["R"],
    [],
    [],
    ["Y"],
  ]
}


def printb(board):
  b = np.array(board).T.tolist()
  print(b)
  for a in b:
    print(a) 

def get_move(state):
# Your code can be called from here however you like
# You are allowed the use of load_data() and save_data(info)
  ####REPLACE######
  #info = load_data()
  info = state
  numColumns = info["columns"]
  numConnect_n = info["connect_n"]
  yourToken = info["your-token"]
  board = info["board"]

  A = AI(board,numColumns,numConnect_n,yourToken)

  printb(A.board)

"""
  while not A.gameIsOver(A.board):
    A.board = A.makeMove(A.board,A.bestMove(2,A.board,1),1)
    print(A.board)
    age = input("What is your column?")
    A.board = A.makeMove(A.board,int(age),0)
    print(A.board)



  # But you must return a valid move that looks like the following:
  return {
    "move": 2, # Column in which you will move (create mark "your-token")
    "team-code": "eef8976e" # Must match the code received in the state object
  }
  """

class AI(object): 
  board = None
  colors = []

  def __init__(self,board,numColumns,numConnect_n,yourToken): 
    self.board = [x[:] for x in board]
    self.columns = numColumns
    self.connectN = numConnect_n
    self.Token = yourToken
    self.colors = []
    self.colors.append(yourToken)

    #finds tokens for both players#
    for a in board:
      for b in a: 
        if not b == yourToken and not b in self.colors:
          self.colors.append(b)

  def bestMove(self, depth, state, curr_player):
        """ Returns the best move (as a column number) and the associated alpha
            Calls search()
        """
        # determine opponent's color
        if curr_player == 0:
            opp_player = 1
        else:
            opp_player = 0
        
        # enumerate all legal moves
        legal_moves = {} # will map legal move states to their alpha values
        for col in range(self.columns):
            # if column i is a legal move...
            # make the move in column 'col' for curr_player
            temp = self.makeMove(state, col, curr_player)
            legal_moves[col] = -self.search(depth-1, temp, opp_player)
        
        best_alpha = -99999999
        best_move = None
        moves = legal_moves.items()
        random.shuffle(list(moves))
        for move, alpha in moves:
            if alpha >= best_alpha:
                best_alpha = alpha
                best_move = move
        
        return best_move

  def search(self, depth, state, curr_player):
        """ Searches the tree at depth 'depth'
            By default, the state is the board, and curr_player is whomever 
            called this search
            
            Returns the alpha value
        """
        
        # enumerate all legal moves from this state
        legal_moves = []
        for i in range(self.columns):
            # if column i is a legal move...
            # make the move in column i for curr_player
            temp = self.makeMove(state, i, curr_player)
            legal_moves.append(temp)
        
        # if this node (state) is a terminal node or depth == 0...
        if depth == 0 or len(legal_moves) == 0 or self.gameIsOver(state):
            # return the heuristic value of node
            return self.value(state, curr_player)
        
        # determine opponent's color
        if curr_player == 0:
            opp_player = 1
        else:
            opp_player = 0

        alpha = -99999999
        for child in legal_moves:
            if child == None:
                print("child == None (search)")
            alpha = max(alpha, -self.search(depth-1, child, opp_player))
        return alpha

  def value(self, state, player):
        """ Simple heuristic to evaluate board configurations
            Heuristic is (num of 4-in-a-rows)*99999 + (num of 3-in-a-rows)*100 + 
            (num of 2-in-a-rows)*10 - (num of opponent 4-in-a-rows)*99999 - (num of opponent
            3-in-a-rows)*100 - (num of opponent 2-in-a-rows)*10
        """
        if player == 0:
            o_player = 1
        else:
            o_player = 0
        my_fours = self.checkForStreak(state, player, 4)
        my_threes = self.checkForStreak(state, player, 3)
        my_twos = self.checkForStreak(state, player, 2)
        opp_fours = self.checkForStreak(state, o_player, 4)
        opp_threes = self.checkForStreak(state, o_player, 3)
        opp_twos = self.checkForStreak(state, o_player, 2)
        if opp_fours > 0:
            return -100000
        else:
            return my_fours*10000 + my_threes*100 + my_twos - opp_fours*10000 - opp_threes*100 - opp_twos


  def makeMove(self, boardstate, column, player):
        """ Change a state object to reflect a player, denoted by color,
            making a move at column 'column'
            
            Returns a copy of new state array with the added move
        """
        temp = [x[:] for x in boardstate]
        temp[column].append(self.colors[player])
        return temp
  def gameIsOver(self, boardstate):
        if self.checkForStreak(boardstate, 0, self.connectN) >= 1:
            return True
        elif self.checkForStreak(boardstate, 1, self.connectN) >= 1:
            return True
        else:
            return False
  def checkForStreak(self, boardstate, player, streak):
        num = 0

        color = self.colors[player]
        # for each piece in the board...
        for i in range(self.columns):
            for j in range(len(boardstate[i])):
                # ...that is of the color we're looking for...
                if boardstate[i][j].lower() == color.lower():
                    # check if a vertical streak starts at (i, j)
                    num += self.verticalStreak(j, i, boardstate, streak)
                    
                    # check if a horizontal four-in-a-row starts at (i, j)
                    num += self.horizontalStreak(j, i, boardstate, streak)
                    
                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    num += self.diagonalCheck(j, i, boardstate, streak)
        # return the sum of streaks of length 'streak'

        return num
  def verticalStreak(self, row, col, boardstate, streak):
        consecutiveCount = 0
        fullheight = len(boardstate[col])

        for i in range(row,fullheight):
          if boardstate[col][i].lower() == boardstate[col][row].lower():
            consecutiveCount += 1
          else:
            break    
        if consecutiveCount >= streak:
            return 1
        else:
            return 0
  def horizontalStreak(self, row, col, boardstate, streak):
        consecutiveCount = 0
        for j in range(col,self.columns):
          if len(boardstate[j]) > row:
            if boardstate[j][row].lower() == boardstate[col][row].lower():
              consecutiveCount +=1
            else:
              break
        if consecutiveCount >= streak:
            return 1
        else:
            return 0
        return 0; 
  def diagonalCheck(self, row, col, boardstate, streak):

        total = 0
        # check for diagonals with positive slope
        consecutiveCount = 0
        i = row

        for j in range(col,self.columns):
          if ((len(boardstate[j])) <= i):
            break
          elif boardstate[j][i].lower() == boardstate[col][row].lower():
              consecutiveCount += 1
          else:
            break
          i +=1
        if consecutiveCount >= streak:
            total += 1
        
        consecutiveCount = 0
        i = row
        for j in range(col,self.columns):
          if ((len(boardstate[j])) <= i or i < 0):
            break
          elif boardstate[j][i].lower() == boardstate[col][row].lower():
              consecutiveCount += 1
          else:
            break
          i -=1
        if consecutiveCount >= streak:
            total += 1
        return total



class Minimax(object):
    """ Minimax object that takes a current connect four board state
    """
    
    board = None
    colors = ["x", "o"]
    
    def __init__(self, board):
        # copy the board to self.board
        self.board = [x[:] for x in board]
            
    def bestMove(self, depth, state, curr_player):
        """ Returns the best move (as a column number) and the associated alpha
            Calls search()
        """
        # determine opponent's color
        if curr_player == self.colors[0]:
            opp_player = self.colors[1]
        else:
            opp_player = self.colors[0]
        
        # enumerate all legal moves
        legal_moves = {} # will map legal move states to their alpha values
        for col in range(7):
            # if column i is a legal move...
            # make the move in column 'col' for curr_player
            temp = self.makeMove(state, col, curr_player)
            legal_moves[col] = -self.search(depth-1, temp, opp_player)
        
        best_alpha = -99999999
        best_move = None
        moves = legal_moves.items()
        random.shuffle(list(moves))
        for move, alpha in moves:
            if alpha >= best_alpha:
                best_alpha = alpha
                best_move = move
        
        return best_move, best_alpha
        
    def search(self, depth, state, curr_player):
        """ Searches the tree at depth 'depth'
            By default, the state is the board, and curr_player is whomever 
            called this search
            
            Returns the alpha value
        """
        
        # enumerate all legal moves from this state
        legal_moves = []
        for i in range(7):
            # if column i is a legal move...
            # make the move in column i for curr_player
            temp = self.makeMove(state, i, curr_player)
            legal_moves.append(temp)
        
        # if this node (state) is a terminal node or depth == 0...
        if depth == 0 or len(legal_moves) == 0 or self.gameIsOver(state):
            # return the heuristic value of node
            return self.value(state, curr_player)
        
        # determine opponent's color
        if curr_player == self.colors[0]:
            opp_player = self.colors[1]
        else:
            opp_player = self.colors[0]

        alpha = -99999999
        for child in legal_moves:
            if child == None:
                print("child == None (search)")
            alpha = max(alpha, -self.search(depth-1, child, opp_player))
        return alpha

    
    def gameIsOver(self, state):
        if self.checkForStreak(state, self.colors[0], 4) >= 1:
            return True
        elif self.checkForStreak(state, self.colors[1], 4) >= 1:
            return True
        else:
            return False
        
    
    def makeMove(self, state, column, color):
        """ Change a state object to reflect a player, denoted by color,
            making a move at column 'column'
            
            Returns a copy of new state array with the added move
        """
        
        temp = [x[:] for x in state]
        for i in range(6):
            if temp[i][column] == ' ':
                temp[i][column] = color
                return temp

    def value(self, state, color):
        """ Simple heuristic to evaluate board configurations
            Heuristic is (num of 4-in-a-rows)*99999 + (num of 3-in-a-rows)*100 + 
            (num of 2-in-a-rows)*10 - (num of opponent 4-in-a-rows)*99999 - (num of opponent
            3-in-a-rows)*100 - (num of opponent 2-in-a-rows)*10
        """
        if color == self.colors[0]:
            o_color = self.colors[1]
        else:
            o_color = self.colors[0]
        
        my_fours = self.checkForStreak(state, color, 4)
        my_threes = self.checkForStreak(state, color, 3)
        my_twos = self.checkForStreak(state, color, 2)
        opp_fours = self.checkForStreak(state, o_color, 4)
        #opp_threes = self.checkForStreak(state, o_color, 3)
        #opp_twos = self.checkForStreak(state, o_color, 2)
        if opp_fours > 0:
            return -100000
        else:
            return my_fours*100000 + my_threes*100 + my_twos
            
    def checkForStreak(self, state, color, streak):
        count = 0
        # for each piece in the board...
        for i in range(6):
            for j in range(7):
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
        for i in range(row, 6):
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
        for j in range(col, 7):
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
        for i in range(row, 6):
            if j > 6:
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
            if j > 6:
                break
            elif state[i][j].lower() == state[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1 # increment column when row is incremented

        if consecutiveCount >= streak:
            total += 1

        return total

get_move(state)