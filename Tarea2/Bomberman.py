from CC3501Utils import *
from Bomb import *

class Bomberman(Figura):
	def __init__(self, grid, clock, pos=Vector(0, 0), rgb=(1.0, 1.0, 1.0)):
		self._grid = grid
		self._clock = clock
		super().__init__(pos, rgb)

	def figura(self):
		glBegin(GL_QUADS)
		glColor3f(255/255, 0/255, 0/255)
		cord = [(0, 0), (0, 50), (50, 50), (50, 0)]
		for p in cord:
			glVertex2f(p[0], p[1])
		glEnd()

	def move(self, direction):
		matrix = self._grid.get_matrix()
		
		new_pos = self.pos + direction
		x = int(new_pos.x/50)
		y = int(new_pos.y/50)

		if 0 < x < len(matrix) and 0 < y < len(matrix[0]):
			if matrix[x][y] != 1:
				self.pos += direction

	def put_bomb(self, pjs):
		for p in pjs:
			if type(p) == Bomb and p.pos == self.pos:
				return
		
		self._grid.set_pos(self.pos, 1)

		bomb = Bomb(self.pos)
		pjs.append(bomb)
	
