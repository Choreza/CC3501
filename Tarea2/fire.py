from CC3501Utils import *
from coordinate import Coordinate
from datetime import datetime
from destructiveblock import DestructiveBlock

class Fire(Figura):
	def __init__(self, pjs, radius, pos=Vector(0, 0), rgb=(1.0, 1.0, 1.0)):
		self.pjs = pjs
		self.pos = pos
		self.radius = radius

		self.coord = []
		self.init_coordinates()
		
		self.start = datetime.now()

		super().__init__(pos, rgb)
		

	def init_coordinates(self):
		s = self

		x = s.pos.x
		y = s.pos.y

		s.coord.append(Coordinate(s.pos, s.pos + Vector(50, 50)))

		directions = []
		directions.append([])
		for i in range(1, s.radius):
			directions[0].append(Vector(x - i*50, y))

		directions.append([])
		for i in range(1, s.radius):
			directions[1].append(Vector(x + i*50, y))

		directions.append([])
		for i in range(1, s.radius):
			directions[2].append(Vector(x, y - i*50))

		directions.append([])
		for i in range(1, s.radius):
			directions[3].append(Vector(x, y + i*50))

		for direction in directions:
			overlap = False

			for p in direction:
				coord = Coordinate(p, p + Vector(50, 50))
				
				for pj in s.pjs:
					if pj == s.pjs[0] or type(pj) == DestructiveBlock:
						for c in pj.coord:
							if c.overlap(coord):
								overlap = True

								if type(pj) == DestructiveBlock:
									pj.explode(s)

				if not(overlap):
					s.coord.append(coord)
				else:
					break
				
	def figura(self):
		s = self
		
		glBegin(GL_QUADS)
		glColor3f(255.0/255, 165.0/255, 0.0/255)
		for p in s.coord:
			aux = p.inf - s.pos
			x = aux.x
			y = aux.y
			glVertex2f(x, y)
			glVertex2f(x + 50, y)
			glVertex2f(x + 50, y + 50)
			glVertex2f(x, y + 50)
		glEnd()

	def lifetime(self):
		now = datetime.now()
		difference = (now - self.start).total_seconds()
		return difference

