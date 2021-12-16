from checkers.game import *
from checkers.board import *
import sys
from mcts_strategy import *
from heuristic_strategy import *
from random_strategy import *
import random

# hello! to run, just type python test_checkers.py.

if __name__ == "__main__":
    test = False
    if len(sys.argv) == 4 or len(sys.argv) == 5:
        print("testing...")
        test = True
    elif len(sys.argv) != 1:
        print("usage: python test_checkers.py num_games strategy1 strategy2 [depth]")
        sys.exit(1)

    # for my own (or your) testing purposes
    ''' run: python test_checkers.py num_games strategy1 strategy2 [depth] 
    num_games is the number of full games you'd like to play
    strategy1 and strategy2 are either 'random', 'heuristic', or 'mcts'
    depth is an optional argument for the depth of mcts (if not given, the depth will default to 200)
    output will be a list of results (so, say player1 wins every time in 3 games: [1, 1, 1]) along with a summary of what you ran (e.g. 'mcts 200 depth vs. heuristic') '''

    if test:
        winners = []
        for i in range(int(sys.argv[1])):
            game = Game()
            board, board2 = Board(), Board()

            # parsing command line
            if sys.argv[2] == 'random':
                p1_test_function = random_strategy
            elif sys.argv[2] == 'heuristic':
                p1_test_function = heuristic_strategy
            elif sys.argv[2] == 'mcts':
                if len(sys.argv) == 5:
                    depth = int(sys.argv[4])
                else:
                    depth = 200
                p1_test_function = "mcts_strategy"
            else:
                print("usage: python test_checkers.py num_games strategy1 strategy2 [depth]")
                print("strategy1 can be random, heuristic, or mcts")
                sys.exit(1)
            if sys.argv[3] == 'random':
                p2_test_function = random_strategy
            elif sys.argv[3] == 'heuristic':
                p2_test_function = heuristic_strategy
            else:
                print("usage: python test_checkers.py num_games strategy1 strategy2 [depth]")
                print("strategy2 can be random or heuristic")
                sys.exit(1)

            # running game
            while not game.get_winner():

                # player 1
                if game.whose_turn() == 1:
                    if p1_test_function == "mcts_strategy":
                        best_move = mcts_strategy(depth)
                        move = best_move(board)
                    else:
                        move = p1_test_function(board)

                # player 2
                else:
                    move = p2_test_function(board)

                print("player" + str(game.whose_turn()) + " moved " + str(move))
                game.move(move)
                board = board.create_new_board_from_move(move)

            print("winner of game " + str(i + 1) + ": " + str(board.get_winner()))
            winners.append(board.get_winner())
        print("winners: " + str(winners))
        if sys.argv[2] == 'mcts':
            print("game summary: mcts " + str(depth) + " vs " + sys.argv[3])
        else:
            print("game summary: " + sys.argv[2] + " vs " + sys.argv[3])

    else:
        print("Hi Prof. Glenn - welcome to my CS 474 final project!")
        input("Press enter to move to each line ")
        input("For my project, I wrote an MCTS solution to checkers ")
        
        input("Checkers is a two-player, turn-based, non-stochastic game where both players have perfect information. Each player has 12 pieces and can move their pieces diagonally forward on a checkerboard. Players can jump their opponent's pieces to take them off the board. If a player's piece reaches the other side, it becomes a king and can now move diagonally backwards too. The goal is to remove all of your opponent's pieces from the board. ")
        
        input("To solve this, first I modified ImparaAI's checkers implementation (https://github.com/ImparaAI/checkers) ")
        input("(This included finding a way to make the game test playouts without permanently changing the state of the board.)")
        input("Then, I wrote a heuristic function, which weighted different values like: how many pieces on the board, what pieces are on the board, mobility value (number of legal moves per each player), and distance from being a king. The heuristic strategy is  to select the next possible move with the highest heuristic value.")
        input("Then, I modified our MCTS project from class, using a new reward system, the checkers implementation (which included having to create a state because using an object as a hash table key is finnicky), and an epsilon greedy default policy in which 80% of the time the heuristic strategy is chosen from the possible moves and 20% of the time a random move is chosen. ")
        
        input("So here are my results... ")
        input("* drumroll please * ")
        input("Important note: I have discovered that in this implementation of get_possible_moves(), if even one capture move is available, it will only return capture moves. So, the random strategy is a little better than random!")
        
        input("In a competition between a heuristic strategy and random strategy, out of 1000 games, the heuristic strategy wins: 99.5% of the time ")
        input("As for the rest, my program has been running for over 2 hours and unfortunately still has not tested a significant amount of games and iterations (20 games, 200 depth mcts), so I will have to make an educated guess on its success ")
        input("In a competition between an MCTS algorithm (with 100 depth) and random strategy, out of 5 games, the MCTS algorithm wins: ~75% of the time")
        input("Finally, in a competition between an MCTS algorithm (with 100 depth) and heuristic strategy, out of 5 games, the MCTS algorithm wins: ~50% of the time")

        input("Though certainly not perfect, it does produce results..? ")
        input("If you'd like to test for yourself, run: 'python test_checkers.py num_games strategy1 strategy2 [depth]'. num_games is the number of full games you'd like to play. strategy1 can be either 'random', 'heuristic', or 'mcts'. strategy2 can be either 'random' or 'heuristic'. depth is an optional argument for the depth of mcts (if not given, the depth will default to 200). The output will be a list of results (so, say player1 wins every time in 3 games: [1, 1, 1]) along with a summary of what you ran (e.g. 'mcts 200 depth vs. heuristic') ")
        print("Thank you very much for an amazing class!! I learned so much and am excited to apply these concepts in the future. ")
        print("- Siena")
