
from Tkinter import *
import random
import operator
import time
import tkFont as tkfont

def printf(s):
	print s

# class MyButton(Button):
# 	def __int__(self, *args, **kwargs):
# 		Button.__init__(self, *args, **kwargs)
# 		# self['revealed'] = False
# 		self.revealed = False

# 	def reveal(self):
# 		self.revealed = True

# 	def is_revealed(self):
# 		return self.revealed

class App:
	def __init__(self, master):
		self.master = master

		self.rows = 10
		self.columns = 10
		self.bombs = 15

		self.colors = {1:"blue", 2:"green", 3:"red", 4:"purple", 5:"maroon", 6:"turquoise", 7:"black", 8:"gray"}

		self.left_mouse_down = False
		self.right_mouse_down = False

		self.left_mouse_pressed = False
		self.right_mouse_pressed = False

		self.buttons = None
		self.map = None

		self.flags = 0
		self.revealed = 0
		self.started = False

		self.initUI()
		self.populate(rows=self.rows, columns=self.columns, bombs=self.bombs)
		
		

	def initUI(self):
		f = Frame(self.master, height=400, width=400)
		menubar = Menu(self.master)
		self.master.config(menu=menubar)
		fileMenu = Menu(menubar)
		fileMenu.add_command(label="Exit", command=self.onExit)
		menubar.add_cascade(label="File", menu=fileMenu)

		self.button_frame = Frame(f)
		self.button_frame.grid(row=1, column=1)

		self.bold_font = tkfont.Font(family="Helvetica", size=12, weight="bold")

		l = Label(f, text = "TEST1234567890\nTEST\nTEST", bg='red')


		l.grid(row=1, column=0)
		

		self.row_entry = Entry(f)
		self.row_entry.grid(row=0, column=0)

		self.column_entry = Entry(f)
		self.column_entry.grid(row=0, column=1)

		self.bomb_entry = Entry(f)
		self.bomb_entry.grid(row=0, column=2)

		self.reset_button = Button(f, text = "Reset", command=lambda r=self.rows, c=self.columns, b=self.bombs: self.populate(r,c,b))
		self.reset_button.grid(row=2, column=1)

		f.pack_propagate(0)
		f.pack(fill=BOTH)

	def onExit(self):
		quit()

	def reset(self):
		self.started = False
		self.flags = 0
		self.revealed = 0

	def populate(self, rows, columns, bombs, click_position=None):
		self.reset()

		for widget in self.button_frame.winfo_children():
			widget.destroy()
		self.buttons = [[] for r in xrange(0,rows)]
		self.map = [[0]*columns for r in xrange(0,rows)]
		self.revealed_map = [[False]*columns for r in xrange(0,rows)]
		
		"""Place bombs
		Select a random spot on the map. Add a bomb if there isn't already there. Increment the surrounding tiles"""
		bombs_placed = 0
		while bombs_placed < bombs:
			r = random.randint(0, rows-1)
			c = random.randint(0, columns-1)
			if self.map[r][c] != "*" and (r,c)!=click_position:
				self.map[r][c] = "*"
				for i in xrange(-1,2):
					for j in xrange(-1,2):
						if (i==0 and j==0) or not(0<=r+i<self.rows) or not(0<=c+j<self.columns):
							continue
						try:
							if self.map[r+i][c+j]!="*":
								self.map[r+i][c+j]+=1
						except IndexError:
							""
				bombs_placed += 1

		"""Create Buttons"""
		for r in xrange(0, rows):
			for c in xrange(0, columns):

				# b = Button(self.button_frame, text = "", width=2, command=lambda r=r, c=c: self.button_click(r,c))
				# b = Button(self.button_frame, text = "", width=2, command = lambda r=r, c=c: self.buttons[r][c].config(relief=SUNKEN))
				b = Button(self.button_frame, text = "", width=2, command = lambda r=r, c=c: self.sink(r,c))
				# b = Button(self.button_frame, text = "", width=2)

				"""Add the map to the top of all the buttons"""
				# b.config(text=(self.map[r][c] if self.map[r][c]!=0 else " "))

				"""Add bindings for left, right, and both mouse button clicks"""
				b.bind("<Button-1>", lambda event, r=r, c=c: self.button_click2(event, 'left', True,r,c))
				b.bind("<Button-3>", lambda event, r=r, c=c: self.button_click2(event, 'right', True,r,c))
				b.bind("<ButtonRelease-1>", lambda event, r=r, c=c: self.button_click2(event, 'left', False,r,c))
				b.bind("<ButtonRelease-3>", lambda event, r=r, c=c: self.button_click2(event, 'right', False,r,c))

				# b.bind("<Enter>", lambda event, r=r, c=c: self.test(event, r,c))

				b.config(font = self.bold_font)
				b.grid(row=r, column=c)
				
				self.buttons[r].append(b)

	# def test(self, event, r, c):
	# 	print self.left_mouse_down, self.right_mouse_down


	"""Sink the button. Need to do this for the default command"""
	def sink(self, r, c):
		self.buttons[r][c]['relief'] = 'sunken'


	"""Should probably merge button_click and button_click2"""
	def button_click(self, r, c):
		if self.started == False:
			self.populate(rows=self.rows, columns=self.columns, bombs=self.bombs, click_position=(r,c))
			self.started = True

		if self.revealed_map[r][c]==True:
			return

		self.buttons[r][c]['relief']='sunken'
		self.buttons[r][c].config( text=(self.map[r][c] if self.map[r][c]!=0 else " "))


		self.revealed+=1
		self.revealed_map[r][c] = True

		"""If all non-bomb spaces are revealed"""
		if (self.rows*self.columns == self.bombs + self.revealed):
			print "YOU WIN"

		"""If a bomb is clicked"""
		if self.map[r][c]=="*":
			print "BOOM!"
			for row in xrange(0, self.rows):
				for column in xrange(0, self.columns):
					if self.map[row][column] == "*":
						self.buttons[row][column].config(state="disabled", text="*")
					self.buttons[row][column].config(state="disabled")


		elif self.map[r][c]==0:
			for i in xrange(-1,2):
				for j in xrange(-1,2):
					if (i==0 and j==0) or not(0<=r+i<self.rows) or not(0<=c+j<self.columns):
						continue
					if self.map[r+i][c+j]!="*" and self.revealed_map[r+i][c+j] == False:
						self.button_click(r+i, c+j)
	

		else:
			self.buttons[r][c].config(fg=self.colors[self.map[r][c]])

	def button_click2(self, event, mouse, state, r, c):
		if state == True:
			if self.left_mouse_down and self.left_mouse_down <= time.time():
				self.left_mouse_down = False
			if self.right_mouse_down and self.right_mouse_down <= time.time():
				self.right_mouse_down = False

			if mouse == 'left' and state==True:
				self.left_mouse_down = time.time() + 500
			if mouse == 'right' and state==True:
				self.right_mouse_down = time.time() + 500

			# print self.left_mouse_down, self.right_mouse_down

		if state==False:
			if self.left_mouse_down and self.right_mouse_down:
				print 'both down'
				if self.buttons[r][c]['state']!='disabled':
					if self.revealed_map[r][c]==True:
						"""Count the number of flags in the adjacent tiles"""
						flag_count = 0
						for i in xrange(-1,2):
							for j in xrange(-1,2):
								if (i==0 and j==0) or not(0<=r+i<self.rows) or not(0<=c+j<self.columns):
									continue
								if self.buttons[r+i][c+j]['state']=='disabled':
									flag_count+=1
						"""If the number of flags is equal to the tile number, reveal the surrounding tiles"""
						if str(flag_count) == str(self.buttons[r][c]['text']):
							for i in xrange(-1,2):
								for j in xrange(-1,2):
									if (i==0 and j==0) or not(0<=r+i<self.rows) or not(0<=c+j<self.columns) or self.buttons[r+i][c+j]['state']=='disabled':
										continue
									self.button_click(r+i, c+j)


			elif self.left_mouse_down:
				print 'left down'
				if self.buttons[r][c]['state']!='disabled':
					self.button_click(r,c)

			elif self.right_mouse_down:
				print 'right down'
				self.set_flag(r,c)

			self.left_mouse_down = False
			self.right_mouse_down = False

	"""Place a flag on top of a tile"""
	def set_flag(self, r, c):
		if self.started==False:
			return

		if self.buttons[r][c]['state']=="normal":
			self.buttons[r][c].config(state="disabled", text="F")
			self.flags+=1
			if (self.flags == self.bombs) and (self.rows*self.columns == self.flags + self.revealed):
				print "YOU WIN"


		elif self.buttons[r][c]['state']=="disabled" and self.buttons[r][c]['text']=="F":
			self.buttons[r][c].config(state="normal", text="")
			self.flags-=1



root = Tk()
root.title("Minesweeper")
root.minsize(width=400, height=400)
app = App(root)
root.mainloop()