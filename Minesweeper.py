import random
import copy
import tkinter as tk
from tkinter import *

class Gui(tk.Tk):

	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.cells = {}
		self.text = {}
		self.game = Minesweeper()
		self.cell_width = 15
		self.cell_height = 15
		self.left_mouse_pressed = False
		self.right_mouse_pressed = False
		self.colordict = {'0':'#FAFAFA','1':'#8181F7','2':'#088A29','3':'#FE2E2E','4':'#08088A','5':'#8A0808','6':'#01DFD7', '7':'#000000', '8':'#848484'}
		self.bgcolordict = {'B':'#FA5858','F':'#A9BCF5',' ':'#D8D8D8','W':'#DF0101'}
		self.start()

	def start(self):
		self.v = StringVar()
		self.width = self.game.width
		self.height = self.game.height
		self.screen_width = (self.width + 2)*self.cell_width
		self.screen_height = (self.height + 2)*self.cell_height
		self.startButton = tk.Button(self, text='Start a new game', command=lambda: self.restart())
		self.startButton.pack()
		self.canvas = tk.Canvas(self, width=self.screen_width, height=self.screen_height + 60, borderwidth=0, highlightthickness=0)
		self.canvas.pack(side="top", fill="both", expand="true")
		self.drawBoard()
		self.pointsText = tk.Label(self, textvariable=self.v)
		self.pointsText.pack()
		self.v.set('New game! \nMines: ' + str(self.game.minesleft))


	def drawBoard(self):
		offsetx = self.cell_width
		offsety = self.cell_height
		for x in range(self.width):
			for y in range(self.height):
				x1 = x * self.cell_width + offsetx
				y1 = y * self.cell_height + offsety
				x2 = x1 + self.cell_width
				y2 = y1 + self.cell_height
				self.cells[(x,y)] = self.canvas.create_rectangle(x1,y1,x2,y2, fill='#D8D8D8', tags='rect')
				self.text[(x,y)] = self.canvas.create_text(x1+7.5, y1+7.5, anchor=CENTER, text=" ")
				self.canvas.tag_bind(self.text[(x,y)], '<Button-1>', lambda event, x=x, y=y, press=1:self.onAnyofTwoPressed(x, y, press))
				self.canvas.tag_bind(self.text[(x,y)], '<Button-2>', lambda event, x=x, y=y, press=2:self.onAnyofTwoPressed(x, y, press))
				self.canvas.tag_bind(self.text[(x,y)], '<Button-3>', lambda event, x=x, y=y, press=3:self.onAnyofTwoPressed(x, y, press))
				self.canvas.tag_bind(self.text[(x,y)], '<ButtonRelease-1>', self.resetPressedState)
				self.canvas.tag_bind(self.text[(x,y)], '<ButtonRelease-2>', self.resetPressedState)
				self.canvas.tag_bind(self.text[(x,y)], '<ButtonRelease-3>', self.resetPressedState)

	def onAnyofTwoPressed(self, x, y, press, event=None):
		if press==1:
			self.left_mouse_pressed = True
			self.updateBoard(x, y)
		if press==3 or press==2:
			self.right_mouse_pressed = True
			self.placeFlag(x, y)
		if (self.left_mouse_pressed and self.right_mouse_pressed):
			self.shotcut(x, y)
		
	def resetPressedState(self, event):
		self.left_mouse_pressed = False
		self.right_mouse_pressed = False

	def updateBoard(self, x, y, event=None):
		if self.game.game == True:
			self.game.pickCell(y, x)
		self.colorBoard()
		self.v.set('Mines: ' + str(self.game.minesleft))

	def placeFlag(self, x, y, event=None):
		if self.game.game == True and self.game.placeFlag(y, x) == True:
			self.v.set('Mines: ' + str(self.game.minesleft))
			self.colorBoard()
				
	def shotcut(self, x, y, event=None):
		if self.game.game == True:
			self.game.shotcut(y, x)
		self.colorBoard()
			
	def colorBoard(self):
		for y in range(self.height):
			for x in range(self.width):
				text = str(self.game.playerboard[y][x])
				textcolor = self.color(text)
				bgcolor = self.bgcolor(text)
				self.canvas.itemconfig(self.text[(x,y)], text=text, fill=textcolor)
				self.canvas.itemconfig(self.cells[(x,y)], fill=bgcolor)

	def color(self, text):
		if text in self.colordict:
			return self.colordict[text]
		return 'black'

	def bgcolor(self, text):
		if text in self.bgcolordict:
			return self.bgcolordict[text]
		return 'white'

	def restart(self):
		self.game.game = True
		self.game.createBoard()
		self.game.newBoard()
		self.colorBoard()
		self.v.set('New game! \nMines: ' + str(self.game.minesleft))

