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
import google.generativeai as genai
import math


genai.configure(api_key="AIzaSyDtTnQTv7V3s30S2f0vZJnyhaMx9rl5Lkw")
model = genai.GenerativeModel("gemini-1.5-flash")



AUTHORS = 'Tony Wu and Castor Chen' 

import time # You'll probably need this to avoid losing a
 # game due to exceeding a time limit.

# Create your own type of agent by subclassing KAgent:

class OurAgent(KAgent):  # Keep the class name "OurAgent" so a game master
    # knows how to instantiate your agent class.

    def __init__(self, twin=False):
        self.twin=twin
        self.nickname = 'Yoda'
        if twin: self.nickname += 'Sith'
        self.long_name = 'Jedi Master Yoda'
        self.persona = 'Wise'
        if twin: 
            self.long_name += '\'s Evil Sith Clone'
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

        # get all possible moves
        possibleMoves = self.getPossibleMoves(currentState)
        if not possibleMoves:
            return None, "No possible moves."

        # Set depthRemaining based on k
        depthRemaining = 3
        k = self.game_type.k
        if k <= 3:
            depthRemaining = 3
        elif k <= 5:
            depthRemaining = 5
        else:
            depthRemaining = 7
        
        # minimax to find the best move
        bestMove, _ = self.minimax(currentState, depthRemaining, pruning=True, alpha=float('-inf'), beta=float('inf'))
        if (bestMove == None):
            return None, "No possible moves."

        # apply the best move to get the new state
        newState = self.applyMove(currentState, bestMove)

        # generate a new utterance
        newRemark = self.getResponse(currentRemark)

        return [[bestMove, newState], newRemark]

    # returns all possible moves from the current state
    def getPossibleMoves(self, state):
        possibleMoves = []
        for i in range(len(state.board)):
            for j in range(len(state.board[0])):
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
        
        if depthRemaining == 0 or state.finished:
            return None, self.staticEval(state)
        
        bestMove = None
        
        if self.playing == 'X':
            max = float('-inf')
            for move in self.getPossibleMoves(state):
                new_state = self.applyMove(state, move)
                _, eval = self.minimax(new_state, depthRemaining - 1, pruning, alpha, beta, zHashing)
                if eval > max:
                    max = eval
                    bestMove = move
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
                    bestMove = move
                if pruning:
                    beta = min(beta, eval)
                    if alpha is not None and beta <= alpha:
                        break
            return bestMove, min
 
    def staticEval(self, state):

        # helper method that counts the number of 
        # k-in-a-row sequences for a player
        def count_sequences(board, player, length):

            # helper method to check if a sequence is valid, 
            # i.e., all cells are the same and not blocked
            def isValidSequence(cells):
                return all(cell == player for cell in cells)
            
            count = 0
            # check rows and cols
            for i in range(len(board)):
                for j in range(len(board[0]) - length + 1):
                    # rows
                    if isValidSequence(board[i][j:j+length]):
                        count += 1
                    # cols
                    if isValidSequence([board[j+k][i] for k in range(length)]):
                        count += 1

            # check diags
            for i in range(len(board) - length + 1):
                for j in range(len(board[0]) - length + 1):
                    # down-right diag
                    if isValidSequence([board[i+k][j+k] for k in range(length)]):
                        count += 1
                    # down-left diag
                    if isValidSequence([board[i+k][j+length-1-k] for k in range(length)]):
                        count += 1
            
            return count
        
        # count the num of streaks of length 1 to K-1 for a player
        def count_streaks(board, player):
            score = 0
            for streakLen in range(1, self.game_type.k):
                temp = count_sequences(board, player, streakLen)

                # set weights
                # with sigmoid func
                # weight = 1 / (1 + math.exp(-streakLen))

                # with exponential func
                weight = (1.6**streakLen)

                score += temp * weight
            return score
        
        X_score = count_streaks(state.board, 'X')
        O_score = count_streaks(state.board, 'O')

        return X_score - O_score
    
    def getResponse(self, currentRemark):
        newRemark = "OK"
        self.utterances_matter = True
        if (self.utterances_matter):
            try:
                response = model.generate_content(
                    f"Pretend you are {self.long_name} with a {self.persona} persona in a K-in-a-row game."
                    f"Your opponent just said \"{currentRemark}\". What is your response?"
                )
                return response.text + "\n"
            except Exception as e:
                return "Down, Gemini® is. Respond, I cannot."
        return newRemark
 
# OPTIONAL THINGS TO KEEP TRACK OF:

#  WHO_MY_OPPONENT_PLAYS = other(WHO_I_PLAY)
#  MY_PAST_UTTERANCES = []
#  OPPONENT_PAST_UTTERANCES = []
#  UTTERANCE_COUNT = 0
#  REPEAT_COUNT = 0 or a table of these if you are reusing different utterances

# I used python 3.9 and 
# pip install -q -U google-generativeai
# To install agent. More info: https://ai.google.dev/gemini-api/docs/quickstart?lang=python

# Sample code to test agent, output in terminal
agent = OurAgent(True)
agent.getResponse("Are you evil?")