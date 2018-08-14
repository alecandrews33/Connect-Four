# Name: Alec Andrews
# CMS cluster login name: avandrew

'''
final_board.py

This module contains classes that implement the Connect-4 board object.
'''

# Imports go here...
from copy import deepcopy

class MoveError(Exception):
    '''
    Instances of this class are exceptions which are raised when
    an invalid move is made.
    '''
    pass

class BoardError(Exception):
    '''
    Instances of this class are exceptions which are raised when
    some erroneous condition relating to a Connect-Four board occurs.
    '''
    pass

class Connect4Board:
    '''
    Instance of this class manage a Connect-Four board, but do not
    manage the play of the game itself.
    '''

    def __init__(self):
        '''
        Initialize the board.
        '''
        self.board = []
        for e in range(6):
            row = []
            for i in range(7):
                row.append(0)
            self.board.append(row)
        self.rows = 6
        self.columns = 7
        self.moves = []

    def getRows(self):
        '''
        Return the number of rows.
        '''

        return self.rows

    def getCols(self):
        '''
        Return the number of columns.
        '''

        return self.columns

    def get(self, row, col):
        '''
        Arguments:
          row -- a valid row index
          col -- a valid column index

        Return value: the board value at (row, col).

        Raise a BoardError exception if the 'row' or 'col' value is invalid.
        '''
        
        if row < 0 or row > 5:
            raise BoardError("The row value is invalid")
        if col < 0 or col > 6:
            raise BoardError("The column value is invalid")
        else:
            return self.board[row][col]

    def clone(self):
        '''
        Return a clone of this board i.e. a new instance of this class
        such that changing the fields of the new instance will not
        affect the old instance.

        Return value: the new Connect4Board instance.
        '''

        return deepcopy(self)

    def possibleMoves(self):
        '''
        Compute the list of possible moves (i.e. a list of column numbers 
        corresponding to the columns which are not completely filled up).

        Return value: the list of possible moves
        '''
        open_columns = []
        for column in range(7):
            # Check the top row to determine if a piece can be played in a 
            # given column. If this row is empty, the column is available.
            if self.board[5][column] == 0:
                open_columns.append(column)
        return open_columns

    def makeMove(self, col, player):
        '''
        Make a move on the specified column for the specified player.

        Arguments:
          col    -- a valid column index
          player -- either 1 or 2

        Return value: none

        Raise a MoveError exception if a move cannot be made because the column
        is filled up, or if the column index or player number is invalid.
        '''

        if player != 1 and player != 2:
            raise MoveError("There are only two players, 1 and 2.")        
        if col < 0 or col > self.columns :
            raise MoveError("This is an invalid column value.")
        moves = self.possibleMoves() 
        if col not in moves:
            raise MoveError("That column is full.")
        
        # Find the highest open row in the given column and place piece.
        for row in range(0, 6):
            if self.get(row, col) == 0:
                self.board[row][col] = player
                self.moves.append((row, col))
                break
            
                

    def unmakeMove(self, col):
        '''
        Unmake the last move made on the specified column.

        Arguments:
          col -- a valid column index

        Return value: none

        Raise a MoveError exception if there is no move to unmake, or if the
        column index is invalid.
        '''

        if col < 0 or col > 6:
            raise MoveError("This is an invalid column value.")
        if self.board[0][col] == 0:
            raise MoveError("You cannot undo a move from an empty column.")

        # Find the highest piece in the given column and remove it.
        for row in range(5, -1, -1):
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                break

        # Remove the most recent move.
        self.moves.pop()
            
    def vertWin(self, col):
        '''This method checks to see if a win has been achieved in the vertical
        direction.'''

        # A win would only come from the last move. 
        last = self.moves[-1]
        row = last[0]

        # A vertical win would require a piece to be in the 4th highest row.
        if row >= 3:
            # Check if the last four pieces placed in the given column
            # are from the same team.
            for n in range(1,4):
                if self.get(row - n, col) != self.get(row, col):
                    # Any difference in this set of 4 would not result 
                    # in a win.
                    return False
            # 4 consecutive vertical pieces from the same team results
            # in a win.
            return True
        else:
            return False
   
    def horizWin(self, col):
        '''This method checks to see if a win has been achieved in the 
        horizontal direction.'''

        # A win could only result from the most recent move.
        last = self.moves[-1]
        row = last[0]
        value = self.get(row, col)
        columns = 0

        # Find how many consecutive columns to the right of the given 
        # column have the same value (are from the same team). Return 
        # a win if there are 3 (the fourth is given).   
        for n in range (1, 4):
            if col + n < 7:
                if self.get(row, col + n) == value:
                    columns += 1
                    if columns == 3:
                        return True
                else: 
                    break
            else:
                break
        
        # Keep adding to the column total by checking the columns
        # to the left of the given column. If they have the same 
        # value as the given column, increment the columns counter.
        # Return a win if there are 3 (the fourth is given).
        for n in range(1, 4):
            if col - n >= 0:
                if self.get(row, col - n) == value:
                    columns += 1
                    if columns == 3:
                        return True
                else: 
                    break
            else:
                break
        
        
        
    def diagWin(self,col):
        '''This helper function checks to see if four same-colored tiles were
        placed consecutively along a diagonal.'''

        # A win could only have resulted from the last move.
        last = self.moves[-1]
        row = last[0]
        value = self.get(row, col)
        pieces = 0

        # See how many consecutive pieces going from bottom left to the top 
        # right are of the same value as the last played piece.
        for n in range(1, 4):
            new_row = row + n
            new_col = col + n            
            if new_row <= self.rows - 1 and new_col <= self.columns - 1:
                if self.get(new_row, new_col) == value:
                    pieces += 1
                else: 
                    break
            else:
                break
        for n in range(1, 4):
            new_row = row - n
            new_col = col - n            
            if new_row >= 0 and new_col >= 0:
                if self.get(new_row, new_col) == value:
                    pieces += 1
                else: 
                    break
            else: 
                break

        # If at least 3 other pieces are found of the same value
        # in this diagonal direction, then return true. Otherwise,
        # reset the piece counter and check for a diagonal win 
        # in the other direction (top left to bottom right).
        if pieces >= 3:
            return True
        tiles = 0
        for n in range(1, 4):
            new_row = row + n
            new_col = col - n
            if new_row <=  self.rows - 1 and new_col >= 0:
                if self.get(new_row, new_col) == value:
                    tiles += 1
                else:
                    break
            else:
                break
        for n in range(1, 4):
            new_row = row - n
            new_col = col + n
            if new_row >= 0 and new_col <= self.columns - 1:
                if self.get(new_row, new_col) == value:
                    tiles += 1
                else: 
                    break
            else:
                break

        # If at least 3 other pieces are found of the same value
        # in this diagonal direction, then return true. Otherwise,
        # return false as no diagonal win has been found.
        if tiles >= 3:
            return True
        else:
            return False
        
            
            
             
        
                
        

    def isWin(self, col):
        '''
        Check to see if the last move played in column 'col' resulted in a win
        (four or more discs of the same color in a row in any direction).

        Argument: 
          col    -- a valid column index

        Return value: True if there is a win, else False

        Raise a BoardError exception if the column is empty (i.e. no move has
        ever been made in the column), or if the column index is invalid.
        '''

        if col < 0 or col > 6 :
            raise MoveError("This is an invalid column value.")
        if self.board[0][col] == 0:
            raise MoveError("This column is empty")
        if self.vertWin(col) == True:
            return True
        if self.horizWin(col) == True:
            return True 
        if self.diagWin(col) == True:
            return True
        return False

    def isDraw(self):
        '''
        Check to see if the board is a draw because there are no more
        columns to play in.

        Precondition: This assumes that there is no win on the board.

        Return value: True if there is a draw, else False
        '''

        if self.possibleMoves() == []:
            return True
        return False

    def isWinningMove(self, col, player):
        '''
        Check to see if making the move 'col' by the player 'player'
        would result in a win.  The board state does not change.

        Arguments:
          col    -- a valid column index
          player -- either 1 or 2

        Return value: True if the move would result in a win, else False.

        Precondition: This assumes that the move can be made.
        '''

        # Make the move on a copy of the board and see if it results
        # in a win.
        copy = self.clone()
        copy.makeMove(col, player)
        if copy.isWin(col) == True:
            return True
        return False

    def isDrawingMove(self, col, player):
        '''
        Check to see if making the move 'col' by the player 'player'
        would result in a draw.  The board state does not change.

        Arguments:
          col    -- a valid column index
          player -- either 1 or 2

        Return value: True if the move would result in a draw, else False.

        Precondition: This assumes that the move can be made, and that the
        move has been checked to see that it does not result in a win.
        '''
        
        # Make the move on a copy of the board and see if it results 
        # in a draw.
        copy = self.clone()
        copy.makeMove(col, player)
        if copy.isDraw() == True:
            return True
        return False
