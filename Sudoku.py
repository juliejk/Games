import random
import copy
import tkinter as tk
from tkinter import *

class Gui(tk.Tk):

	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.cells = {}
		self.text = {}
		self.game = Sudoku()
		self.cell_width = 15
		self.cell_height = 15
		self.start()

	def start(self):
		self.width = self.game.width
		self.height = self.game.height
		self.screen_width = (self.width + 2)*self.cell_width
		self.screen_height = (self.height + 2)*self.cell_height
		self.startButton = tk.Button(self, text='Start a new game', command=lambda: self.restart())
		self.startButton.pack()
		self.canvas = tk.Canvas(self, width=self.screen_width, height=self.screen_height + 60, borderwidth=0, highlightthickness=0)
		self.canvas.pack(side="top", fill="both", expand="true")
		self.drawBoard()

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
				self.text[(x,y)] = self.canvas.create_text(x1+7.5, y1+7.5, anchor=CENTER, text=" ")
				self.canvas.tag_bind(self.text[(x,y)], '<Button-1>', lambda event, x=x, y=y, press=1:self.onAnyofTwoPressed(x, y, press))

class Sudoku(object):

	def __init__(self, height=9, width=9):
		self.height = height
		self.width = width
		correctBoard = False
		while correctBoard == False:
			self.createBoard()
			correctBoard = self.checkBoard()
		
	def createBoard(self):
		self.board = [[0 for i in range(self.width)] for j in range(self.height)]
		for y in range(self.width):
			for x in range(self.height):
				if self.board[y][x] == 0:
					row = self.checkRow(y)
					col = self.checkCol(x)
					box = self.checkBox(x, y)
					i=1
					while i < 10:
						#i = random.randint(1,9)
						if i not in row and i not in col and i not in box:
							self.board[y][x] = i
							break
						i+=1
		self.printBoard()

	def checkBoard(self):
		for y in range(self.width):
			for x in range(self.height):
				if self.board[y][x] == 0:
					return False
		return True

	def checkRow(self, y):
		row = []
		for x in range(self.width):
			if self.board[y][x] != 0:
				row.append(self.board[y][x])
		return row

	def checkCol(self, x):
		col = []
		for y in range(self.height):
			if self.board[y][x] != 0:
				col.append(self.board[y][x])
		return col

	def checkBox(self, x, y):
		box = []
		xlist, ylist = self.getxyList(x, y)
		for y in ylist:
			for x in xlist:
				if self.board[y][x] != 0:
					box.append(self.board[y][x])
		return box

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

	def printBoard(self, board):
		for i in range(self.height):
			print(board[i])

Sudoku()