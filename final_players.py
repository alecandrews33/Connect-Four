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

        # Gather a list of the possible moves and pick one randomly.
        assert player in [1, 2]
        possible_moves = board.possibleMoves()
        assert possible_moves != []
        return random.choice(possible_moves)


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
        
        # Get the possible moves, and see if any of them would 
        # result in a win. 
        assert player in [1, 2]
        possible_moves = board.possibleMoves()
        assert possible_moves != []
        for column in possible_moves:
            # Create a copy of the board to try each move 
            # without changing board state.
            copy = board.clone()
            copy.makeMove(column, player)
            # If a move would yield a win, take that move.
            if copy.isWin(column) == True:
                return column 
        # If no moves yield a win, then pick a random move.
        return random.choice(possible_moves)


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
        possible_moves = board.possibleMoves()
        # Find the opponent.
        if player == 1:
            opponent = 2
        else:
            opponent = 1
        assert possible_moves != []
        # If only one available move, take it.
        if len(possible_moves) == 1:
            return possible_moves[0]
        opponent_winners = []
        # Look through possible moves and find which ones 
        # give the opponent an opportunity to win.
        for column in possible_moves:
            copy = board.clone()
            copy.makeMove(column, player) 
            # If a move yields a win, take that move.         
            if copy.isWin(column) == True:
                return column 
            # See what moves the opponent will have 
            # available to them after your move.
            next_moves = copy.possibleMoves()
            for move in next_moves:
                next_copy = copy.clone()
                next_copy.makeMove(move, opponent)
                # If the opponent has a chance to win 
                # after this move, then add it to the
                # opponent winners list and stop looking 
                # at the opponent's moves.
                if next_copy.isWin(move) == True:
                    opponent_winners.append(column)
                    break
        # If all moves allow the opponent a chance to win, 
        # pick a random one.
        if opponent_winners == possible_moves:
            return random.choice(possible_moves)
        # Otherwise, get a list of the moves that don't 
        # allow the opponent to win, and choose a random 
        # move from that list.
        else:
            opponent_blockers = []
            for move in possible_moves:
                if move not in opponent_winners:
                    opponent_blockers.append(move)
            return random.choice(opponent_blockers)

                
            

            
            
            


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

        # Establish the highest number of wins and set the opponent.
        # Choose the first move as the initial best move.
        best = 0
        if player == 1:
            opponent = 2
        else:
            opponent = 1
        possible_moves = board.possibleMoves()
        top_move = possible_moves[0]
        # For each possible move, make the move on a copy of the board.
        for move in possible_moves:
            copy = board.clone()
            copy.makeMove(move, player)
            # If a move would yield a win, take that move.
            if copy.isWin(move) == True:
                return move
            # Otherwise, initialize the number of wins to 0 and 
            # simulate the number of games that were already 
            # defined using simple players on both sides.
            else:
                wins = 0
                for n in range(self.n):
                    copy2 = copy.clone()
                    sim = Connect4Simulator(copy2, SimplePlayer(),
                                            SimplePlayer(), opponent)                    
                    result = sim.simulate()
                    # Keep track of how many simulated wins the player has
                    # after making the current move.
                    if result == player:
                        wins += 1
                # If this move yielded more simulated wins than what was 
                # previously the best, set it as the top move, and keep 
                # track of how many wins it had.
                if wins > best:
                    best = wins
                    top_move = move
        # Return the top move that won the most simulated games.
        return top_move

