from CC3501Utils import *
from destructiveblock import DestructiveBlock
from coordinate import Coordinate
import random

class PowerUp(Figura):
	def __init__(self, pjs, pos=Vector(0, 0), rgb=(1.0, 1.0, 1.0)):
		self.pjs = pjs
		self.choose_pos()

		self.coord = []
		self.coord.append(Coordinate(pos, pos + Vector(50, 50)))

		self.posibilities = ['bomb', 'radius', 'speed']
		self.power = random.randint(0, len(self.posibilities)-1)
		
		super().__init__(self.pos, rgb)

	def choose_pos(self):
		s = self

		availablepos = []
		for pj in s.pjs:
			if type(pj) == DestructiveBlock:
				availablepos.append(pj.pos)

		pos = random.randint(0, len(availablepos)-1)
		s.pos = availablepos[pos]

	def figura(self):
		print(self.pos)
		glBegin(GL_QUADS)
		glColor3f(0/255, 128.0/255, 0/255)
		cord = [(0, 0), (0, 50), (50, 50), (50, 0)]
		for p  in cord:
			glVertex2f(p[0], p[1])
		glEnd()