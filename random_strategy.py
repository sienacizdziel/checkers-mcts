from checkers.board import *
import random

def random_strategy(board):
    ''' random strategy for checkers board '''
    return random.choice(board.get_possible_moves())