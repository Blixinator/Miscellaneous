from Tkinter import *
import random
import time

from Piece import Piece

		

class App:
	def __init__(self, master):
		self.master = master
		self.rows = 20
		self.columns = 10
		self.initUI()

	def initUI(self):
		""

		self.labels = [[] for r in xrange(0,self.rows)]
		self.label_frame = Frame(self.master, bd=1, relief="solid")
		
		for r in xrange(0, self.rows):
			for c in xrange(0, self.columns):
				""
				l = Label(self.label_frame, bd=0.5, width=4, height=2, relief="ridge")
				l.grid(row=r, column=c)

				self.labels[r].append(l)

		self.label_frame.grid(row=0, column=0, sticky='nsew')




root = Tk()
root.title("Tetris")
# root.minsize(width=400, height=400)
app = App(root)
root.mainloop()