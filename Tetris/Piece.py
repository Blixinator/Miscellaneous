import random

class Piece(object):

	def __init__(self):
		""
		self.row = 0
		self.column = 0
		self.shape = None
		self.generate()


	def generate(self):
		self.shapes = [\
		[[1, 1, 1, 1]],\

		[[1, 1],\
		 [1, 1]],\

		[[0, 1, 0],\
		 [1, 1, 1]],\

		[[1, 1, 0],\
		 [0, 1, 1]],\

		[[0, 1, 1],\
		 [1, 1, 0]],\

		[[1, 0, 0],\
		 [1, 1, 1]],\

		[[0, 0, 1],\
		 [1, 1, 1]],\
		]

		self.shape = random.choice(self.shapes)
		print self.shape

	def rotate_left(self):
		""

	def rotate_right(self):
		""

	def move_down(self):
		""

class Board(object):
	def __init__(self):
		""

p = Piece()