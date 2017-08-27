import pyglet
from square import *
from pyglet.window import key

window = pyglet.window.Window()

keys = key.KeyStateHandler()
window.push_handlers(keys)


class Board:
	
	class Cell:
		def __init__(self, maxCellHealth, origin, size, colorId, color):
			self.colorId = colorId
			self.color = color
			self.health = maxCellHealth
			
			self.__body = Square(origin, size, color)
			
		def draw(self):
			self.__body.draw()
			
		def changeColor(self, newColorId, newColor, newHealth):
			self.colorId = newColorId
			self.color = newColor
			self.health = newHealth
			
			self.__body.setColor(newColor)
			
		def receiveDamage(self, colorIdofPredator, colorOfPredator, maxHealth):
			changedColor = False
			self.health -= 1
			if self.health < 0:
				self.changeColor(colorIdofPredator, colorOfPredator, maxHealth)
				changedColor = True
			return changedColor
	
	def __init__(self, cellSize = 10, initNumCellColors = 3, maxCellHealth = 4):
		
		self.__maxCellHealth = maxCellHealth
		
		self.__cellSize = cellSize
		self.__numCellColors = initNumCellColors
		self.__initNumCellColors = initNumCellColors
		
		self.__generation = 0
		
		self.__numRows = window.height // cellSize
		self.__numCols = window.width // cellSize
		
		self.__colorIdToColor = {}
		
		for i in range(initNumCellColors):
			self.__colorIdToColor[i] = Color(randomColor = True)
			
		self.__cells = []
		
		self.__initBoard()	
		self.draw()
		
		self.__neighborCoordinates = [(-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2),
																	(-2, -1),	(-1, -1), (0, -1), (1, -1), (2, -1),
																	(-2,  0), (-1,  0),      	 	 (1,  0), (2,  0),
																	(-2,  1), (-1,  1), (0,  1), (1,  1), (2,  1),
																	(-2,  2), (-1,  2), (0,  2), (1,  2), (2,  2)]
																	

		
	def __initBoard(self):
		x = 0
		y = 0			
		origin = Point(x, y)
		for i in range(self.__numRows):
			newRow = []
			for j in range(self.__numCols):
				randomColorId = random.randint(0, self.__initNumCellColors - 1)
				newCell = self.Cell(self.__maxCellHealth, origin, self.__cellSize, 
					colorId = randomColorId, color = self.__colorIdToColor[randomColorId])
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
				
	def update(self):
		self.__generation += 1
		for (i, row) in enumerate(self.__cells):
			for (j, cell) in enumerate(row):
				self.__defend(i, j)
				
	def incrNumTypes(self):
		newColor = Color(randomColor = True)
		newColorId = self.__numCellColors
		newHealth = self.__maxCellHealth
		self.__colorIdToColor[newColorId] = newColor
		self.__numCellColors += 1
		for row in self.__cells:
			for cell in row:
				if random.randint(0, 100) / 100 > (1 - (1 / self.__numCellColors)):
					cell.changeColor(newColorId, newColor, newHealth)
		self.update()
		
	def decrNumTypes(self):
		if self.__numCellColors == 2:
			return
		idToPop = len(self.__colorIdToColor) - 1
		self.__colorIdToColor.pop(idToPop)
		self.__numCellColors = len(self.__colorIdToColor)
		for row in self.__cells:
			for cell in row:
				if cell.colorId == idToPop:
					otherColorId = random.randint(0, self.__numCellColors - 1)
					otherColor = self.__colorIdToColor[otherColorId]
					cell.changeColor(otherColorId, otherColor, self.__maxCellHealth)
		self.update()
				
	def __coordinatesAreOutOfBounds(self, x, y):
		if x < 0 or x >= self.__numRows:
			return True
		elif y < 0 or y >= self.__numCols:
			return True
		else:
			return False
				
	def __defend(self, i, j):
		# Idea: change rules of predation, e.g., a cell can be eaten not just by the
		# cells of color ids one above itself, but also by cells of colors ids which
		# it divides into, or whatever.
		colorIdOfPredator = (self.__cells[i][j].colorId + 1) % self.__numCellColors
		
		for neighborCoordinates in self.__neighborCoordinates:
			x = i + neighborCoordinates[0]
			y = j + neighborCoordinates[1]
			if not self.__coordinatesAreOutOfBounds(x, y):
				neighbor = self.__cells[x][y]
				if neighbor.colorId == colorIdOfPredator:
					colorOfPredator = self.__colorIdToColor[colorIdOfPredator]
					changedColor = self.__cells[i][j].receiveDamage(colorIdOfPredator, 
						colorOfPredator, self.__maxCellHealth)
					if changedColor:
						return
			
board = Board(cellSize = 12, initNumCellColors = 3, maxCellHealth = 15)


def update(dt):
	window.clear()
	if keys[key.UP]:
		board.incrNumTypes()
	elif keys[key.DOWN]:
		board.decrNumTypes()
	board.draw()
	board.update()
	
def main():
	pyglet.clock.schedule_interval(update, 1/120)
	pyglet.app.run()

if __name__ == "__main__":
	main()
