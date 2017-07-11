from copy import deepcopy
import json
import sys
import random

MAX_DEPTH = 4

with open("vizinhos.json") as v_file:
	neighbors = json.load(v_file)

with open("coletas.json") as c_file:
	eatings = json.load(c_file)

def check_move(m_from, m_to, color, board):

	global neighbors
	global eatings

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
		output += "\t RED:" + str(self.red)

		return output

	def avaliacao(self, me):
		n_y = len([x for x in self.yellow if x != None])
		n_r = len([x for x in self.red if x != None])
		h  = 0
		if me == "y":
			if "h1" in self.yellow:
				h += 50
			h += (n_y - n_r) * 100
			return h

		else:
			if "h1" in self.yellow:
				h -= 50
			h += (n_r - n_y) * 100
			return h

		# return random.randint(0,100)

		
	def startGame(self):
		self.yellow = ["g1","g2","g3","g4","g5","g6","g7","g8","f1","f2","f3","f4","f5","f6","f7","f8"]
		self.red = ["b1","a2","a3","a4","a5","a6","a7","a8","a9","a10","a11","a12","a13","a14","a15","a16"]

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
				sequence = []		# Sequences of moves
				# MOVIMENTO COMUM
				if p != None:
					for n in neighbors[p]:
						if n not in self.yellow and n not in self.red:
							newYellow = [x if x != p else str(n) for x in self.yellow]
							newBoard = Board()
							newBoard.setYellow(newYellow)
							newBoard.setRed(self.red)

							sequence.append(newBoard)

							children.append(sequence)
					# CONSUMO DE PECA OPONENTE
					for n in eatings[p]:
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

		elif color == "r":

			for p in self.red:
				sequence = []		# Sequences of moves
				# MOVIMENTO COMUM
				if p != None:
					for n in neighbors[p]:
						if n not in self.yellow and n not in self.red:
							newRed = [x if x != p else str(n) for x in self.red]
							newBoard = Board()
							newBoard.setYellow(self.yellow)
							newBoard.setRed(newRed)

							sequence.append(newBoard)

							children.append(sequence)

					# CONSUMO DE PECA OPONENTE
					for n in eatings[p]:
						if n[1] in self.yellow and (n[2] not in self.yellow and n[2] not in self.red):
							newYellow = [x if x != n[1] else None for x in self.yellow]
							newRed = [x if x != p else str(n[2]) for x in self.red]
							newBoard = Board()
							newBoard.setYellow(newYellow)
							newBoard.setRed(newRed)

							sequence.append(newBoard)

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
			beta_board = None
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
					beta_board = c
				if alpha >= beta:
					# print tab + "Returned: " + str(beta)
					return beta, beta_board
					
			# print tab + "Returned: " + str(aval)
			return aval, beta_board

		else:
			# print tab + "Max"

			aval = -sys.maxint-1
			# print board.board
			alpha_board = None
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
					alpha_board = c
				if alpha >= beta:
					# print tab + "Returned: " + str(alpha)
					return alpha, alpha_board

			# print tab + "Returned: " + str(aval)
			return aval, alpha_board 
	else:
		# print tab + "Returned: " + str(estado)
		return estado, board
def main():
	start = Board()
	start.startGame()
	# print b
	opponent = raw_input("Which color are you? (r/y):  ")
	# children = b.move("r")
	
	me = "r" if opponent == "y" else "y"

	finished = False

	if me == "r":
		print "I go first!"
		aval, sequence = minimax(start, "r", me, -sys.maxint-1,sys.maxint, 0, "")
		sequence_size = len(sequence)
		if sequence_size > 1:
			print "MASSACRE!!!!!!!!"
		print "My move(s) is(are): "
		for a, b in zip(start.red, sequence[0].red):
			if a != b:
				print "From: " + a
				print "To: "  + b
				break
		if sequence_size > 1:
			for i in range(sequence_size-1):
				for a, b in zip(sequence[i].red, sequence[i+1].red):
					if a != b:
						print "From: " + a
						print "To: "  + b
						break
		current_board = sequence[-1]
	else:
		print "You go first!"


	while not finished:
		print "Your Turn"
		print current_board
		data = raw_input("Enter your move (<from><space><to>): ")
		data = data.split(" ")
		m_from = data[0]
		m_to = data[1]

		valid =	check_move(m_from, m_to, opponent, current_board)

		while not valid:
			print "Invalid move! Try Again"

			data = raw_input("Enter your move (<from><space><to>): ")
			data = data.split(" ")
			m_from = data[0]
			m_to = data[1]

			valid =	check_move(m_from, m_to, opponent, current_board)


		if opponent == "y":
			current_board.yellow = [x if x != m_from else m_to for x in current_board.yellow]
		else:
			current_board.red = [x if x != m_from else m_to for x in current_board.red]

		aval = current_board.avaliacao(me)

		if aval < -100000:
			print "You win"
			break

		print "My Turn"
		print current_board
		aval, sequence = minimax(current_board, me, me, -sys.maxint-1,sys.maxint, 0, "")
		sequence_size = len(sequence)
		if sequence_size > 1:
			print "MASSACRE!!!!!!!!"
		print "My move(s) is(are): "
		for a, b in zip(current_board.red, sequence[0].red):
			if a != b:
				print "From: " + a
				print "To: "  + b
				break
		if sequence_size > 1:
			for i in range(sequence_size-1):
				for a, b in zip(sequence[i].red, sequence[i+1].red):
					print sequence[i]
					print sequence[i+1]
					if a != b:
						print "From: " + a
						print "To: "  + b
						break
		
		current_board = sequence[-1]
		
		aval = current_board.avaliacao(me)
		
		if aval > 100000:
			print "I win"
			break

if __name__ == '__main__':
	main()





