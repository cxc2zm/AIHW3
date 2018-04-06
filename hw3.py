
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
    [],
    [],
    [],
    [],
    [],
    [],
  ]
}


def printb(board):
  for a in board:
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



  print(A.finished(A.board))
  print("run")
  while not A.finished(A.board):
    print("opponent move")
    A.board = A.colMove(A.board,A.optimalmove(5,A.board,1),1)
    printb(A.board)
    age = input("What is your column?")
    A.board = A.colMove(A.board,int(age),0)
    printb(A.board)



  # But you must return a valid move that looks like the following:
  return {
    "move": A.optimalmove(5,A.board,0), # Column in which you will move (create mark "your-token")
    "team-code": info["team-code"] # Must match the code received in the state object
  }


class AI(object): 

  def __init__(self,board,numColumns,numConnect_n,yourToken): 
    self.board = [x[:] for x in board]
    self.columns = numColumns
    self.connectN = numConnect_n
    self.Token = yourToken
    self.playerTokens = []
    self.playerTokens.append(yourToken)

    for a in board:
      for b in a: 
        if not b == yourToken and not b in self.playerTokens:
          self.playerTokens.append(b)

    if(len(self.playerTokens) == 1):
      self.playerTokens.append("@")

  def optimalmove(self, level, boardstate, player):

        if player == 0:
            opponent = 1
        else:
            opponent = 0
        
        moves = {} # will map legal move states to their alpha heuristicVals
        for col in range(self.columns):
            # if column i is a legal move...
            # make the move in column 'col' for curr_player
            temp = self.colMove(boardstate, col, player)
            moves[col] = -self.breadthSearch(level-1, temp, opponent)
        
        optVal = -999999
        optMove = None
        moves = moves.items()
        random.shuffle(list(moves))
        for move, val in moves:
            if val >= optVal:
                optVal = val
                optMove = move
        
        return optMove

  def breadthSearch(self, level, boardstate, player):
        """ Searches the tree at depth 'depth'
            By default, the state is the board, and curr_player is whomever 
            called this search
            
            Returns the alpha heuristicVal
        """
        
        # enumerate all legal moves from this state
        moves = []
        for i in range(self.columns):
            # if column i is a legal move...
            # make the move in column i for curr_player
            temp = self.colMove(boardstate, i, player)
            moves.append(temp)
        
        # if this node (state) is a terminal node or depth == 0...
        if level == 0 or len(moves) == 0 or self.finished(boardstate):
            # return the heuristic heuristicVal of node
            return self.heuristicVal(boardstate, player)
        
        # determine opponent's color
        if player == 0:
            opponent = 1
        else:
            opponent = 0

        alpha = -99999999
        for child in moves:
            if child == None:
                print("child == None (breadthSearch)")
            alpha = max(alpha, -self.breadthSearch(level-1, child, opponent))
        return alpha

  def heuristicVal(self, boardstate, player):
        """ Simple heuristic to evaluate board configurations
            Heuristic is (num of 4-in-a-rows)*99999 + (num of 3-in-a-rows)*100 + 
            (num of 2-in-a-rows)*10 - (num of opponent 4-in-a-rows)*99999 - (num of opponent
            3-in-a-rows)*100 - (num of opponent 2-in-a-rows)*10
        """
        if player == 0:
            opponent = 1
        else:
            opponent = 0

        mysum = 0; 
        for i in range(2,self.connectN):
          mysum += self.numInARow(boardstate, player, i)*(10**i)
          mysum -= self.numInARow(boardstate, opponent, i)*(10**i)

        if(self.numInARow(boardstate, player, self.connectN) > 0):
          return -1000000000
        else:
          return mysum

  def colMove(self, boardstate, column, player):
        """ Change a state object to reflect a player, denoted by color,
            making a move at column 'column'
            
            Returns a copy of new state array with the added move
        """
        temp = [x[:] for x in boardstate]
        temp[column].append(self.playerTokens[player])
        return temp
  def finished(self, boardstate):
        if self.numInARow(boardstate, 0, self.connectN) >= 1:
            return True
        elif self.numInARow(boardstate, 1, self.connectN) >= 1:
            return True
        else:
            return False
  def numInARow(self, boardstate, player, streak):
        num = 0

        color = self.playerTokens[player]
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
get_move(state)