
from Tkinter import *
import random
import operator
import time
import tkFont as tkfont

def printf(s):
	print s

class App:
	def __init__(self, master):
		self.master = master

		self.rows = 10
		self.columns = 10
		self.bombs = 15

		self.test = False

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
		# self.button_frame.place(in_=f, anchor="c", relx=.5, rely=.5)
		self.button_frame.grid(row=1, column=1)

		# self.button_frame = Frame(f)
		# self.button_frame.pack(fill=BOTH, anchor="c")
		self.bold_font = tkfont.Font(family="Helvetica", size=12, weight="bold")

		l = Label(f, text = "TEST1234567890\nTEST\nTEST", bg='red')


		l.grid(row=1, column=0)
		# l.bind("<Button-1>", self.set('left', True))
		# l.bind("<Button-3>", self.set('right', True))
		# l.bind("<ButtonRelease-1>", self.set('left', False))
		# l.bind("<ButtonRelease-3>", self.set('right', False))

		l.bind("<Button-1>", lambda x: self.left_right_click('left', True))
		l.bind("<Button-3>", lambda x: self.left_right_click('right', True))
		l.bind("<ButtonRelease-1>", lambda x: self.left_right_click('left', False))
		l.bind("<ButtonRelease-3>", lambda x: self.left_right_click('right', False))

		# l.bind("<Button-1>", self.onAnyofTwoPressed)
		# l.bind("<Button-3>", self.onAnyofTwoPressed)

		# l.bind("<ButtonRelease-1>", self.resetPressedState)
		# l.bind("<ButtonRelease-3>", self.resetPressedState)




		# l.bind("<Button-1><Button-3>", self.test)
		# l.bind("<1>", self.lclick)
		# l.bind("<ButtonRelease-1>", self.lclick)
		# l.bind("<ButtonRelease-1>", lambda x: printf("x"))
		# l.bind("<ButtonRelease-1><ButtonRelease-3>", lambda x: printf("x"))
		# l.bind("<ButtonRelease-1>", lambda x: self.set("left", True))
		# l.bind("<1>", lambda x: self.mouse_down=True)



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
		""

	def onAnyofTwoPressed(self, event):
		if self.left_mouse_pressed and self.left_mouse_pressed <= time.time():
			self.left_mouse_pressed = False

		if self.right_mouse_pressed and self.right_mouse_pressed <= time.time():
			self.right_mouse_pressed = False

		if event.num==1:
			self.left_mouse_pressed = time.time() + 500
		if event.num==3:
			self.right_mouse_pressed = time.time() + 500


	def resetPressedState(self, event):
		if self.left_mouse_pressed and self.right_mouse_pressed:
			print 'both pressed'
		elif self.left_mouse_pressed:
			print 'left pressed'
		elif self.right_mouse_pressed:
			print 'right pressed'
		self.left_mouse_pressed = False
		self.right_mouse_pressed = False



	def left_right_click(self, mouse, state):
		if state == True:
			if self.left_mouse_down and self.left_mouse_down <= time.time():
				self.left_mouse_down = False
			if self.right_mouse_down and self.right_mouse_down <= time.time():
				self.right_mouse_down = False

			if mouse == 'left' and state==True:
				self.left_mouse_down = time.time() + 500
			if mouse == 'right' and state==True:
				self.right_mouse_down = time.time() + 500
		if state==False:
	
			if self.left_mouse_down and self.right_mouse_down:
				print 'both down'
			elif self.left_mouse_down:
				print 'left down'
			elif self.right_mouse_down:
				print 'right down'

			self.left_mouse_down = False
			self.right_mouse_down = False

	




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
		
		bombs_placed = 0
		while bombs_placed < bombs:
			r = random.randint(0, rows-1)
			c = random.randint(0, columns-1)
			if self.map[r][c] != "*" and (r,c)!=click_position:
				self.map[r][c] = "*"
				for i in xrange(-1,2):
					for j in xrange(-1,2):
						# if i==0 and j==0:
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

				b = Button(self.button_frame, text = "", width=2, command=lambda r=r, c=c: self.button_click(r,c))
				# b = Button(self.button_frame, text = "", width=2)
				# b = Button(self.button_frame, text=(self.map[r][c] if self.map[r][c]!=0 else " "), width=2, command=lambda r=r, c=c: self.button_click(r,c))
				

				# b.bind("<Button-1>", lambda event, r=r, c=c: self.button_click2(event, 'left', True,r,c))
				# b.bind("<Button-3>", lambda event, r=r, c=c: self.button_click2(event, 'right', True,r,c))
				# b.bind("<ButtonRelease-1>", lambda event, r=r, c=c: self.button_click2(event, 'left', False,r,c))
				# b.bind("<ButtonRelease-3>", lambda event, r=r, c=c: self.button_click2(event, 'right', False,r,c))

				b.bind("<Button-3>", lambda event, r=r, c=c: self.set_flag(event,r,c))

				b.config(font = self.bold_font)
				b.grid(row=r, column=c)
				
				self.buttons[r].append(b)


	def button_click(self, r, c):

		if self.buttons[r][c]["relief"]=="sunken":
			return

		if self.started == False:
			self.populate(rows=self.rows, columns=self.columns, bombs=self.bombs, click_position=(r,c))
			self.started = True

		# self.buttons[r][c].config(state="disabled", relief=SUNKEN, text=(self.map[r][c] if self.map[r][c]!=0 else " "))
		self.buttons[r][c].config(relief=SUNKEN, text=(self.map[r][c] if self.map[r][c]!=0 else " "))
		self.revealed+=1

		if (self.rows*self.columns == self.bombs + self.revealed):
				print "YOU WIN"
				# print self.flags, self.revealed

		if self.map[r][c]=="*":
			print "BOOM!"
			# self.populate(rows=self.rows, columns=self.columns, bombs=self.bombs)
			for row in xrange(0, self.rows):
				for column in xrange(0, self.columns):
					# self.buttons[row][column].config(state="disabled", text=(self.map[row][column] if self.map[row][column]!=0 else " "))
					if self.map[row][column] == "*":
						self.buttons[row][column].config(state="disabled", text="*")
					self.buttons[row][column].config(state="disabled")


		elif self.map[r][c]==0:
			for i in xrange(-1,2):
				for j in xrange(-1,2):
					# if not(i==0 or j==0) or not(0<=r+i<self.rows) or not(0<=c+j<self.columns):
					if (i==0 and j==0) or not(0<=r+i<self.rows) or not(0<=c+j<self.columns):
						continue
					# try:
					if self.map[r+i][c+j]!="*" and self.buttons[r+i][c+j]['relief']=='raised':
						self.button_click(r+i, c+j)
						# if self.map[r+i][c+j] not in ('*', 0):
						# 	self.buttons[r+i][c+j].config(relief=SUNKEN, text=(self.map[r+i][c+j] if self.map[r+i][c+j]!=0 else " "))
						# 	self.buttons[r+i][c+j].config(fg=self.colors[self.map[r+i][c+j]])

					# except IndexError:
					# 	""

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
		if state==False:
	
			if self.left_mouse_down and self.right_mouse_down:
				print 'both down'
			elif self.left_mouse_down:
				print 'left down'
				# self.button_click(r,c)
			elif self.right_mouse_down:
				print 'right down'
				self.set_flag(event,r,c)

			self.left_mouse_down = False
			self.right_mouse_down = False

		print r, c


	def test(self, event):
		print "clicked at", event.x, event.y

	def set_flag(self, event, r, c):
		if self.buttons[r][c]["relief"]=="sunken":
			return

		if self.buttons[r][c]['state']=="normal":
			self.buttons[r][c].config(state="disabled", text="F")
			self.flags+=1
			if (self.flags == self.bombs) and (self.rows*self.columns == self.flags + self.revealed):
				print "YOU WIN"


		elif self.buttons[r][c]['state']=="disabled" and self.buttons[r][c]['text']=="F":
			self.buttons[r][c].config(state="normal", text="")
			self.flags-=1

		# print r,c


	


root = Tk()
root.title("Minesweeper")
root.minsize(width=400, height=400)
app = App(root)
root.mainloop()