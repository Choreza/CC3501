from OpenGL.GL import *
from CC3501Utils import *
from Bomb import *


class Vista:
	def dibujar(self, pjs):
		grid = pjs[0]
        # limpia la pantalla
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		for p in pjs:
			if type(p) == Bomb:
				if p.life_time() >= 4:
					grid.set_pos(p.pos, 0)
					pjs.remove(p)
				else:
					p.dibujar()
		for p in pjs:
			if type(p) != Bomb:
				p.dibujar()