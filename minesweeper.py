# Student: Josh Fiedler
# Portfolio assignment: Minesweeper game from scratch
import tkinter
from tkinter import *
import random 
import collections
import time
# Helpful sources:
#https://www.python-course.eu/tkinter_canvas.php#:~:text=The%20Canvas%20widget%20supplies%20graphics,various%20kinds%20of%20custom%20widgets.
#http://zetcode.com/tkinter/drawing/
#https://www.geeksforgeeks.org/python-check-if-two-lists-are-identical/

class Tile:
	def __init__(self, x, y, tile_id, assigned_game):
		self.x = x # Every tile is positioned via x and y coordinates
		self.y = y
		self.i = 0 # i and j coordinates for handling edge cases with neighbors
		self.j = 0
		self.tile_id = "Tile"+str(tile_id) # Every tile has a unique id
		# Lines to randomly generate probability of a mine, can be changed via difficulty setting (maybe)
		self.mine_prob = random.randint(1,4)
		if self.mine_prob == 3:
			self.mine = True
		else:
			self.mine = False
		self.flag = False # Variable saves if a tile is flagged by the user
		#self.flag_shape = None
		self.cover = True # Every tile starts covered with another rectangle 
		# Neighbor variables save which tile is adjacent in 8 directions, similar to a linked list
		self.neighbor_N = None
		self.neighbor_E = None
		self.neighbor_W = None
		self.neighbor_S = None
		self.neighbor_NW = None
		self.neighbor_NE = None
		self.neighbor_SW = None
		self.neighbor_SE = None
		self.neighbor_list = [] # Organize all neighboring tiles in one place 
		self.color = "gray" # Color of the base tiles
		self.number = 0 # Default number of neighboring mines
		self.game = assigned_game # Saves which game object contains the tiles
	def draw_tile(self):
		# Draws, for all tiles, a base layer rectangle.
		self.game.w.create_rectangle(self.x,self.y,self.x+20,self.y+20,fill = self.color, tags = self.tile_id)
	def draw_mine(self):
		# If a tile has a mine, this draws the mine in the center of the tile.
		if self.mine == True:
			self.game.w.create_rectangle(self.x+5,self.y+5,self.x+10,self.y+10,fill = "black")
	def draw_text(self):
		# Draw text displays the number of mines neighboring a tile, and centers
		# the number in the tile.
		if self.mine == False:
			self.game.w.create_text(self.x+10,self.y+10,text = self.number)
	def draw_cover(self, param):
		# Draw cover creates a rectangle over every tile. Param is the color
		if self.cover == True:
			self.game.w.create_rectangle(self.x,self.y,self.x+20,self.y+20,fill = param, tags = self.tile_id)
	def draw_flag(self,event):
		# Draw flag will display a red flag on tiles right clicked, or
		# remove the flag graphic if the tile has one. 
		if self.cover == True:
			if self.flag == False:
				self.flag = True
				points = [self.x+5,self.y+5,self.x+5,self.y+15,self.x+10,self.y+10]
				self.flag_shape = self.game.w.create_polygon(points,outline="black",fill="red",width=1)
			else:
				self.flag = False
				self.game.w.delete(self.flag_shape)
				
	def print_neighbors(self):
		# Prints neighbors of a selected tile, function only needed for testing and is called from the printID
		# function.
		if self.neighbor_NW:
			print("NW:",self.neighbor_NW.tile_id,end=" ")
		else:
			print("NW: None",end=" ")
		if self.neighbor_N:
			print("North:",self.neighbor_N.tile_id,end=" ")
		else:
			print("North: None",end=" ")
		if self.neighbor_NE:
			print("NE:",self.neighbor_NE.tile_id)
		else:
			print("NE: None")
		if self.neighbor_W:
			print("West:",self.neighbor_W.tile_id,end=" ")
		else:
			print("West: None",end=" ")
			
		print("Self:",self.tile_id,end = " ")
		
		if self.neighbor_E:
			print("East:",self.neighbor_E.tile_id)
		else:
			print("East: None")
		if self.neighbor_SW:
			print("SW:",self.neighbor_SW.tile_id,end=" ")
		else:
			print("SW: None",end=" ")
		if self.neighbor_S:
			print("South:",self.neighbor_S.tile_id,end=" ")
		else:
			print("South: None",end=" ")
		if self.neighbor_SE:
			print("SE:",self.neighbor_SE.tile_id)
		else:
			print("SE: None")
	def show_neighbors(self,tile):
		# Show neighbors is a recursive function to reveal all surrounding 
		# tiles if a tile neighboring 0 mines is clicked.
		
		# Check the current tile's list of neighbors for other 0's
		for i in range(len(tile.neighbor_list)):
			curr = tile.neighbor_list[i]
			
			# If neighbor is a 0 and has not been visited by the recursive function, reveal the tile.
			if curr.number == 0 and curr not in self.game.visited_tiles:
				
				curr.cover = False
				if curr not in self.game.visited_tiles:
					# Append to the list of visited tiles 
					self.game.visited_tiles.append(curr)
				curr.draw_tile()
				curr.draw_cover(None)
				# Call the recursive function again 
				tile.show_neighbors(curr)
			# If neighbor is not a 0, reveal tile but end recursive calls
			else:
				curr.cover = False
				curr.draw_tile()
				
				if curr.number > 0:
					curr.draw_text()
				curr.draw_cover(None)
				if curr not in self.game.visited_tiles:
					# Append to the list of visited tiles 
					self.game.visited_tiles.append(curr)
	def printID(self,event):
		# This function handles all events related to clicking a tile on the puzzle board.
		# Only unflagged tiles are clickable
		if self.flag == False:
			
			self.cover = False # Remove cover of a clicked tile
			
			if self.mine == True:
				# If a mine is clicked, base tile changes to red and endgame is called.
				print("Game over")
				self.color = "red"
				self.game.endgame()
			else:
				# append to list of safe mines
				self.game.visited_tiles.append(self)
				#print("Visited",len(self.game.visited_tiles),"tiles")
			# Redraw the tile, including the mine if applicable
			self.draw_tile()
			self.draw_mine()
			self.draw_cover(None)
			if self.number > 0:
				# Show the tile's text if above 0
				self.draw_text()
			else:
				# Clicking a tile of 0 neighboring mines calls the recursive function.
				if self.mine == False:
					self.show_neighbors(self)
			#if collections.Counter(self.game.visited_tiles) == collections.Counter(self.game.safe_tiles):
			if len(self.game.safe_tiles) == len(self.game.visited_tiles):
				print("**** Victory ****")
				self.game.end_time = time.time()
				elapsed_time = (self.game.end_time - self.game.start_time)
				elapsed_time = '%.2f' % (elapsed_time)
				self.game.assigned_menu.winning_window(elapsed_time)
				
