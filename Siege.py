from copy import deepcopy
import json
import sys
import random

MAX_DEPTH = 2

with open("vizinhos.json") as v_file:
	neighbors = json.load(v_file)

with open("coletas.json") as c_file:
	eatings = json.load(c_file)

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
		if me == "y":
			return n_y - n_r
		else:
			return n_r - n_y

		# return random.randint(0,100)

		
	def startGame(self):
		self.yellow = ["g1","g2","g3","g4","g5","g6","g7","g8","f1","f2","f3","f4","f5","f6","f7","f8"]
		self.red = ["a1","a2","a3","a4","a5","a6","a7","a8","a9","a10","a11","a12","a13","a14","a15","a16"]

	def setYellow(self, yellow):
		self.yellow = deepcopy(yellow)

	def setRed(self, red):
		self.red = deepcopy(red)
	
	def move(self, color):
		children = []
		print color

		global neighbors
		global eatings

		if color == "y":
			for p in self.yellow:
				# MOVIMENTO COMUM
				for n in neighbors[p]:
					if n not in self.yellow and n not in self.red:
						newYellow = [x if x != p else str(n) for x in self.yellow]
						newBoard = Board()
						newBoard.setYellow(newYellow)
						newBoard.setRed(self.red)
						children.append(newBoard)
				# CONSUMO DE PECA OPONENTE
				for n in eatings[p]:
					if n[1] in self.red and (n[2] not in self.yellow and n[2] not in self.red):
						newYellow = [x if x != p else str(n[2]) for x in self.yellow]
						newRed = [x if x != n[1] else None for x in self.red]
						newBoard = Board()
						newBoard.setYellow(newYellow)
						newBoard.setRed(newRed)
						children.append(newBoard)

		elif color == "r":

			for p in self.red:
				# MOVIMENTO COMUM
				for n in neighbors[p]:
					if n not in self.yellow and n not in self.red:
						newRed = [x if x != p else str(n) for x in self.red]
						newBoard = Board()
						newBoard.setYellow(self.yellow)
						newBoard.setRed(newRed)
						children.append(newBoard)

				# CONSUMO DE PECA OPONENTE
				for n in eatings[p]:
					if n[1] in self.yellow and (n[2] not in self.yellow and n[2] not in self.red):
						newYellow = [x if x != n[1] else None for x in self.yellow]
						newRed = [x if x != p else str(n[2]) for x in self.red]
						newBoard = Board()
						newBoard.setYellow(newYellow)
						newBoard.setRed(newRed)
						children.append(newBoard)

		return children

def minimax(board, turn, me, alpha, beta, depth):
	# print "nova iteracao da recursao"
	print depth
	print board
	estado = board.avaliacao(me)
	print estado

	# ends = [n for n in range(-1,2)]
	# if estado in ends:
	# 	return estado
	print depth < MAX_DEPTH
	if depth < MAX_DEPTH:
		print "Turn: " + turn
		print "Me: " + me
		if turn != me:
			# print "Min"
			aval = sys.maxint
			beta_board = None
			children = board.move(turn)
			print "CHILDREN: " + str(len(children))
			for c in children:
				avalminmax, n_board = minimax(c, me, me, alpha, beta, depth+1)
				aval = min(aval, avalminmax)
				# print depth
				# print "BOARD: " + str(n_board)
				if aval < beta:
					beta = aval
				if alpha >= beta:
					return beta, c

			return aval, c

		else:
			# print "Max"

			aval = -sys.maxint-1
			# print board.board
			alpha_board = None
			print turn
			children = board.move(turn)

			if me == "r":
				turn = "y"
			else:
				turn = "r"

			print "CHILDREN: " + str(len(children))
			for c in children:
				avalminmax, n_board = minimax(c, turn, me, alpha, beta, depth+1)
				aval = min(aval, avalminmax)
				# print depth
				# print "BOARD: " + str(n_board)
				if aval > alpha:
					alpha = aval
				if alpha >= beta:
					return alpha, c

			return aval, c 
	else:
		return estado, board
def main():
	b = Board()
	b.startGame()
	# print b

	# children = b.move("r")
	me = "r"

	aval, board = minimax(b, "y", me, -sys.maxint-1,sys.maxint, 0)
	print aval
	print board


if __name__ == '__main__':
	main()





