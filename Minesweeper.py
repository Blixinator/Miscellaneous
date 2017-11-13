
from Tkinter import *
import random
import time
import tkFont
import threading

class MyButton(Button):
	def __int__(self, *args, **kwargs):
		Button.__init__(self, *args, **kwargs)
		self.revealed = False
		self.flagged = False


	def set_row(self, row):
		self.r = row

	def set_col(self, col):
		self.c = col

	def set_value(self, value):
		self.value = value

	def row(self):
		return self.r

	def col(self):
		return self.c

	def value(self):
		return self.value

	def set_flag(self, state):
		self.flagged = state

	def get_flag(self):
		return self.flagged



class App:
	def __init__(self, master):
		self.master = master
		# self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

		self.cheat_mode = False
		# self.cheat_mode = True

		self.rows = 10
		self.columns = 10
		self.mines = 15

		self.rows = 16
		self.columns = 16
		self.mines = 40

		self.mine_character = 'X'
		self.flag_character = 'F'

		self.colors = {1:"blue", 2:"green", 3:"red", 4:"purple", 5:"maroon", 6:"turquoise", 7:"black", 8:"gray"}

		self.left_mouse_down = False
		self.right_mouse_down = False

		self.shift_l_down = False

		self.buttons = None
		self.map = None

		self.flags = 0
		self.revealed = 0
		self.started = False

		self.elapsed = 0

		self.timer = threading.Timer(1.0, self.test)

		self.initUI()


	def initUI(self):
		f = Frame(self.master)
		self.menu_bar = Menu(self.master)
		self.master.config(menu=self.menu_bar)
		self.game_menu = Menu(self.menu_bar, tearoff=False)
		self.menu_bar.add_cascade(label="Game", menu=self.game_menu)

		self.game_menu.add_command(label='Beginner', command=lambda: self.set_difficulty('beginner'))
		self.game_menu.add_command(label='Intermediate', command=lambda: self.set_difficulty('intermediate'))
		self.game_menu.add_command(label='Expert', command=lambda: self.set_difficulty('expert'))
		self.game_menu.add_command(label='Custom', command=lambda: self.set_difficulty('custom'))
		

		self.top_frame = Frame(f)

		self.flag_tracker = Label(self.top_frame, text="{:0>3}".format(self.mines), width=3, bg='red')
		self.flag_tracker.pack(side='left')

		self.timer_label = Label(self.top_frame, text="999", width=3, bg='red')
		self.timer_label.pack(side='right')

		self.reset_button = Button(self.top_frame, text = "Reset", command=lambda r=self.rows, c=self.columns, m=self.mines: self.populate(r,c,m))
		self.reset_button.pack()

		self.top_frame.grid(row=0, sticky = "WE")

		self.button_frame = Frame(f)
		self.button_frame.grid(row=1, column=0, sticky='nsew')



		f.pack_propagate(0)
		f.pack(fill=BOTH)

		self.populate(rows=self.rows, columns=self.columns, mines=self.mines)

		self.test()


	def onExit(self):
		quit()

	def on_closing(self):
		# threading.Timer(1.0, self.test).cancel()
		self.timer.cancel()
		self.timer.join()
		self.master.destroy()
		# self.timer.cancel()
		quit()

	def test(self):
		if self.elapsed == 0:
			self.timer.start()
		if self.elapsed < 999:
			# print "!"
			try:
				self.elapsed += 1
				# print self.elapsed
				self.timer_label['text'] = "{:0>3}".format(999-self.elapsed)
			except TclError:
				self.timer.cancel()
				print "WHY DOESN'T THIS CANCEL?"
				""
		else:
			""

	def set_difficulty(self, difficulty):

		if difficulty == 'beginner':
			self.rows = 9
			self.columns = 9
			self.mines = 10
		elif difficulty == 'intermediate':
			self.rows = 16
			self.columns = 16
			self.mines = 40
		elif difficulty == 'expert':
			self.rows = 16
			self.columns = 30
			self.mines = 99
		elif difficulty == 'custom':
			# TODO
			return
		else:
			return

		self.populate(rows=self.rows, columns=self.columns, mines=self.mines)
		self.master.update()
		self.master.minsize(width=self.button_frame.winfo_width(), height=self.button_frame.winfo_height() + self.top_frame.winfo_height())
		self.master.maxsize(width=self.button_frame.winfo_width(), height=self.button_frame.winfo_height() + self.top_frame.winfo_height())


	def reset(self):
		self.started = False
		self.flags = 0
		self.revealed = 0
		self.flag_tracker.config(text="{:0>3}".format(self.mines))
		self.timer_label.config(text="999")

	def populate(self, rows, columns, mines, click_position=None):
		self.reset()

		"""Create a list of possible locations to place mines
		This removes the need to randomly pick tiles until you find one without a mine on it"""
		possible_mine_locations = range(0, self.rows*self.columns)
		if click_position != None:
			clicked_r, clicked_c = click_position
			possible_mine_locations.remove(clicked_r*self.columns+clicked_c)

		"MAYBE REDOING THIS WILL SPEED UP RESET"
		for widget in self.button_frame.winfo_children():
			widget.destroy()

		self.buttons = [[] for r in xrange(0,rows)]
		self.map = [[0]*self.columns for r in xrange(0,self.rows)]
		self.revealed_map = [[False]*self.columns for r in xrange(0,self.rows)]
		
		"""Place mines
		Select a random spot on the map. Add a mine if there isn't already there. Increment the surrounding tiles"""
		mines_placed = 0
		while mines_placed < self.mines:
			mine_position = random.choice(possible_mine_locations)
			possible_mine_locations.remove(mine_position)
			r = int(mine_position/( self.columns))
			c = mine_position % self.columns


			self.map[r][c] = self.mine_character
			for i in xrange(-1,2):
				for j in xrange(-1,2):
					if (i==0 and j==0) or not(0<=r+i<self.rows) or not(0<=c+j<self.columns):
						continue
			
					if self.map[r+i][c+j]!=self.mine_character:
						self.map[r+i][c+j]+=1

			mines_placed += 1

		"""Create Buttons"""
		for r in xrange(0, self.rows):
			for c in xrange(0, self.columns):


				b = MyButton(self.button_frame, text = "", width=2, command = lambda r=r, c=c: self.buttons[r][c].config(relief=SUNKEN))
				# b = MyButton(self.button_frame, text = "", width=2, command = lambda r=r, c=c: self.sink(r,c))

				b.set_row(r)
				b.set_col(c)

				"""Add the map to the top of all the buttons"""
				if self.cheat_mode == True:
					b.config(text=(self.map[r][c] if self.map[r][c]!=0 else " "))

				"""Add bindings for left, right, and both mouse button clicks"""
				b.bind("<Button-1>", lambda event: self.button_click2(event, 'left', True))
				b.bind("<Button-3>", lambda event: self.button_click2(event, 'right', True))
				b.bind("<ButtonRelease-1>", lambda event: self.button_click2(event, 'left', False))
				b.bind("<ButtonRelease-3>", lambda event: self.button_click2(event, 'right', False))
				b.bind("<Leave>", lambda event, r=r, c=c: self.hover_leave(event,r,c))
				b.bind("<B1-Motion>", lambda event: self.move_leave(event))
				b.config(font = tkFont.Font(family="Helvetica", size=12, weight="bold"))
				b.grid(row=r, column=c)
				
				self.buttons[r].append(b)

	def move_leave(self, event):
		
		event.widget.grab_release()
		widget = self.button_frame.winfo_containing(event.x_root, event.y_root)

		try:
			r = widget.row()
			c = widget.col()
		except AttributeError:
			return


		if self.left_mouse_down!=False and self.right_mouse_down!=False and self.buttons[r][c]['state']!='disabled':
			for i in xrange(-1,2):
				for j in xrange(-1,2):
					if not(0<=r+i<self.rows) or not(0<=c+j<self.columns):
						continue
					if self.buttons[r+i][c+j]['state']!='disabled':
						self.buttons[r+i][c+j]['relief']='sunken'

		widget.grab_set()
		if widget['state']!='disabled':
			widget['relief'] = 'sunken'
		

	# "Removing r, c from arguments added the bug the keeps buttons sunken"
	def hover_leave(self, event, r, c):

		for i in xrange(-1,2):
			for j in xrange(-1,2):
				if not(0<=r+i<self.rows) or not(0<=c+j<self.columns):
					continue
				if self.revealed_map[r+i][c+j] == False:
					self.buttons[r+i][c+j]['relief']='raised'



	
	"""Sink the button. Need to do this for the default command"""
	def sink(self, r, c):
		self.buttons[r][c]['relief'] = 'sunken'


	"""Should probably merge button_click and button_click2"""
	def button_click(self, r, c):

		for row in self.buttons:
			for e in row:
				e.grab_release()

		if self.started == False:
			if self.cheat_mode == False:
				self.populate(rows=self.rows, columns=self.columns, mines=self.mines, click_position=(r,c))
			self.started = True
			

		if self.revealed_map[r][c]==True:
			return

		self.buttons[r][c]['relief']='sunken'
		self.buttons[r][c].config( text=(self.map[r][c] if self.map[r][c]!=0 else " "))


		self.revealed+=1
		self.revealed_map[r][c] = True

		"""If all non-mine spaces are revealed"""
		if (self.rows*self.columns == self.mines + self.revealed):
			print "YOU WIN"

			self.win_condition()

		"""If a mine is clicked"""
		if self.map[r][c]==self.mine_character:
			print "BOOM!"
			self.buttons[r][c]['bg']='red'
			self.sink(r,c)
			self.buttons[r][c]['relief']='sunken'
			for row in xrange(0, self.rows):
				for column in xrange(0, self.columns):
					if self.map[row][column] == self.mine_character:
						self.buttons[row][column].config(state="disabled", text=self.mine_character)
					self.buttons[row][column].config(state="disabled")


		elif self.map[r][c]==0:
			for i in xrange(-1,2):
				for j in xrange(-1,2):
					if (i==0 and j==0) or not(0<=r+i<self.rows) or not(0<=c+j<self.columns):
						continue
					if self.map[r+i][c+j]!=self.mine_character and self.revealed_map[r+i][c+j] == False:
						self.button_click(r+i, c+j)
	

		else:
			self.buttons[r][c].config(fg=self.colors[self.map[r][c]])

	def button_click2(self, event, mouse, state):
		widget = self.button_frame.winfo_containing(event.x_root, event.y_root)
		r = widget.row()
		c = widget.col()

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
			"""If left&right mouse down, sink all adjacent cells"""
			if self.left_mouse_down and self.right_mouse_down and self.buttons[r][c]['state']!='disabled':
				for i in xrange(-1,2):
					for j in xrange(-1,2):
						if not(0<=r+i<self.rows) or not(0<=c+j<self.columns):
							continue
						if self.buttons[r+i][c+j]['state']!='disabled':
							self.buttons[r+i][c+j]['relief']='sunken'


		if state==False:
			# if self.left_mouse_down==False:
			self.buttons[r][c].grab_release()

			for i in xrange(-1,2):
				for j in xrange(-1,2):
					if not(0<=r+i<self.rows) or not(0<=c+j<self.columns):
							continue
					if self.buttons[r+i][c+j]['state']=='disabled' or self.revealed_map[r+i][c+j]==True:
						continue

					self.buttons[r+i][c+j]['relief']='raised'

			
	
			if self.left_mouse_down and self.right_mouse_down:
				# print 'both down'
				"BOTH DOWN"
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
						if str(flag_count) >= str(self.buttons[r][c]['text']):
							for i in xrange(-1,2):
								for j in xrange(-1,2):
									if (i==0 and j==0) or not(0<=r+i<self.rows) or not(0<=c+j<self.columns) or self.buttons[r+i][c+j]['state']=='disabled':
										continue
									self.button_click(r+i, c+j)


			elif self.left_mouse_down:
				# print 'left down'
				"LEFT DOWN"
				if self.buttons[r][c]['state']!='disabled':
					self.button_click(r,c)

			elif self.right_mouse_down:
				# print 'right down'
				"RIGHT DOWN"
				if self.revealed_map[r][c]==False:
					self.set_flag(r,c)
				else:
					""
					# print r,c,"!"

			self.left_mouse_down = False
			self.right_mouse_down = False

	"""Place a flag on top of a tile"""
	def set_flag(self, r, c):
		if self.started==False:
			return

		if self.buttons[r][c]['state']=="normal":
			self.buttons[r][c].config(state="disabled", text=self.flag_character)
			self.flags+=1
			self.flag_tracker.config(text="{:0>3}".format(self.mines-self.flags))
			

		elif self.buttons[r][c]['state']=="disabled" and self.buttons[r][c]['text']==self.flag_character:
			self.buttons[r][c].config(state="normal", text="")
			self.flags-=1
			self.flag_tracker.config(text="{:0>3}".format(self.mines-self.flags))

	def win_condition(self):
		# print "!"
		for r in xrange(0, self.rows):
			for c in xrange(0, self.columns):
				b = self.buttons[r][c]
				b.unbind("<Button-1>")
				b.unbind("<Button-3>")
				b.unbind("<ButtonRelease-1>")
				b.unbind("<ButtonRelease-3>")
				b.unbind("<Leave>")
				b.unbind("<B1-Motion>")
				b.config(command = "")
				if self.revealed_map[r][c]==False and self.buttons[r][c]['state']!='disabled':
					self.buttons[r][c]['state'] = 'disabled'


root = Tk()
root.title("Minesweeper")
app = App(root)

root.mainloop()