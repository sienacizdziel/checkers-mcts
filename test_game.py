from checkers.game import *
from checkers.board import *
import sys
from mcts import *
from heuristic import *

if __name__ == "__main__":
    test = False
    if len(sys.argv) == 2:
        print("testing...")
        test = True

    # for my own testing purposes
    if test:
        winners = []
        for i in range(int(sys.argv[1])):
            game = Game()
            board, board2 = Board(), Board()
            while not game.get_winner():
                if game.whose_turn() == 1:
                    # print(board.get_possible_moves())
                    best_move = mcts_strategy(200)
                    move = best_move(board)
                    # move = heuristic_strategy(board)
                else:
                    # move = random.choice(board.get_possible_moves())
                    move = heuristic_strategy(board)
                print(str(move) + " player" + str(game.whose_turn()))
                game.move(move)
                board = board.create_new_board_from_move(move)
                # print(best_move(test_board2))
                # board = board.create_new_board_from_move(move)
                # board2 = board
            print(board.get_winner())
            winners.append(board.get_winner())
        print(winners)
        print("mcts 200 heuristic vs. heuristic")
        # game2 = Game()
        # board3 = Board()
        # while not game2.get_winner():
        #     move = heuristic_strategy(board3)
        #     game2.move(move)
        #     board3 = board3.create_new_board_from_move(move)
        # print(board3.get_winner())

    else:
        print("Hi Prof. Glenn - welcome to my CS 474 final project!")
        input("Press enter to move to each line ")
        input("For my project, I wrote an MCTS solution to checkers ")
        input("Checkers is a two-player, turn-based, non-stochastic game where both players have perfect information. Each player has 12 pieces and can move their pieces diagonally forward on a checkerboard. Players can jump their opponent's pieces to take them off the board. If a player's piece reaches the other side, it becomes a king and can now move diagonally backwards too. The goal is to remove all of your opponent's pieces from the board. ")
        input("To solve this, first I modified ImparaAI's checkers implementation (https://github.com/ImparaAI/checkers) ")
        input("(This included finding a way to make the game test playouts without permanently changing the state of the board.)")
        input("Then, I wrote a heuristic function, which weighted different values like: how many pieces on the board, what pieces are on the board, mobility value (number of legal moves per each player), and distance from being a king. The heuristic strategy is then to select the next possible move with the highest heuristic value.")
        input("Then, I modified our MCTS project from class, using a new reward system, the checkers implementation (which included having to create a state because using an object as a hash table key is finnicky), and an epsilon greedy default policy in which 80\% of the time the heuristic strategy is chosen from the possible moves and 20\% of the time a random move is chosen. ")
        input("So here are my results... ")
        input("* drumroll please * ")
        input("Important note: I have discovered that in get_possible_moves(board) in this implementaiton of checkers")
        input("In a competition between ")
        input("In a competition between my MCTS algorithm and ")



    
# print(game.whose_turn()) #1 or 2
# print(game.get_possible_moves()) #[[9, 13], [9, 14], [10, 14], [10, 15], [11, 15], [11, 16], [12, 16]]
# game.move([9, 13])
# print(game.is_over()) #True or False
# print(game.get_winner()) #None or 1 or 2
# print(game.moves) #[[int, int], [int, int], ...]
# game.consecutive_noncapture_move_limit = 20
# print(game.move_limit_reached()) #True or False
# for piece in game.board.pieces:
# 	print(piece.player) #1 or 2
# 	piece.other_player #1 or 2
# 	piece.king #True or False
# 	piece.captured #True or False
# 	piece.position #1-32
# 	piece.get_possible_capture_moves() #[[int, int], [int, int], ...]
# 	piece.get_possible_positional_moves() #[[int, int], [int, int], ...]
