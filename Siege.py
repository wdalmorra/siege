from copy import deepcopy
import json

with open("vizinhos.json") as v_file:
	vizinhos = json.load(v_file)

with open("coletas.json") as c_file:
	coletas = json.load(c_file)

class Board():
	"""docstring for Board"""
	def __init__(self):
		self.amarelas = [None] * 16
		self.vermelhas = [None] * 16

	def copy(self, board):
		self.amarelas = deepcopy(board.amarelas)
		self.vermelhas = deepcopy(board.vermelhas)


