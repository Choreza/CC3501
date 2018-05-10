from CC3501Utils import *
from coordinate import Coordinate
from datetime import datetime
from fire import Fire
import numpy as np

class Bomb(Figura):
	def __init__(self, pjs, radius, pos=Vector(0, 0), rgb=(1.0, 1.0, 1.0)):
		super().__init__(pos, rgb)
		self.pjs = pjs
		
		self.coord = []
		self.coord.append(Coordinate(pos, pos + Vector(50, 50)))

		self.start = datetime.now()
		self.radius = radius

	def lifetime(self):
		now = datetime.now()
		difference = (now - self.start).total_seconds()
		return difference

	def explode(self):
		s = self
		s.pjs.remove(s)
		s.pjs[1].bombs += 1
		s.pjs.append(Fire(s.pjs, s.radius,  s.pos))		

	def figura(self):
		glBegin(GL_QUADS)
		glColor3f(0/255, 0/255, 255/255)
		cord = [(0, 0), (0, 50), (50, 50), (50, 0)]
		for p  in cord:
			glVertex2f(p[0], p[1])
		glEnd()