# Name: Alec Andrews    
# CMS cluster login name: avandrew

'''
final_players.py

This module contains code for various bots that play Connect4 at varying 
degrees of sophistication.
'''

import random
from Connect4Simulator import *
# Any other imports go here...


class RandomPlayer:
    '''
    This player makes one of the possible moves on the game board,
    chosen at random.
    '''

    def chooseMove(self, board, player):
        '''
        Given the current board and player number, choose and return a move.

        Arguments:
          board  -- a Connect4Board instance
          player -- either 1 or 2

        Precondition: There must be at least one legal move.
        Invariant: The board state does not change.
        '''

        assert player in [1, 2]
        possibles = board.possibleMoves()
        assert possibles != []
        return random.choice(possibles)


class SimplePlayer:
    '''
    This player will always play a move that gives it a win if there is one.
    Otherwise, it picks a random legal move.
    '''

    def chooseMove(self, board, player):
        '''
        Given the current board and player number, choose and return a move.

        Arguments:
          board  -- a Connect4Board instance
          player -- either 1 or 2

        Precondition: There must be at least one legal move.
        Invariant: The board state does not change.
        '''
        
        assert player in [1, 2]
        possibles = board.possibleMoves()
        assert possibles != []
        for column in possibles:
            copy = board.clone()
            copy.makeMove(column, player)
            if copy.isWin(column) == True:
                return column
        return random.choice(possibles)


class BetterPlayer:
    '''
    This player will always play a move that gives it a win if there is one.
    Otherwise, it tries all moves, collects all the moves which don't allow
    the other player to win immediately, and picks one of those at random.
    If there is no such move, it picks a random move.
    '''

    def chooseMove(self, board, player):
        '''
        Given the current board and player number, choose and return a move.

        Arguments:
          board  -- a Connect4Board instance
          player -- either 1 or 2

        Precondition: There must be at least one legal move.
        Invariant: The board state does not change.
        '''

        assert player in [1, 2]
        possibles = board.possibleMoves()
        if player == 1:
            opponent = 2
        else:
            opponent = 1
        assert possibles != []
        if len(possibles) == 1:
            return possibles[0]
        lst = []
        lst2 = []
        for column in possibles:
            board1 = board.clone()
            board1.makeMove(column, player)          
            if board1.isWin(column) == True:
                return column 
            possibles1 = board1.possibleMoves()
            for move in possibles1:
                board2 = board1.clone()
                board2.makeMove(move, opponent)
                if board2.isWin(move) == True:
                    lst.append(column)
        for column in possibles:
            if column not in lst:
                lst2.append(column)
        if lst2 == []:
            return random.choice(possibles)
        return random.choice(lst2)
                
            

            
            
            


class Monty:
    '''
    This player will randomly simulate games for each possible move,
    picking the one that has the highest probability of success.
    '''

    def __init__(self, n, player):
        '''
        Initialize the player using a simpler computer player.

        Arguments: 
          n      -- number of games to simulate.
          player -- the computer player
        '''

        assert n > 0
        self.player = player
        self.n = n

    def chooseMove(self, board, player):
        '''
        Given the current board and player number, choose and return a move.

        Arguments:
          board  -- a Connect4Board instance
          player -- either 1 or 2

        Precondition: There must be at least one legal move.
        Invariant: The board state does not change.
        '''
        best = 0
        if player == 1:
            opponent = 2
        else:
            opponent = 1
        possibles = board.possibleMoves()
        top_move = possibles[0]
        for move in possibles:
            board_copy = board.clone()
            board_copy.makeMove(move, player)
            if board_copy.isWin(move) == True:
                return move
            else:
                wins = 0
                for n in range(self.n):
                    board_copy2 = board_copy.clone()
                    sim = Connect4Simulator(board_copy2, SimplePlayer(),
                                            SimplePlayer(), opponent)                    
                    result = sim.simulate()
                    if result == player:
                        wins += 1
                if wins > best:
                    best = wins
                    top_move = move
        return top_move

