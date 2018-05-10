from CC3501Utils import *
from coordinate import Coordinate

class Grid(Figura):
	def __init__(self, col, row, pos=Vector(0, 0), rgb=(1.0, 1.0, 1.0)):
		self.coord = []
		self.__initmatrix(col, row)
		super().__init__(pos, rgb)

	def __initmatrix(self, col, row):
		self.matrix = [[1 for j in range(col)] for i in range(row)]	
		for i in range(1, row-1):
			for j in range(1, col-1):
				if (i % 2 == 1 and j % 2 == 1) or (i % 2 != j % 2):
					self.matrix[i][j] = 0

	def set_pos(self, vec, val):
		x = int(vec.x/50)
		y = int(vec.y/50)
		self.matrix[x][y] = val

	def figura(self):
		mat = self.matrix
		glBegin(GL_QUADS)
		
		glColor3f(80/255, 80/255, 80/255)

		for i in range(len(mat)):
			for j in range(len(mat[0])):
				if mat[i][j]:
					glVertex2f(50 * i, 50 * j)
					glVertex2f(50 * i + 50, 50 * j)
					glVertex2f(50 * i + 50, 50 * j + 50)
					glVertex2f(50 * i, 50 * j + 50)

					self.coord.append(Coordinate(Vector(50 * i, 50 * j), Vector(50 * i + 50, 50 * j + 50)))
		glEnd()
