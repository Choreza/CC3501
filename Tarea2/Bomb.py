from CC3501Utils import *
import datetime

class Bomb(Figura):
	def __init__(self, pos=Vector(0, 0), rgb=(1.0, 1.0, 1.0)):
		super().__init__(pos, rgb)
		self._start = datetime.datetime.now()

	def life_time(self):
		now = datetime.datetime.now()
		delta = now - self._start
		return delta.total_seconds()

	def figura(self):
		glBegin(GL_QUADS)
		glColor3f(0/255, 0/255, 255/255)
		cord = [(0, 0), (0, 50), (50, 50), (50, 0)]
		for p  in cord:
			glVertex2f(p[0], p[1])
		glEnd()