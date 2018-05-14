from OpenGL.GL import *
from CC3501Utils import *
from bomb import Bomb
from fire import Fire
from bomberman import Bomberman
from powerup import PowerUp
from destructiveblock import DestructiveBlock

class Vista:
	def dibujar(self, pjs):
		grid = pjs[0]
        # limpia la pantalla
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		if type(pjs[1]) == Bomberman:
			pjs[1].check_pos()

		for p in pjs:
			if type(p) == Fire:
				if p.lifetime() > 2:
					pjs.remove(p)
				else:
					p.dibujar()

		for p in pjs:
			if type(p) == PowerUp:
				p.dibujar()

		for p in pjs:
			if type(p) == DestructiveBlock:
				if p.fire != None and not(p.fire in pjs):
					pjs.remove(p)

		for p in pjs:
			if type(p) == Bomb:
				if p.lifetime() > 3:
					p.explode()
				else:
					p.dibujar()

		for p in pjs:
			if type(p) != Bomb and type(p) != Fire and type(p) != PowerUp:
				p.dibujar()

			if type(p) == Bomberman:
				if p.killer != None:
					pjs.remove(p)
				else:
					p.dibujar()
