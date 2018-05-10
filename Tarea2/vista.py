from OpenGL.GL import *
from CC3501Utils import *
from bomb import Bomb
from fire import Fire


class Vista:
	def dibujar(self, pjs):
		grid = pjs[0]
        # limpia la pantalla
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		
		for p in pjs:
			if type(p) == Fire:
				if p.lifetime() > 2:
					pjs.remove(p)
				else:
					p.dibujar()

		for p in pjs:
			if type(p) == Bomb:
				if p.lifetime() > 3:
					p.explode()
				else:
					p.dibujar()

		for p in pjs:
			if type(p) != Bomb and type(p) != Fire:
				p.dibujar()