class Game:
	def __init__(self,boardx,boardy,menus):
		self.x = boardx # Sets x,y game board dimensions
		self.y = boardy 
		self.start_time = time.time()
		self.end_time = 0
		self.tile_list = [] # Generic list of all tiles for testing
		self.safe_tiles = [] # List of all non-mine tiles, needed for determining win condition
		self.visited_tiles = [] # List storing all mines clicked by user
		self.w = None # Sets the tkinter canvas of the game
		self.assigned_menu = menus # Passes menu object this game object interacts with
	def create_rects(self):
		# Function creates the puzzle board. 
		# Game dimensions assigned by game object from fixed menu choices.
		
		j = 0
		x = 10
		y = 10
		tile_id = 1
		
		print("Game dimens:",self.x,self.y)
		# j variable sets each row of tiles
		while j < self.y:
			i = 0
			x = 10
			# i variable draws each tile in row
			while i < self.x:
				# create tile object
				#print("tile id var:",tile_id)
				newTile = Tile(x,y,tile_id,self)
				newTile.i = i
				newTile.j = j
				newTile.draw_tile()
				newTile.draw_mine()
				newTile.draw_cover("white")
				
				# define neighbors of tile 
				if tile_id > 1:
					# Set all west neighbors
					if (i)%(self.x) == 0:
						newTile.neighbor_W = None
						newTile.neighbor_NW = None
						newTile.neighbor_SW = None
					else:
						newTile.neighbor_W = self.tile_list[((j*self.x)+i)-1]
						newTile.neighbor_list.append(self.tile_list[((j*self.x)+i)-1])
					# Set all east neighbors 
					if (tile_id-1)%(self.x) == 0:
						newTile.neighbor_E = None # no tiles east of this
						newTile.neighbor_NE = None
						newTile.neighbor_SE = None
						
					else:
						self.tile_list[((j*self.x)+i)-1].neighbor_E = newTile
						self.tile_list[((j*self.x)+i)-1].neighbor_list.append(newTile)
				if tile_id > self.x:
					# Set all north neighbors
					if j == 0:
						# Condition for first row
						newTile.neighbor_N = None
						newTile.neighbor_NE = None
						newTile.neighbor_NW = None
					else:
						newTile.neighbor_N = self.tile_list[((j*self.x)+i)-self.x]
						newTile.neighbor_list.append(self.tile_list[((j*self.x)+i)-self.x])
						
						if newTile.i == (self.x-1): # Edge case: last column has no NE tiles
							newTile.neighbor_NE = None
						else:
							newTile.neighbor_NE = self.tile_list[(((j*self.x)+i)-self.x)+1]
							newTile.neighbor_list.append(self.tile_list[(((j*self.x)+i)-self.x)+1])
						if newTile.i == 0: # Edge case: first column has no NW tiles
							newTile.neighbor_NW = None
						else:
							newTile.neighbor_NW = self.tile_list[(((j*self.x)+i)-self.x)-1]
							newTile.neighbor_list.append(self.tile_list[(((j*self.x)+i)-self.x)-1])
					if j < (self.y):
						# Set all south neighbors
						self.tile_list[(tile_id-1) - self.x].neighbor_S = newTile
						self.tile_list[(tile_id-1) - self.x].neighbor_list.append(newTile)
						
						if self.tile_list[((tile_id-1) - self.x)+1].i == 0:
							self.tile_list[((tile_id-1) - self.x)+1].neighbor_SW = None
						else:
							self.tile_list[((tile_id-1) - self.x)+1].neighbor_SW = newTile
							self.tile_list[((tile_id-1) - self.x)+1].neighbor_list.append(newTile)
						if self.tile_list[((tile_id-1) - self.x)-1].i == (self.x-1): # No west tiles = no NW tiles
							self.tile_list[((tile_id-1) - self.x)-1].neighbor_SE = None
						else:
							self.tile_list[((tile_id-1) - self.x)-1].neighbor_SE = newTile
							self.tile_list[((tile_id-1) - self.x)-1].neighbor_list.append(newTile)
							
					if j == (self.y):
						# Condition for last row
						# no tiles south 
						newTile.neighbor_S = None
						newTile.neighbor_SE = None
						newTile.neighbor_SW = None
						
				# Bind button events to tiles: Left click (button 1) and
				# right click (button 3) for revealing tiles or flagging tiles.
				self.w.tag_bind(newTile.tile_id,"<Button-1>",newTile.printID)
				self.w.tag_bind(newTile.tile_id,"<Button-3>",newTile.draw_flag)
				# Append the tile to list of all tiles 
				self.tile_list.append(newTile)
				if newTile.mine == False:
					# If there is no mine, append to list of safe tiles
					self.safe_tiles.append(newTile)
				# increment column
				x += 20
				i += 1
				tile_id += 1
			# increment row
			y += 20
			j += 1
		# once all mines are created, calls the function to update text on mines
		self.update_mine_text()
		
	def update_mine_text(self):
		# Function to calculate number of mines adjacent to a tile
		for i in range(len(self.tile_list)):
			curr_tile = self.tile_list[i]
			
			mine_total = 0
			if curr_tile.neighbor_NE:
				if curr_tile.neighbor_NE.mine == True:
					mine_total += 1
			if curr_tile.neighbor_N:
				if curr_tile.neighbor_N.mine == True:
					mine_total += 1
			if curr_tile.neighbor_NW:
				if curr_tile.neighbor_NW.mine == True:
					mine_total += 1
			if curr_tile.neighbor_E:
				if curr_tile.neighbor_E.mine == True:
					mine_total += 1
			if curr_tile.neighbor_W:
				if curr_tile.neighbor_W.mine == True:
					mine_total += 1
			if curr_tile.neighbor_SE:
				if curr_tile.neighbor_SE.mine == True:
					mine_total += 1
			if curr_tile.neighbor_S:
				if curr_tile.neighbor_S.mine == True:
					mine_total += 1
			if curr_tile.neighbor_SW:
				if curr_tile.neighbor_SW.mine == True:
					mine_total += 1
			if mine_total > 0:
				# Updates the tile's number to the amount of adjacent mines
				curr_tile.number = mine_total
	def refresh(self):
		# Function restarts the existing game
		for i in range(len(self.tile_list)):
			self.start_time = time.time()
			self.tile_list[i].color = "gray"
			self.tile_list[i].cover = True
			self.visited_tiles.clear()
			self.tile_list[i].draw_tile()
			self.tile_list[i].draw_mine()
			self.tile_list[i].draw_cover("white")
	def endgame(self):
		# Function handles the end game state
		for i in range(len(self.tile_list)):
			# Reveal all mines in the end
			if self.tile_list[i].mine == True:
				
				self.tile_list[i].draw_tile()
				self.tile_list[i].draw_mine()
				self.tile_list[i].draw_cover(None)
	def erase_board(self):
		# Function destroys the current game and calls the menu to create a new puzzle.
		self.tile_list.clear()
		self.visited_tiles.clear()
		self.safe_tiles.clear()
		self.w.destroy()
		self.assigned_menu.master.withdraw()
		self.assigned_menu.first_menu.update()
		self.assigned_menu.first_menu.deiconify()
		self.assigned_menu.setup_puzzle()
		
