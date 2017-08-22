from copy import deepcopy
import json
import sys
import random
from client import Client

MAX_DEPTH = 5

with open("vizinhos.json") as v_file:
	neighbors = json.load(v_file)

with open("coletas.json") as c_file:
	eatings = json.load(c_file)

def update_board(color, current_board, m_from, m_to):
	if color == "y":
		if m_to in neighbors[m_from]:
			current_board.yellow = [x if x != m_from else m_to for x in current_board.yellow]
		else:
			for n in eatings[m_from]:
				if n[2] == m_to:
					current_board.yellow = [x if x != m_from else str(n[2]) for x in current_board.yellow]
					current_board.red = [x if x != n[1] else None for x in current_board.red]
					break
	else:
		if m_to in neighbors[m_from]:
			current_board.red = [x if x != m_from else m_to for x in current_board.red]
		else:
			for n in eatings[m_from]:
				if n[2] == m_to:
					current_board.yellow = [x if x != n[1] else None for x in current_board.yellow]
					current_board.red = [x if x != m_from else str(n[2]) for x in current_board.red]
					break
	return current_board

def my_turn(current_board, me):
	aval, sequence = minimax(current_board, me, me, -sys.maxint-1,sys.maxint, 0, "")
	print aval
	list_moves(current_board, sequence, me)
	return sequence

def opponent_massacre(color, current_board):
	more = raw_input("Any more moves? (y/n):")
	while(more == "y"):
		valid = False
		m_from, m_to = read_move(color, current_board)
		current_board = update_board(color, current_board, m_from, m_to)
		more = raw_input("Any more moves? (y/n):")
	return current_board

def opponent_turn(color, current_board):
	m_from, m_to = read_move(color, current_board)
	current_board = update_board(color, current_board, m_from, m_to)
	current_board = opponent_massacre(color, current_board)
	return current_board

def read_move(color, current_board):
	m_from, m_to  = get_move()
	valid =	check_move(m_from, m_to, color, current_board)
	while not valid:
		print "Invalid move! Try Again"
		m_from, m_to  = get_move()
		valid =	check_move(m_from, m_to, color, current_board)
	return m_from, m_to

def get_move():
	data = raw_input("Enter your move (<from><space><to>): ")
	data = data.split(" ")
	m_from = data[0]
	m_to = data[1]
	return m_from, m_to

def list_moves(current_board, sequence, color):
	sequence_size = len(sequence)
	if sequence_size > 1:
		print "MASSACRE!!!!!!!!"
	print "My move(s) is(are): "
	for a, b in zip(current_board.red if color == "r" else current_board.yellow, sequence[0].red if color == "r" else sequence[0].yellow):
		if a != b:
			print "From: " + a
			print "To: "  + b
			break
	if sequence_size > 1:
		for i in range(sequence_size-1):
			for a, b in zip(sequence[i].red if color == "r" else sequence[i].yellow, sequence[i+1].red if color == "r" else sequence[i+1].yellow):
				if a != b:
					print "From: " + a
					print "To: "  + b
					break
		
def check_move(m_from, m_to, color, board):
	global neighbors
	global eatings

	if color == "y":
		if m_from not in board.yellow:
			return False
	else:
		if m_from not in board.red:
			return False

	if m_from in neighbors:
		if m_to in neighbors[m_from] and m_to not in board.yellow and m_to not in board.red:
			return True
		for pos in eatings[m_from]:
			if pos[2] == m_to:
				if color == "y":
					if pos[1] in board.red and (pos[2] not in board.yellow and pos[2] not in board.red):
						return True
				elif color == "r":
					if pos[1] in board.yellow and (pos[2] not in board.yellow and pos[2] not in board.red):
						return True
	return False

def massacre(board, color):

	global neighbors
	global eatings

	sequence = []
	ate = False

	if color == "y":
		for p in board.yellow:
			if p != None:
				for n in eatings[p]:
					if n[1] in board.red and (n[2] not in board.yellow and n[2] not in board.red):
						newYellow = [x if x != p else str(n[2]) for x in board.yellow]
						newRed = [x if x != n[1] else None for x in board.red]
						newBoard = Board()
						newBoard.setYellow(newYellow)
						newBoard.setRed(newRed)
						sequence.append(newBoard)

						sequence.extend(massacre(newBoard, color))
						ate = True
						break
			if ate:
				break
	else:
		for p in board.red:
			if p != None:
				for n in eatings[p]:
					if n[1] in board.yellow and (n[2] not in board.yellow and n[2] not in board.red):
						newYellow = [x if x != n[1] else None for x in board.yellow]
						newRed = [x if x != p else str(n[2]) for x in board.red]
						newBoard = Board()
						newBoard.setYellow(newYellow)
						newBoard.setRed(newRed)
						sequence.append(newBoard)
						if "h1" not in newBoard.red:
							sequence.extend(massacre(newBoard, color))

						ate = True
						break
			if ate:
				break
	return sequence














