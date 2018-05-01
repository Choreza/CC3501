from CC3501Utils import *

class Bomberman(Figura):
	def __init__(self, grid, pos=Vector(0, 0), rgb=(1.0, 1.0, 1.0)):
		self._grid = grid
		super().__init__(pos, rgb)

	def figura(self):
		glBegin(GL_QUADS)
		glColor3f(255/255, 0/255, 0/255)
		cord = [(0, 0), (0, 50), (50, 50), (50, 0)]
		for p in cord:
			glVertex2f(p[0], p[1])
		glEnd()

	def move(self, hor, ver):
		matrix = self._grid.get_matrix()
		
		x = int((self.pos.x + hor)/50)
		y = int((self.pos.y + ver)/50)

		if 0 < x < len(matrix) and 0 < y < len(matrix[0]):
			if matrix[x][y] != 1:
				self.pos += Vector(hor, ver)

		

