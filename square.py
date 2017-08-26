import pyglet
#from pyglet.window import mouse
from pyglet import clock
import random

class Color:
	def __init__(self, r = 255, g = 255, b = 255, randomColor = False):
		
		if randomColor:
			self.randomizeColor()
		else:
			self.r = r
			self.g = g
			self.b = b
		
	def randomizeColor(self):
		self.r = random.randint(0, 255)
		self.g = random.randint(0, 255)
		self.b = random.randint(0, 255)

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Square:
	# Origin is the Point of the top left vertex
	def __init__(self, origin, size = 10, color = Color(randomColor = True)):
		self.__origin = origin
		self.__size = size
		self.__color = color

		self.__updateBodyAttributes()
		
	def setColor(self, color):
		self.__color = color
		self.__updateBodyAttributes()
		
	def draw(self):
		self.body.draw(pyglet.gl.GL_QUADS)
		
	def __updateBodyAttributes(self):
		origin = self.__origin
		size = self.__size
		color = self.__color
		topLeft = origin
		topRight = Point(origin.x + size, origin.y)
		bottomLeft = Point(origin.x, origin.y + size)
		bottomRight = Point(origin.x + size, origin.y + size)
		self.body = pyglet.graphics.vertex_list(4, 
			('v2i', (topLeft.x, topLeft.y, 
							 bottomLeft.x, bottomLeft.y,
							 bottomRight.x, bottomRight.y,
							 topRight.x, topRight.y)), 
			('c3B', (color.r, color.g, color.b, 
						   color.r, color.g, color.b,
							 color.r, color.g, color.b,  
							 color.r, color.g, color.b)))