class Board():
	"""docstring for Board"""
	def __init__(self):
		self.yellow = [None] * 16
		self.red = [None] * 16

	def __str__(self):

		output = "YELLOW:" + str(self.yellow)
		output += "\nRED:" + str(self.red)

		return output

	def avaliacao(self, me):

		n_y = len([x for x in self.yellow if x != None])
		n_r = len([x for x in self.red if x != None])

		avg_d_r = 0.0
		hgst_d_r = 0
		for r in self.red:
			if r != None:
				r_d = ord(r[0])-96
				avg_d_r += r_d
				if r_d > hgst_d_r:
					hgst_d_r = r_d

		if n_r > 0:
			avg_d_r /= n_r


		avg_d_y = 0.0
		for y in self.yellow:
			if y != None:
				avg_d_y += ord(y[0])-96

		if n_y > 0:
			avg_d_y /= n_y

		h  = 0

		if me == "y":

			if "h1" in self.red:
				return -1000000
			elif n_r == 0:
				return 1000000


			h += (n_y - n_r) * 10 		# Difference of Soldiers            			The Higher The Better
			# h -= avg_d_r * 2			# Average Distance of Red Army To Center		The Higher The Worse
			h += avg_d_y - (avg_d_r - avg_d_y) 				# Average Distance of Yellow Army To Center		The Higher The Better
			# if "h1" in self.yellow:
			# 	h *= 5					# Yellow Dominate Throne
			return h

		else:

			if "h1" in self.red:
				return 1000000
			elif n_r == 0:
				return -1000000
			# if "h1" in self.yellow:
			#	h -= 100				# Yellow Dominate Throne
			h += (n_r - n_y) * 10		# Difference of Soldiers            			The Higher The Better
			h += avg_d_r - (avg_d_y - avg_d_r)			# Average Distance of Red Army To Center		The Higher The Better
			# h -= avg_d_y * 2			# Average Distance of Yellow Army To Center		The Higher The Worse
			h += hgst_d_r				# Closest Red Soldier 							The Highert The Better
			return h


		
	def startGame(self):
		self.yellow = ["g1","g2","g3","g4","g5","g6","g7","g8"]
		self.red = ["d1","d3","d5","d7","d9","d11","d13","d15"]

	def setYellow(self, yellow):
		self.yellow = deepcopy(yellow)

	def setRed(self, red):
		self.red = deepcopy(red)

	def move(self, color):
		children = []
		# print color


		global neighbors
		global eatings

		if color == "y":
			for p in self.yellow:
				# MOVIMENTO COMUM
				if p != None:
					for n in neighbors[p]:
						sequence = []		# Sequences of moves
						if n not in self.yellow and n not in self.red:
							newYellow = [x if x != p else str(n) for x in self.yellow]
							newBoard = Board()
							newBoard.setYellow(newYellow)
							newBoard.setRed(self.red)

							sequence.append(newBoard)

							children.append(sequence)
					# eat opponent's soldier
					for n in eatings[p]:
						sequence = []		# Sequences of moves
						if n[1] in self.red and (n[2] not in self.yellow and n[2] not in self.red):
							newYellow = [x if x != p else str(n[2]) for x in self.yellow]
							newRed = [x if x != n[1] else None for x in self.red]
							newBoard = Board()
							newBoard.setYellow(newYellow)
							newBoard.setRed(newRed)

							sequence.append(newBoard)

							# Check for MASSACRE!
							sequence.extend(massacre(newBoard, color))

							children.append(sequence)
							sequence = []

		elif color == "r":

			for p in self.red:
				# MOVIMENTO COMUM
				if p != None:
					for n in neighbors[p]:
						sequence = []		# Sequences of moves
						if n not in self.yellow and n not in self.red:
							newRed = [x if x != p else str(n) for x in self.red]
							newBoard = Board()
							newBoard.setYellow(self.yellow)
							newBoard.setRed(newRed)

							sequence.append(newBoard)

							children.append(sequence)

					# eat opponent's soldier
					for n in eatings[p]:
						sequence = []		# Sequences of moves
						if n[1] in self.yellow and (n[2] not in self.yellow and n[2] not in self.red):
							newYellow = [x if x != n[1] else None for x in self.yellow]
							newRed = [x if x != p else str(n[2]) for x in self.red]
							newBoard = Board()
							newBoard.setYellow(newYellow)
							newBoard.setRed(newRed)

							sequence.append(newBoard)
							if "h1" not in newBoard.red:
								# Check for MASSACRE!
								sequence.extend(massacre(newBoard, color))

							children.append(sequence)

		return children










