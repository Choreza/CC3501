from CC3501Utils import *

class Grid(Figura):
	def __init__(self, col, row, pos=Vector(0, 0), rgb=(1.0, 1.0, 1.0)):
		self.__init_matrix(col, row)
		super().__init__(pos, rgb)

	def __init_matrix(self, col, row):
		self._matrix = [[1 for j in range(col)] for i in range(row)]	
		for i in range(1, row-1):
			for j in range(1, col-1):
				if (i % 2 == 1 and j % 2 == 1) or (i % 2 != j % 2):
					self._matrix[i][j] = 0

	def get_matrix(self):
		return self._matrix

	def figura(self):
		mat = self._matrix
		glBegin(GL_QUADS)
		
		glColor3f(80/255, 80/255, 80/255)

		for i in range(len(mat)):
			for j in range(len(mat[0])):
				if mat[i][j]:
					glVertex2f(50*i, 50*j)
					glVertex2f(50*i + 50, 50*j)
					glVertex2f(50*i + 50, 50*j + 50)
					glVertex2f(50*i, 50*j + 50)
		glEnd()