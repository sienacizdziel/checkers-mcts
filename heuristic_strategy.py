import random
def heuristic(board):
    ''' heuristic function derived from two sites:
     - http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.39.742&rep=rep1&type=pdf 
     - http://www.cs.columbia.edu/~devans/TIC/AB.html '''

    positions = board.searcher.get_positions_by_player(board.player_turn)
    # print(positions)

    # heuristic weights:
        # how many pieces on the board
        # what pieces are on the board 
        # mobility value: number of legal moves per each player
        # distance from being a king

    piece_quality = num_pieces = king_distance = 0
    mobility = len(board.get_possible_moves())
    for pos in positions:
        num_pieces += 1
        # kings count as 5 points, other pieces count as 3
        if board.searcher.get_piece_by_position(pos).king:
            piece_quality += 5
        else:
            if board.player_turn == 1:
                # print("player 1")
                king_distance += 7 - ((pos - 1) // 4) # rows to being a king
            else:
                # print("player 2")
                king_distance += (pos - 1) // 4 # rows to being a king
            piece_quality += 3

    w1, w2, w3, w4 = 3, 3, 5, 2
    return w1 * num_pieces + w2 * piece_quality + w3 * mobility + w4 * king_distance

    
def heuristic_strategy(board):
    ''' takes a board and returns the best move based off a basic heuristic '''
    max_heuristic, best_move = -float('inf'), None
    # print(board.get_possible_moves())
    # print(board.get_possible_moves())
    # if board.get_winner() != None:
        # print("here")
    # print("heuristic strategy" + str(board.get_possible_moves()))
    for move in board.get_possible_moves():
        value = heuristic(board.create_new_board_from_move(move))
        if value > max_heuristic:
            max_heuristic = value
            best_move = [move]
        elif value == max_heuristic:
            best_move.append(move)
        # print(max_heuristic)
    # print(best_move)
    # print(best_move)
    # print(max_heuristic)
    return random.choice(best_move)

    
