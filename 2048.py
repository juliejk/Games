import random
import copy
import tkinter as tk
from tkinter import *

class Gui(tk.Tk):

	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.cells = {}
		self.text = {}
		self.game = Game2048()
		self.cell_width = 40
		self.cell_height = 40
		self.bgcolor = {2: '#F2F2F2', 4: '#F5ECCE', 8: '#F5D0A9', 16: '#FA8258', 32: '#FA5858', 64: '#FE2E2E', 128: '#F2F5A9', 256: '#F3F781', 512: '#F4FA58', 1024: '#F7FE2E', 2048: '#FFFF00'}
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
		self.bind_all('<Key>', self.keyPressed)
		self.colorBoard()
		self.pointsText = tk.Label(self, textvariable=self.v)
		self.pointsText.pack()
		self.v.set('New game!')

	def drawBoard(self):
		offsetx = self.cell_width
		offsety = self.cell_height
		for y in range(self.height):
			for x in range(self.width):
				x1 = x * self.cell_width + offsetx
				y1 = y * self.cell_height + offsety
				x2 = x1 + self.cell_width
				y2 = y1 + self.cell_height
				self.cells[(x,y)] = self.canvas.create_rectangle(x1,y1,x2,y2, fill='#E6E6E6', tags='rect')
				self.text[(x,y)] = self.canvas.create_text(x1+(self.cell_width/2), y1+(self.cell_height/2), anchor=CENTER, text=" ")

	def keyPressed(self,event):
		if event.keysym == 'Right':
			self.updateBoard('R')
		elif event.keysym == 'Left':
			self.updateBoard('L')
		elif event.keysym == 'Up':
			self.updateBoard('U')
		elif event.keysym == 'Down':
			self.updateBoard('D')

	def updateBoard(self, arrow):
		if self.game.end == False:
			self.game.updateBoard(arrow)
			self.colorBoard()
		elif self.game.end == True:
			self.v.set('GAME OVER!')

	def colorBoard(self):
		for y in range(self.height):
			for x in range(self.width):
				text = self.game.board[y][x]
				if text == 0:
					text = ' '
				bgcolor = self.bgcolorFun(text)
				self.canvas.itemconfig(self.text[(x,y)], text=text, fill='black')
				self.canvas.itemconfig(self.cells[(x,y)], fill=bgcolor)

	def bgcolorFun(self, text):
		if text in self.bgcolor:
			return self.bgcolor[text]
		else:
			return '#E6E6E6'

	def restart(self):
		self.game.createBoard()
		self.colorBoard()
		self.v.set('New game!')

class Game2048(object):

	def __init__(self, height=4, width=4):
		self.height = height
		self.width = width
		self.createBoard()

	def createBoard(self):
		self.end = False
		self.board = [[0 for i in range(self.width)] for j in range(self.height)]
		for i in range(2):
			self.genNewCell()

	def genNewCell(self):
		while True:
			x = random.randint(0, self.height-1)
			y = random.randint(0, self.width-1)
			if self.board[x][y] == 0:
				n = random.random()
				if n < 0.9:
					self.board[x][y] = 2
				else:
					self.board[x][y] = 4
				break

	def updateBoard(self, arrow):
		self.four = 0
		tempboard = copy.copy(self.board)
		if arrow == 'U' or arrow == 'D':
			self.board = [list(i) for i in zip(*self.board)]
		for y in range(self.height):
			temprow = copy.copy(self.board[y])
			if arrow == 'R':
				row = self.moveRight(temprow)[::-1]
			elif arrow == 'L':
				row = self.moveRight(temprow[::-1])
			elif arrow == 'U':
				row = self.moveRight(temprow[::-1])
			elif arrow == 'D':
				row = self.moveRight(temprow)[::-1]
			self.board[y] = row
		if arrow == 'U' or arrow == 'D':
			self.board = [list(i) for i in zip(*self.board)]
		if self.board != tempboard:
			self.genNewCell()
		if self.four == 4:
			self.end = self.checkIfEnd()

	def moveRight(self, temprow):
		row = list(filter((0).__ne__, temprow))
		i = len(row)-1
		temp = []
		while i >= 0:
			if len(row) == 0:
				break
			if i == 0:
				temp.append(row[i])
			elif row[i] == row[i-1]:
				temp.append(row[i]*2)
				i-=1
			else:
				temp.append(row[i])
			i-=1
		if len(temp) == len(temprow):
			self.four += 1
		temp.extend([0 for b in range(self.width-len(temp))])
		return temp

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

	def printBoard(self, board):
		for i in range(self.height):
			print(board[i])

app = Gui()
app.mainloop()