class Minesweeper(object):
	
	def __init__(self, height=16, width=30, mines=99):
		self.height = height
		self.width = width
		self.mines = mines
		self.game= True
		self.createBoard()
		self.newBoard()

	def createBoard(self):
		k = 1
		self.minesleft = self.mines
		self.board = [[0 for i in range(self.width)] for j in range(self.height)]
		while k <= self.mines:
			i = random.randint(0, self.height-1)
			j = random.randint(0, self.width-1)
			if self.board[i][j] == 0:
				self.board[i][j] = 9
				k+=1
		for x in range(self.height):
			for y in range(self.width):
				count = 0
				if self.board[x][y] == 9:
					continue
				xlist, ylist = self.getxyList(x, y)
				for u in xlist:
					for v in ylist:
						if self.board[u][v] == 9:
							count+=1
				self.board[x][y] = count

	def newBoard(self):
		self.playerboard = [[' ' for i in range(self.width)] for j in range(self.height)]

	def shotcut(self, i, j):
		count = 0
		end = False
		if self.playerboard[i][j] != 'F' and self.playerboard[i][j] != ' ':
			xlist, ylist = self.getxyList(i, j)
			for x in xlist:
				for y in ylist:
					if self.playerboard[x][y] == 'F':
						count+=1
			if count >= int(self.playerboard[i][j]):
				for u in xlist:
					for v in ylist:
						if self.playerboard[u][v] == ' ':
							if self.board[u][v] == 9:
								end = True
							elif self.board[u][v] == 0:
								self.pickCell(u, v)
							else:
								self.playerboard[u][v] = self.board[u][v]
		if end == True:
			self.endgame()

	def placeFlag(self, i ,j):
		if self.playerboard[i][j] == ' ':
			self.playerboard[i][j] = 'F'
			self.minesleft-=1
			return True
		elif self.playerboard[i][j] == 'F':
			self.playerboard[i][j] = ' '
			self.minesleft+=1
			return True
		return False

	def pickCell(self, i, j):
		self.cells = []
		visitedCells = []
		if self.playerboard[i][j] != 'F':
			if self.board[i][j] == 9:
				self.endgame()
			elif self.board[i][j] != 0:
				self.playerboard[i][j] = str(self.board[i][j])
			else:
				self.cells.append((i,j))
				while True:
					tempCells = copy.copy(self.cells)
					for x in visitedCells:
						tempCells.remove(x)
					if len(tempCells) == 0:
						break
					temp = tempCells.pop()
					self.getCells(temp[0], temp[1])
					visitedCells.append(temp)

	def getCells(self, i ,j):
		xlist, ylist = self.getxyList(i, j)
		for x in xlist:
			for y in ylist:
				if self.playerboard[x][y] != 'F':
					if self.board[x][y] == 0 and (x,y) not in self.cells:
							self.cells.append((x,y))
					self.playerboard[x][y] = str(self.board[x][y])

	def getxyList(self, x, y):
		xlist = [x]
		ylist = [y]
		if x > 0:
			xlist.append(x-1)
		if y > 0:
			ylist.append(y-1)
		if x < self.height-1:
			xlist.append(x+1)
		if y < self.width-1:
			ylist.append(y+1)
		return xlist, ylist

	def endgame(self):
		for x in range(self.height):
			for y in range(self.width):
				if self.playerboard[x][y] == 'F' and self.board[x][y] != 9:
					self.playerboard[x][y] = 'W'
				if self.board[x][y] == 9 and self.playerboard[x][y] != 'F':
					self.playerboard[x][y] = 'B'
		self.game = False

	def printBoard(self, board):
		for i in range(self.height):
			print(board[i])

app = Gui()
app.mainloop()
