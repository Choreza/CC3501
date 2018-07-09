

class Rectangle:
    def __init__(self, inf, sup):
        """
        Rectangle builder
        :param inf: Bottom coordinate
        :param sup: Top coordinate
        """
        self.inf = inf
        self.sup = sup

    def overlap(self, rect):
        """
        Check if this rectangle overlap the given rectangle.
        :param rect: Rectangle to check overlap.
        :return:
        """
        s = self
        c = rect

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
        """
        :return: String representative of the rectangle.
        """
        return "(" + str(self.inf) + ", " + str(self.sup) + ")"

    def move(self, pos):
        """
        Move the rectangle coordinate according to the given direction.
        :param pos: Vector to move.
        :return:
        """
        self.inf += pos
        self.sup += pos

    def __add__(self, vec):
        """
        The same as move, but operator.
        :param vec:
        :return:
        """
        return Rectangle(self.inf + vec, self.sup + vec)

    def __eq__(self, other):
        """
        Check if this rectangle equals to the given rectangle.
        :param other: Rectangle to compare.
        :return:
        """
        return self.inf == other.inf and self.sup == other.sup
