from CC3501Utils import *
import random

class PowerUp(Figura):
	def __init__(self, pjs, pos=Vector(0, 0), rgb=(1.0, 1.0, 1.0)):
		super().__init__(pos, rgb)
		self.pjs = pjs
		self.pos = pos

		self.coord = []
		self.coord.append(Coordinate(pos, pos + Vector(50, 50)))

		self.posibilities = ['bomb', 'radius', 'speed']
		self.power = random.randint(0, len(self.posibilities)-1)

	def figura(self):
		glBegin(GL_QUADS)
		glColor3f(0/255, 0/255, 255/255)
		cord = [(0, 0), (0, 50), (50, 50), (50, 0)]
		for p  in cord:
			glVertex2f(p[0], p[1])
		glEnd()