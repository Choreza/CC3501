from CC3501Utils import *
from bomb import Bomb
from coordinate import Coordinate
from fire import Fire
from powerup import PowerUp
from destructiveblock import DestructiveBlock

class Bomberman(Figura):
	def __init__(self, pjs, pos=Vector(0, 0), rgb=(1.0, 1.0, 1.0)):
		super().__init__(pos, rgb)
		self.pjs = pjs

		self.bombs = 5
		self.speed = 12.5
		self.bombradius = 2
		self.killer = None

		self.coord = []
		self.coord.append(Coordinate(pos, pos + Vector(50, 50)))

	def figura(self):
		glBegin(GL_QUADS)
		glColor3f(255/255, 0/255, 0/255)
		cord = [(0, 0), (0, 50), (50, 50), (50, 0)]
		for p in cord:
			glVertex2f(p[0], p[1])
		glEnd()


	def check_pos(self):
		s = self
		for pj in s.pjs:
			if type(pj) == Fire:
				for coord in pj.coord:
					if coord.overlap(s.coord[0]):
						s.die(pj)

	def die(self, pj):
		self.killer = pj

	def move(self, direction):
		s = self
		direction *= s.speed

		for pj in s.pjs:
			
			if type(pj) == Bomb:
				if pj == s.pjs[len(s.pjs)-1] and s.coord[0].overlap(pj.coord[0]):
					break
			
			if type(pj) == PowerUp:
				if pj.coord[0].overlap(s.coord[0]):
					s.eat(pj)

			if type(pj) != Bomberman and type(pj) != Fire:
				for c in pj.coord:
					if (s.coord[0] + direction).overlap(c):	
						return
			
		self.pos += direction
		self.coord[0].move(direction)

	def put_bomb(self):
		s = self

		x = s.pos.x - s.pos.x % 50
		y = s.pos.y - s.pos.y % 50
		
		for pj in s.pjs:
			if type(pj) == Bomb:
				if pj.coord[0].overlap(s.coord[0]):
					return
		
		if s.bombs > 0:
			s.bombs -= 1
		else:
			return
		
		s.pjs.append(Bomb(s.pjs, s.bombradius, Vector(x, y)))

	def eat(self, powerup):
		s = self
		p = powerup

		s.pjs.remove(p)

		if p.posibilities[p.power] == 'bomb':
			s.bombs += 1

		if p.posibilities[p.power] == 'speed':
			s.speed *= 2

		if p.posibilities[p.power] == 'radius':
			s.bombradius += 1

	def clear_radius(self, radius):
		s = self

		i = -radius*50
		j = -radius*50

		while i < radius*50:
			while j < radius*50:
				acoord = Coordinate(s.pos+Vector(i, j), s.pos+Vector(i+50, j+50))
				for pj in s.pjs:
					if type(pj) != DestructiveBlock:
						continue
					for coord in pj.coord:
						if acoord.overlap(coord):
							print(coord)
							s.pjs.remove(pj)
							break
				j += 50
			j = -radius*50
			i += 50