class Menus:
	def __init__(self,master):
		#self.running = True
		self.master = master		
		self.master.withdraw()
		self.first_menu = Toplevel(self.master)
		self.second_menu = Toplevel(self.master)
		self.second_menu.withdraw()
		self.third_menu = Toplevel(self.master)
		self.third_menu.withdraw()
		self.tkvar = StringVar(self.first_menu)
		
	#def on_close(self):
	#	self.running = False
	def winning_window(self,elapsed_time):
		self.second_menu.update()
		self.second_menu.deiconify()
		Label(self.second_menu,text = "Win with time "+str(elapsed_time)+" seconds").grid(row = 0,column = 0)
	def rules_window(self):
		self.third_menu.update()
		self.third_menu.deiconify()
		Label(self.third_menu,text = "Left button click to \n clear a tile, \n right button click to \n flag a tile. \n Clear all non-mines \n to win.").grid(row=0,column=0) 
	def setup_puzzle(self):
		# While running, this menu shows 
		self.first_menu.wm_title("Setup")
		
		choices = ("10 x 10","10 x 20","20 x 20","20 x 30", "30 x 30")
		self.tkvar.set(choices[0])
		
		first_menu = OptionMenu(self.first_menu,self.tkvar,*choices)
		
		Label(self.first_menu, text = "Set puzzle size").grid(row = 1, column = 0)
		first_menu.grid(row = 1, column = 1)
		
		first_b1 = Button(self.first_menu,text = "Start",command=lambda:self.puzzle_create(self.tkvar))
		first_b1.grid(row = 2, column = 0)
		
	def puzzle_create(self,answer):
		root.update()
		self.first_menu.withdraw()
		self.master.update()
		self.master.deiconify()
		#user_answer = answer.get()
		#print(user_answer)
	
		# Get the user's choice of game size
		user_ans = self.tkvar.get()
		
		# Extract game dimensions from user choice, save in board_x and board_y
		user_ans = user_ans.split("x")
		
		for i in range(len(user_ans)):
			user_ans[i] = user_ans[i].strip(" ")
		
		board_x = int(user_ans[1])
		board_y = int(user_ans[0])
		# Create a new game object
		mygame = Game(board_x,board_y,self)
		
		# Set the size for the canvas widget
		canvas_width = 20*board_x+20
		canvas_height = 20*board_y+20
		# Create the canvas
		mygame.w = Canvas(self.master,
				  width = canvas_width,
			   height = canvas_height)
		self.master.wm_title("Minesweeper")
		
		mygame.w.grid(row = 0, column = 0)
		mygame.create_rects() # Creates all tiles in the game
		
		# Button to restart current puzzle 
		b1 = Button(self.master,text="Restart",command=lambda:mygame.refresh())
		b1.grid(row=0,column=2)
		
		# Button to start a new puzzle
		b2 = Button(self.master,text="New Puzzle",command=lambda:mygame.erase_board())
		b2.grid(row=1,column=2)
		
		# Button for the rules
		b3 = Button(self.master,text="Rules",command=self.rules_window)
		b3.grid(row=2,column=2)
	
	def ask_quit(self):
		# Closes out all windows
		self.first_menu.destroy()
		self.master.destroy()


# Create the root tkinter window
root = Tk()
# Create menu object and start the puzzle
mymenu = Menus(root)

mymenu.setup_puzzle()
# Condition for close out of top level menu
mymenu.first_menu.protocol("WM_DELETE_WINDOW", mymenu.ask_quit)
# Runs the program
root.mainloop()
