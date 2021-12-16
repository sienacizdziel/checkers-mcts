from copy import deepcopy
from functools import reduce
from .board_searcher import BoardSearcher
from .board_initializer import BoardInitializer

class Board:

	def __init__(self):
		self.player_turn = 1
		self.width = 4
		self.height = 8
		self.position_count = self.width * self.height
		self.rows_per_user_with_pieces = 3
		self.position_layout = {}
		self.piece_requiring_further_capture_moves = None
		self.previous_move_was_capture = False
		self.searcher = BoardSearcher()
		BoardInitializer(self).initialize()

	def get_state(self):
		''' returns a move's current state '''
		''' format (pieces, previous_move_was_capture, captured_piece, piece_requiring_further_capture_moves, player_turn, player_positions) '''
		state = {
			"pieces": self.pieces,
			"previous_move_was_capture": self.previous_move_was_capture,
			"captured_piece": None,
			"piece_requiring_further_capture_moves": self.piece_requiring_further_capture_moves,
			"player_turn": self.player_turn,
			"positions_by_player": self.searcher.get_pieces_by_player(),
			"piece_by_position": self.searcher.position_pieces
		}
		return state

	def get_state_winner(self, state):
		''' returns winner given a state '''
		def count_movable_player_pieces(self, player_number = 1):
			return reduce((lambda count, piece: count + (1 if piece.is_movable() else 0)), self.searcher.get_pieces_by_player(player_number), 0)
		
		if state["player_turn"] == 1 and not count_movable_player_pieces(1):
			return 2
		elif state["player_turn"] == 2 and not count_movable_player_pieces(2):
			return 1
		else:
			return None

	def result(self, state, move):
		''' returns the state a move would result in '''
		''' format (pieces, previous_move_was_capture, captured_piece, piece_requiring_further_capture_moves, new_player_turn) '''
		new_state = {}

		def temp_move_piece(move):
			state["piece_by_position"].get(move[0]).move(move[1])
			return sorted(self.pieces, key = lambda piece: piece.position if piece.position else 0)

		if move in self.get_possible_capture_moves():
			new_state["previous_move_was_capture"] = True
			piece = self.searcher.get_piece_by_position(move[0])
			originally_was_king = piece.king
			captured_piece = piece.capture_move_enemies[move[1]]
			new_state["pieces"] = temp_move_piece(move)
			further_capture_moves_for_piece = [capture_move for capture_move in self.get_possible_capture_moves() if move[1] == capture_move[0]]

			if further_capture_moves_for_piece and (originally_was_king == piece.king):
				new_state["piece_requiring_further_capture_moves"] = self.searcher.get_piece_by_position(move[1])
			else:
				new_state["piece_requiring_further_capture_moves"] = None
				new_state["player_turn"] = 1 if self.player_turn == 2 else 2
		else:
			new_state["previous_move_was_capture"] = False
			new_state["pieces"] = temp_move_piece(move)
			new_state["player_turn"] = 1 if self.player_turn == 2 else 2
			new_state["captured_piece"] = None
			new_state["piece_requiring_further_capture_moves"] = None

		return new_state

	def count_movable_player_pieces(self, player_number = 1):
		return reduce((lambda count, piece: count + (1 if piece.is_movable() else 0)), self.searcher.get_pieces_by_player(player_number), 0)

	def get_possible_moves(self):
		# capture_moves = self.get_possible_capture_moves()
		# # print(positional_moves)
		# # print(capture_moves)
		# # print(positional_moves + capture_moves)
		# return positional_moves + capture_moves
		
		# # if positional_moves and capture_moves:
		# # 	print(positional_moves + capture_moves)
		# # 	return positional_moves + capture_moves
		# # elif capture_moves:
		# # 	return capture_moves
		# # else:		
		# # 	return positional_moves

		capture_moves = self.get_possible_capture_moves()
		return capture_moves if capture_moves else self.get_possible_positional_moves()

	def get_possible_capture_moves(self):
		return reduce((lambda moves, piece: moves + piece.get_possible_capture_moves()), self.searcher.get_pieces_in_play(), [])

	def get_possible_positional_moves(self):
		return reduce((lambda moves, piece: moves + piece.get_possible_positional_moves()), self.searcher.get_pieces_in_play(), [])

	def position_is_open(self, position):
		return not self.searcher.get_piece_by_position(position)

	def create_new_board_from_move(self, move):
		# print("here")
		new_board = deepcopy(self)

		if move in self.get_possible_capture_moves():
			new_board.perform_capture_move(move)
		else:
			new_board.perform_positional_move(move)

		return new_board

	def move(self, move):
		# print("move" + str(move))
		prev_state = {
			"previous_move_was_capture": self.previous_move_was_capture,
			"pieces": self.pieces,
			"piece_requiring_further_capture_moves": self.piece_requiring_further_capture_moves,
			"player_turn": self.player_turn
		}

		if move in self.get_possible_capture_moves():
			enemy_piece, enemy_position = self.perform_capture_move(move)
			move_type = "capture"
		else:
			self.perform_positional_move(move)
			move_type = "positional"
			enemy_piece, enemy_position = None, None

		prev_state["move_type"] = move_type
		prev_state["enemy_piece"] = enemy_piece
		prev_state["enemy_position"] = enemy_position

		return self, prev_state

	def undo_move(self, prev_state):
		self.previous_move_was_capture = prev_state["previous_move_was_capture"]
		if prev_state["enemy_piece"]:
			prev_state["enemy_piece"].uncapture(prev_state["enemy_position"])
		self.pieces = prev_state["pieces"]
		self.piece_requiring_further_capture_moves = prev_state["piece_requiring_further_capture_moves"]
		self.player_turn = prev_state["player_turn"]

	def perform_capture_move(self, move):
		self.previous_move_was_capture = True
		piece = self.searcher.get_piece_by_position(move[0])
		originally_was_king = piece.king
		enemy_piece = piece.capture_move_enemies[move[1]]
		enemy_position = enemy_piece.capture()
		self.move_piece(move)
		further_capture_moves_for_piece = [capture_move for capture_move in self.get_possible_capture_moves() if move[1] == capture_move[0]]

		if further_capture_moves_for_piece and (originally_was_king == piece.king):
			self.piece_requiring_further_capture_moves = self.searcher.get_piece_by_position(move[1])
		else:
			self.piece_requiring_further_capture_moves = None
			self.switch_turn()
		return enemy_piece, enemy_position

	def perform_positional_move(self, move):
		self.previous_move_was_capture = False
		# print(self.searcher.get_piece_by_position(move[0]))
		self.move_piece(move)
		self.switch_turn()

	def switch_turn(self):
		self.player_turn = 1 if self.player_turn == 2 else 2

	def move_piece(self, move):
		self.searcher.get_piece_by_position(move[0]).move(move[1])
		self.pieces = sorted(self.pieces, key = lambda piece: piece.position if piece.position else 0)

	def is_valid_row_and_column(self, row, column):
		if row < 0 or row >= self.height:
			return False

		if column < 0 or column >= self.width:
			return False

		return True

	def get_winner(self):
		if self.player_turn == 1 and not self.count_movable_player_pieces(1):
			return 2
		elif self.player_turn == 2 and not self.count_movable_player_pieces(2):
			return 1
		elif not self.count_movable_player_pieces(1) and not self.count_movable_player_pieces(2):
			# print("hereeeeee")
			return 0
		else:
			return None

	def __setattr__(self, name, value):
		super(Board, self).__setattr__(name, value)

		if name == 'pieces':
			[piece.reset_for_new_board() for piece in self.pieces]

			self.searcher.build(self)

	# def __hash__(self):
	# 	return hash(str([self.player_turn, self.searcher.uncaptured_pieces, self.searcher.open_positions, self.searcher.filled_positions, self.searcher.player_positions, self.searcher.player_pieces]))

	# def __eq__(self, other):
	# 	return str([self.player_turn, self.searcher.uncaptured_pieces, self.searcher.open_positions, self.searcher.filled_positions, self.searcher.player_positions, self.searcher.player_pieces]) == str([other.player_turn, other.searcher.uncaptured_pieces, other.searcher.open_positions, other.searcher.filled_positions, other.searcher.player_positions, other.searcher.player_pieces])

	def board_value(self):
		pieces = []
		for piece in self.searcher.uncaptured_pieces:
			# print(piece)
			pieces.append(piece.get_value())
			# , self.searcher.player_pieces
		return str([self.player_turn, self.searcher.open_positions, self.searcher.filled_positions, self.searcher.player_positions])