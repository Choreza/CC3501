

class Coordinate:
	def __init__(self, inf, sup):
		self.inf = inf
		self.sup = sup

	def overlap(self, coord):
		s = self
		c = coord

		if s.sup.x <= c.inf.x:
			return False
		if s.inf.x >= c.sup.x:
			return False
		if s.sup.y <= c.inf.y:
			return False
		if s.inf.y >= c.sup.y:
			return False
		return True

	def __str__(self):
		return "(" + str(self.inf) + ", " + str(self.sup) +")"

	def move(self, pos):
		self.inf += pos
		self.sup += pos

	def __add__(self, vec):
		return Coordinate(self.inf + vec, self.sup + vec)