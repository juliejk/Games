import random
import copy
import tkinter as tk
from tkinter import *

class Gui(tk.Tk):

	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.cells = {}
		self.text = {}
		self.game = Wiper()
		self.cell_width = 15
		self.cell_height = 15
		self.colordict = {0: 'white', 1: '#0000FF', 2: '#F7FE2E', 3: '#2EFE2E', 4: '#FF0000', 5: '#FE2EC8'}
		self.start()

	def start(self):
		self.v = StringVar()
		self.width = self.game.width
		self.height = self.game.height
		self.screen_width = (self.width + 2)*self.cell_width
		self.screen_height = (self.height + 2)*self.cell_height
		self.startButton = tk.Button(self, text='Start a new game', command=lambda: self.restart())
		self.startButton.pack()
		self.canvas = tk.Canvas(self, width=self.screen_width, height=self.screen_height, borderwidth=0, highlightthickness=0)
		self.canvas.pack(side="top", fill="both", expand="true")
		self.drawBoard()
		self.colorBoard()
		self.pointsText = tk.Label(self, textvariable=self.v)
		self.pointsText.pack()
		self.v.set('New game!')

	def drawBoard(self):
		offsetx = self.cell_width
		offsety = self.cell_height
		for x in range(self.width):
			for y in range(self.height):
				x1 = x * self.cell_width + offsetx
				y1 = y * self.cell_height + offsety
				x2 = x1 + self.cell_width
				y2 = y1 + self.cell_height
				self.cells[(x,y)] = self.canvas.create_rectangle(x1,y1,x2,y2, fill='white', tags='rect')
				self.canvas.tag_bind(self.cells[(x,y)], '<Button-1>', lambda event, x=x, y=y:self.updateBoard(x, y))

	def updateBoard(self, x, y, event=None):
		self.game.updateBoard(x, y)
		self.colorBoard()
		if self.game.end == True:
			self.v.set('Game Over! \nPoeng: ' + str(self.game.points))
		else:
			self.v.set('Poeng: ' + str(self.game.points))

	def colorBoard(self):
		for y in range(self.height):
			for x in range(self.width):
				color = self.game.board[y][x]
				bgcolor = self.colordict[color]
				self.canvas.itemconfig(self.cells[(x,y)], fill=bgcolor)

	def restart(self):
		self.game.createBoard()
		self.colorBoard()
		self.v.set('New game!')

class Wiper(object):

	def __init__(self, height=16, width=16, colors=5):
		self.height = height
		self.width = width
		self.colors = colors
		self.createBoard()

	def createBoard(self):
		self.points = 0
		self.end = False
		self.board = [[0 for i in range(self.width)] for j in range(self.height)]
		for y in range(self.height):
			for x in range(self.width):
				i = random.randint(1, self.colors)
				self.board[y][x] = i

	def updateBoard(self, x, y):
		self.cells = [(y, x)]
		visitedCells = []
		self.oneCheck = True
		if self.board[y][x] != 0:
			while True:
				tempCells = copy.copy(self.cells)
				for x in visitedCells:
					if x in tempCells:
						tempCells.remove(x)
				if len(tempCells) == 0:
					break
				temp = tempCells.pop()
				self.getCells(temp[0], temp[1])
				visitedCells.append(temp)
			self.dropDown()
			self.updatePoints(len(self.cells))
		self.end = self.checkIfEnd()
		if self.end == True:
			self.endGame()

	def getCells(self, y ,x):
		temp = self.board[y][x]
		if y > 0 and self.board[y-1][x] == temp:
			self.checkCell(x, y-1)
		if y < self.height-1 and self.board[y+1][x] == temp:
			self.checkCell(x, y+1)
		if x > 0 and self.board[y][x-1] == temp:
			self.checkCell(x-1, y)
		if x < self.width-1 and self.board[y][x+1] == temp:
			self.checkCell(x+1, y)
		if self.oneCheck == False:
			self.board[y][x] = 0

	def checkCell(self, x, y):
		self.oneCheck = False
		if (y, x) not in self.cells:
			self.cells.append((y, x))

	def dropDown(self):
		tempBoard = [list(i) for i in zip(*self.board)]
		i = 0
		for x in range(self.width):
			col = list(filter((0).__ne__, tempBoard[x]))[::-1]
			col.extend([0 for b in range(self.height-len(col))])
			tempBoard[x] = col[::-1]
		temp = []
		for i in range(self.width):
			if tempBoard[i][-1] != 0:
				temp.append(tempBoard[i])
		temp.extend([[0 for b in range(self.height)] for a in range(self.width-len(temp))])
		self.board = [list(i) for i in zip(*temp)]

	def updatePoints(self, lenght):
		if self.oneCheck == False:
			self.points += lenght*10

	def getxyList(self, y, x):
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

	def checkIfEnd(self):
		for y in range(self.height):
			for x in range(self.width):
				if self.board[y][x] == 0:
					continue
				if y > 0 and self.board[y-1][x] == self.board[y][x]:
					return False
				if y < self.height-1 and self.board[y+1][x] == self.board[y][x]:
					return False
				if x > 0 and self.board[y][x-1] == self.board[y][x]:
					return False
				if x < self.width-1 and self.board[y][x+1] == self.board[y][x]:
					return False
		return True

	def endGame(self):
		one = 0; two = 0; three = 0; four = 0; five = 0
		won = 0
		for y in range(self.height):
			for x in range(self.width):
				if self.board[y][x] == 1:
					one+=1
				if self.board[y][x] == 2:
					two+=1
				if self.board[y][x] == 3:
					three+=1
				if self.board[y][x] == 4:
					four+=1
				if self.board[y][x] == 5:
					five+=1
		if one == 0:
			self.points += 1000
			won += 1
		if two == 0:
			self.points += 1000
			won += 1
		if three == 0:
			self.points += 1000
			won += 1
		if four == 0:
			self.points += 1000
			won += 1
		if five == 0:
			self.points += 1000
			won += 1
		if won == 5:
			self.points += 2000

	def printBoard(self, board):
		for i in range(self.height):
			print(board[i])

app = Gui()
app.mainloop()