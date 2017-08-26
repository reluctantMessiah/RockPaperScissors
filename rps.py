import pyglet
from square import *

window = pyglet.window.Window()

class Board:
	
	class Cell:
		def __init__(self, maxCellHealth, origin, size, color = Color(randomColor = True)):
			self.colorId = -1
			self.health = maxCellHealth
			
			self.__body = Square(origin, size, color)
			
		def draw(self):
			self.__body.draw()
	
	def __init__(self, cellSize = 5, initNumCellColors = 3):
		
		self.__maxCellHealth = 10
		
		self.__cellSize = cellSize
		self.__initNumCellColors = initNumCellColors
		
		self.generation = 0
		
		self.__numRows = window.height // cellSize
		self.__numCols = window.width // cellSize
		
		self.__colorIdToColor = {-1 : Color(255, 255, 255)}
		
		for i in range(initNumCellColors):
			self.__colorIdToColor[i] = Color(randomColor = True)
			
		self.__cells = []
		
		self.__initBoard()
		self.draw()
		
	def __initBoard(self):
		x = 0
		y = 0			
		origin = Point(x, y)
		for i in range(self.__numRows):
			newRow = []
			for j in range(self.__numCols):
				newCell = self.Cell(self.__maxCellHealth, origin, self.__cellSize)
				newRow.append(newCell)
				x += self.__cellSize
				origin = Point(x, y)
			self.__cells.append(newRow)
			x = 0
			y += self.__cellSize
			origin = Point(x, y)
			
	def draw(self):
		for row in self.__cells:
			for cell in row:
				cell.draw()
			
#origin = Point(100, 100)
#square = Square(origin, 100)

board = Board()

def update(dt):
	window.clear()
	board.draw()
#	square.draw()
	
def main():
	pyglet.clock.schedule_interval(update, 1/120)
	pyglet.app.run()

if __name__ == "__main__":
	main()
