'''
cchen025_KInARow.py
Authors: Wu, Tony; Chen, Castor

An agent for playing "K-in-a-Row with Forbidden Squares" and related games.
CSE 473, University of Washington

THIS IS A TEMPLATE WITH STUBS FOR THE REQUIRED FUNCTIONS.
YOU CAN ADD WHATEVER ADDITIONAL FUNCTIONS YOU NEED IN ORDER
TO PROVIDE A GOOD STRUCTURE FOR YOUR IMPLEMENTATION.

'''

from agent_base import KAgent
from game_types import State, Game_Type

AUTHORS = 'Tony Wu and Castor Chen' 

import time # You'll probably need this to avoid losing a
 # game due to exceeding a time limit.

# Create your own type of agent by subclassing KAgent:

class OurAgent(KAgent):  # Keep the class name "OurAgent" so a game master
    # knows how to instantiate your agent class.

    def __init__(self, twin=False):
        self.twin=twin
        self.nickname = 'Yoda'
        if twin: self.nickname += '2'
        self.long_name = 'Jedi Master Yoda'
        self.persona = 'Wise'
        if twin: 
            self.long_name += '\'s Sith Clone'
            self.persona = 'Cunning'
        self.voice_info = {'Chrome': 10, 'Firefox': 2, 'other': 0}
        self.playing = "" # e.g., "X" or "O".

    def introduce(self):
        intro = '\nYoda, my name is. Jedi Master, I am. \n'+\
            'Made me, Castor and Tony did. \n'+\
            'Use the force to win, I will. \n'
        if self.twin: intro = "Evil Yoda Sith Clone, I am.\n A Jedi Master, I am not.\n Obliterate you, I will.\n"
        return intro

    # Receive and acknowledge information about the game from
    # the game master:
    def prepare(
        self,
        game_type,
        what_side_to_play,
        opponent_nickname,
        expected_time_per_move = 0.1, # Time limits can be
                                      # changed mid-game by the game master.
        utterances_matter=True):      # If False, just return 'OK' for each utterance.

        # Write code to save the relevant information in variables
        # local to this instance of the agent.
        # Game-type info can be in global variables.
        self.game_type = game_type
        self.what_side_to_play = what_side_to_play
        self.opponent_nickname = opponent_nickname
        self.expected_time_per_move = expected_time_per_move
        self.utterances_matter = utterances_matter
        return "Not-OK"
   
    # The core of your agent's ability should be implemented here:             
    def makeMove(self, currentState, currentRemark, timeLimit=10000):
        print("makeMove has been called")

        print("code to compute a good move should go here.")
        # Here's a placeholder:
        a_default_move = [0, 0] # This might be legal ONCE in a game,
        # if the square is not forbidden or already occupied.
    
        newState = currentState # This is not allowed, and even if
        # it were allowed, the newState should be a deep COPY of the old.
    
        newRemark = "I need to think of something appropriate.\n" +\
        "Well, I guess I can say that this move is probably illegal."

        print("Returning from makeMove")
        return [[a_default_move, newState], newRemark]

    # returns all possible moves from the current state
    def getPossibleMoves(self, state):
        possibleMoves = []
        for i in range(len(state.board)):
            for j in range((state.board[0])):
                if state.board[i][j] == ' ':
                    possibleMoves.append((i, j))
        return possibleMoves

    # returns the new state after applying a move
    def applyMove(self, state, move):
        newState = State(old=state)
        newState.board[move[0]][move[1]] = self.playing
        newState.change_turn()
        return newState

    # The main adversarial search function:
    def minimax(self,
            state,
            depthRemaining,
            pruning=False,
            alpha=None,
            beta=None,
            zHashing=None):
        if depthRemaining == 0 or state.is_terminal():
            return None, self.staticEval(state)
        
        bestMove = None
        
        if self.playing == 'X':
            max = float('-inf')
            for move in self.getPossibleMoves(state):
                new_state = self.applyMove(state, move)
                _, eval = self.minimax(new_state, depthRemaining - 1, pruning, alpha, beta, zHashing)
                if eval > max:
                    max = eval
                    best_move = move
                if pruning:
                    alpha = max(alpha, eval)
                    if beta is not None and beta <= alpha:
                        break
            return bestMove, max
        else:
            min = float('inf')
            for move in self.getPossibleMoves(state):
                new_state = self.applyMove(state, move)
                _, eval = self.minimax(new_state, depthRemaining - 1, pruning, alpha, beta, zHashing)
                if eval < min:
                    min = eval
                    best_move = move
                if pruning:
                    beta = min(beta, eval)
                    if alpha is not None and beta <= alpha:
                        break
            return best_move, min
 
    def staticEval(self, state):
        print('calling staticEval. Its value needs to be computed!')
        # Values should be higher when the states are better for X,
        # lower when better for O.
        return 0
 
# OPTIONAL THINGS TO KEEP TRACK OF:

#  WHO_MY_OPPONENT_PLAYS = other(WHO_I_PLAY)
#  MY_PAST_UTTERANCES = []
#  OPPONENT_PAST_UTTERANCES = []
#  UTTERANCE_COUNT = 0
#  REPEAT_COUNT = 0 or a table of these if you are reusing different utterances