def minimax(board, turn, me, alpha, beta, depth, tab):
	# print "nova iteracao da recursao"
	# print tab + "Depth: " + str(depth)
	# print tab + str(board)
	estado = board.avaliacao(me)
	# print tab + "Avaliacao: " + str(estado)

	# ends = [n for n in range(-1,2)]
	# if estado in ends:
	# 	return estado

	# print depth < MAX_DEPTH-1
	if depth < MAX_DEPTH-1:
		# print "Turn: " + turn
		# print "Me: " + me
		if turn != me:
			# print tab + "Min"

			aval = sys.maxint
			beta_board = [None]
			children = board.move(turn)
			# print "CHILDREN: " + str(len(children))
			for c in children:
				# print tab + str(c[-1])
				avalminmax, n_board = minimax(c[-1], me, me, alpha, beta, depth+1, tab+"\t")
				aval = min(aval, avalminmax)
				# print depth
				# print tab + "BOARD: " + str(n_board)
				if aval < beta:
					beta = aval
					beta_board = []
					beta_board.append(c)
				if aval == beta:
					beta_board.append(c)
				if alpha >= beta:
					# print tab + "Returned: " + str(beta)
					return beta, beta_board[random.randint(0,len(beta_board)-1)]
				
			# print tab + "Returned: " + str(aval)
			return aval, beta_board[random.randint(0,len(beta_board)-1)]

		else:
			# print tab + "Max"

			aval = -sys.maxint-1
			# print board.board
			alpha_board = [None]
			# print turn
			children = board.move(turn)

			if me == "r":
				turn = "y"
			else:
				turn = "r"

			# print "CHILDREN: " + str(len(children))
			for c in children:
				# print tab + str(c[-1])
				avalminmax, n_board = minimax(c[-1], turn, me, alpha, beta, depth+1, tab+"\t")
				aval = max(aval, avalminmax)
				# print depth
				# print tab + "BOARD: " + str(n_board)
				if aval > alpha:
					alpha = aval
					alpha_board = []
					alpha_board.append(c)
				if aval == alpha:
					alpha_board.append(c)
				if alpha >= beta:
					# print tab + "Returned: " + str(alpha)
					return alpha, alpha_board[random.randint(0,len(alpha_board)-1)]

			# print tab + "Returned: " + str(aval)
			return aval, alpha_board[random.randint(0,len(alpha_board)-1)]
	else:
		# print tab + "Returned: " + str(estado)
		return estado, board




def decode_message(opp_color,current_board, message):
	
	message = message.split(" ")
	n_board = Board()
	if len(message) == 4: # Commom move
		new_board = [x if x != message[1] else message[3] for x in(current_board.red if opp_color == "r" else current_board.yellow)]


		if opp_color == "y":
			n_board.yellow = deepcopy(new_board)
			n_board.red = deepcopy(current_board.red)
		else:
			n_board.yellow = deepcopy(current_board.yellow)
			n_board.red = deepcopy(new_board)

	elif len(message) == 6: # Eating

		new_board = [x if x != message[1] else message[3] for x in (current_board.red if opp_color == "r" else current_board.yellow)]
		new_board2 = [x if x != message[5] else None for x in (current_board.red if opp_color == "y" else current_board.yellow)]

		if opp_color == "y":
			n_board.yellow = deepcopy(new_board)
			n_board.red = deepcopy(new_board2)
		else:
			n_board.yellow = deepcopy(new_board2)
			n_board.red = deepcopy(new_board)		

	return n_board

def treat_move(color, c_board, n_board):
	moves = []
	index = 0
	boards = [c_board] + n_board
	for i in range(len(boards) - 1):
		for a, b in zip(boards[index].red if color == "r" else boards[index].yellow, boards[index+1].red if color == "r" else boards[index+1].yellow):
			if a != b:
				for m_to in neighbors[a]:
					if m_to == b:
						moves.append("De " + a + " para " + b)
						index += 1
						break
				
				if len(moves) == index:	# Eating
					for n in eatings[a]:
						if n[2] == b:
							moves.append("De " + a + " para " + b + " captura " + n[1])
							index += 1
							break
	return moves

def main(argv):
	start = Board()
	start.startGame()
	# print b

	me 			 = argv[1]
	port_send 	 = int(argv[2])
	port_rcv 	 = int(argv[3])
	ip_server 	 = argv[4]

	client = Client(port_send,port_rcv, ip_server)
	client.connect()

	opponent = "r" if me == "y" else "y"

	finished = False
	current_board = start
	
	if me == "r":
		print "I go first!"
		sequence = my_turn(current_board, me)
		moves = treat_move(me, current_board, sequence)
		print len(moves)
		for m in moves:
			print m
		current_board = sequence[-1]
		client.send_move(moves)
		aval = current_board.avaliacao(me)
		if aval >= 1000000:
			print "I win"
			finished = True
				
	else:
		print "You go first!"

	while not finished:
		if ((len([x for x in current_board.yellow if x != None]) > 0) and opponent == "y") or (opponent == "r"):
			print "Your Turn"
			
			mess = client.rcv_message()
			while mess != "fim":
				current_board = decode_message(opponent, current_board, mess)
				mess = client.rcv_message()

			aval = current_board.avaliacao(me)
			if aval <= -1000000:
				print "You win"
				finished = True
				continue

		if ((len([x for x in current_board.yellow if x != None]) > 0) and me == "y") or (me == "r"):
			print "My Turn"
			sequence = my_turn(current_board, me)
			moves = treat_move(me, current_board, sequence)
			for m in moves:
				print m
			current_board = sequence[-1]
			client.send_move(moves)
			# print current_board
			aval = current_board.avaliacao(me)
			if aval >= 1000000:
				print "I win"
				finished = True
				continue

if __name__ == '__main__':
	main(sys.argv)





