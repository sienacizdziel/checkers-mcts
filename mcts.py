from checkers.game import *
from checkers.board import *
import math
import random
from heuristic import *
# import pdb

# root 
# special case of ucb if there is a child with zero visit count go to it
# recursively update the rewards 
# pick a child, then do the playout 

# while it > 0
# start at root
    # while not leaf
        # do UCB to select child
    # add node if expandable (nonterminal / non-zero visits)
    # random playout 
    # backpropagate reward 

# average reward over visits
# keep track of reward for player one
# ask root who's the current player
# if p1, max ucb
    # tot reward / # visits + sqrt(2ln parent visits / # visits)
    # subtract for p2 when minning

# key = parent to child
# value = data

# don't forget about time limitations
# is the first traversal of the tree an iteration?
    # the way i see iteration: 
    # look at each child node of the root
    # then, start counting iterations
    # run playouts on all children of the children, until out of iterations
    # select ideal choice based off the node values from the playouts
    # will the number of iterations ever be less than the amount of children you can get from the parent?

class Node:
    def __init__(self, parent, unvisited_children, reward=0, visits=0): 
        self.parent = parent
        self.reward = reward
        self.visits = visits
        self.unvisited_children = unvisited_children
        self.children = {} # key: position, value: (Node, move)

    def get_ucb_stat(self, player, parent_visits, is_exploration):
        # split into player one and two
        # visits should be the natural log of the parent/child
        if is_exploration:
            print(self.reward/ self.visits)
            return (self.reward / self.visits)
        elif player == 1:
            return (self.reward / self.visits) + math.sqrt((0.75 * math.log(parent_visits)) / self.visits)
        else:
            return (self.reward / self.visits) - math.sqrt((0.75 * math.log(parent_visits)) / self.visits)

def mcts_strategy(num_iters):
    ''' returns a function that takes a position and returns the move suggested
    by running MCTS for that number of iterations starting with that position '''
    def playout(board, depth):
        epsilon = 0.8
        while True:
            if depth == 0:
                return 0.5
            # print(board.count_movable_player_pieces(1))
            # print(board.count_movable_player_pieces(2))
            # print(board.get_possible_moves())
            if board.get_winner() != None:
                return 1.0 if board.get_winner() == 1 else 0.0
            if board.player_turn == 1:
                if random.random() < epsilon:
                    move = heuristic_strategy(board)
                else:
                    move = random.choice(board.get_possible_moves())
            else:
                if random.random() < epsilon:
                    move = heuristic_strategy(board)
                else:
                    move = random.choice(board.get_possible_moves())
            board = board.create_new_board_from_move(move)
            depth -= 1

    def playout_recursive(board, depth):
        epsilon = 0.8
        if depth == 0:
            return 0.5
        # put turn limit (wikipedia game complexity table, 2x avg length) on playout and call a draw if it doesn't end in a number of moves
        # replace recursion in playout with iteration
        # do heuristic with some prob and otherwise do random
        ''' conducts a random playout simulation on a position and returns the winner '''
        if board.get_winner() != None:
            # print(board.get_winner())
            return 1.0 if board.get_winner() == 1 else 0.0
        # print(board.get_possible_moves())
        if board.player_turn == 1:
            if random.random() < epsilon:
                move = heuristic_strategy(board)
            else:
                move = random.choice(board.get_possible_moves())
        else:
            if random.random() < epsilon:
                move = heuristic_strategy(board)
            else:
                move = random.choice(board.get_possible_moves())
        # print(move)
        return playout(board.create_new_board_from_move(move), depth - 1)

    def calc_ucb(player, curr_node, is_exploration):
        ''' calculates the max (player 0) or min (player 1) ucb '''
        ''' returns the best moves based off ucbs '''
        moves = []
        for node, move in curr_node.children.values():
            moves.append((node.get_ucb_stat(player, curr_node.visits, is_exploration), move))

        best_move = None
        if player == 1:
            max_ucb = -float('inf')
            for ucb, move in moves:
                if ucb > max_ucb:
                    max_ucb = ucb
                    best_move = [move]
                elif ucb == max_ucb:
                    best_move.append(move)
        else:
            min_ucb = float('inf')
            for ucb, move in moves:
                if ucb < min_ucb:
                    min_ucb = ucb
                    best_move = [move]
                elif ucb == min_ucb:
                    best_move.append(move)
        return random.choice(best_move)

    # def hash_board(board):
    #     return (board.player_turn, board.previous_move_was_capture, board.pieces)


    def find_best_move(board):
        ''' returns the best move given a starting position '''
        iterations = num_iters
        positions = {} # key: Node, value: position

        # make a root node
        root = Node(None, board.get_possible_moves(), visits=1)

        positions[root] = board
        curr_node = root

        while iterations > 0:
            # selection step
            # at a terminal node
            if positions[curr_node].get_winner() != None:
                # backpropagate
                backprop = curr_node
                while backprop != None:
                    backprop.reward += 1.0 if positions[curr_node].get_winner() == 1 else 0.0
                    backprop.visits += 1
                    backprop = backprop.parent
                curr_node = root
                iterations -= 1
                continue

            # select child with max/min ucb
            # print(curr_node.unvisited_children)
            # print(positions[curr_node])
            if curr_node.unvisited_children == []:
                if positions[curr_node].player_turn == 1:
                    # print("Here")
                    next_move = calc_ucb(1, curr_node, False)
                    # print(heuristic_strategy(board))
                    # next_move = heuristic_strategy(board)
                else:
                    next_move = calc_ucb(2, curr_node, False)
                # print(positions[curr_node])
                # next_pos = positions[curr_node].move(next_move)
                next_pos = positions[curr_node].create_new_board_from_move(next_move)
                # print(str([next_pos.player_turn, next_pos.searcher.uncaptured_pieces, next_pos.searcher.open_positions, next_pos.searcher.filled_positions, next_pos.searcher.player_positions, next_pos.searcher.player_pieces]))
                # print(hash(next_pos))
                curr_node = curr_node.children[next_pos.board_value()][0]
                continue
            
            # expansion step
            # select a random choice from potential next moves and add to edges dictionary
            # print(curr_node.unvisited_children)
            next_move = random.choice(curr_node.unvisited_children)
            curr_node.unvisited_children.remove(next_move)
            # next_pos, prev_state = positions[curr_node].move(next_move)
            next_pos = positions[curr_node].create_new_board_from_move(next_move)
            next_node = Node(curr_node, next_pos.get_possible_moves())
            positions[next_node] = next_pos
            curr_node.children[next_pos.board_value()] = (next_node, next_move)
            # print(curr_node.children[next_pos.board_value()])
            # next_pos.undo_move(prev_state)
            
            # simulate step
            winner = playout(board, 50)

            # backpropagation step
            backprop = next_node
            while backprop != None:
                backprop.reward += winner
                backprop.visits += 1
                backprop = backprop.parent

            curr_node = root
            iterations -= 1
            
        # return best move by max ucb
        # print(board.player_turn)
        if board.player_turn == 1:
            best_move = calc_ucb(1, root, True)
        else:
            best_move = calc_ucb(2, root, True)
        # print(board)
        # print(best_move)
        return best_move

    return find_best_move
