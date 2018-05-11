from CC3501Utils import *
import random
from coordinate import Coordinate

class DestructiveBlock(Figura):
	def __init__(self, pjs, pos=Vector(0, 0), rgb=(1.0, 1.0, 1.0)):
		self.pjs = pjs
		self.fire = None
		
		self.choose_pos()
		self.coord = [Coordinate(self.pos, self.pos + Vector(50, 50))]

		super().__init__(self.pos, rgb)

	def figura(self):
		glBegin(GL_QUADS)
		glColor3f(0/255, 255/255, 255/255)
		cord = [(0, 0), (0, 50), (50, 50), (50, 0)]
		for p in cord:
			glVertex2f(p[0], p[1])
		glEnd()

	def choose_pos(self):
		s = self

		grid = s.pjs[0]
		
		x = 0
		y = 0

		for i in range(len(grid.coord)):
			x = max(x, grid.coord[i].inf.x)
			y = max(y, grid.coord[i].inf.y)

		i = 0
		j = 0
		availablecoords = []
		while i <= x:
			while j <= y:
				acoord = Coordinate(Vector(i, j), Vector(i + 50, j + 50))
				
				isavailable = True
				for pj in s.pjs:
					if not(isavailable):
						break
					for coord in pj.coord:
						if acoord.overlap(coord):
							isavailable = False
							break

				if isavailable:
					availablecoords.append(acoord)
				j += 50
			j = 0
			i += 50

		ran = random.randint(0, len(availablecoords) - 1)
		s.pos = availablecoords[ran].inf

	def explode(self, fire):
		self.fire = fire

