from cc3501utils.vector import Vector
from cc3501utils.figure import Figure
from OpenGL.GL import *
from rectangle import Rectangle


class Fire(Figure):
    def __init__(self, pjs, radius, fps, pos, rgb=(1.0, 1.0, 1.0)):
        self.pjs = pjs
        self.physics = pjs.physics
        self.pos = pos
        self.radius = radius

        self.lifetime = 0
        self.timeout = 2*fps

        self.stype = 'fire'
        self.rpos = pos
        self.rects = list()
        self.pos = self.physics.scl_coord_res(self.rpos)
        self.init_blocks()
        super().__init__(self.pos, rgb)

    def init_blocks(self):
        s = self

        x = s.rpos.x
        y = s.rpos.y

        length = s.physics.len_blocks
        block = Rectangle(s.rpos, s.rpos + Vector(length, length))

        s.physics.add_block(block, s.stype)
        s.rects.append(block)

        directions = list()
        directions.append([])
        for i in range(1, s.radius):
            directions[0].append(Vector(x - i * length, y))

        directions.append([])
        for i in range(1, s.radius):
            directions[1].append(Vector(x + i * length, y))

        directions.append([])
        for i in range(1, s.radius):
            directions[2].append(Vector(x, y - i * length))

        directions.append([])
        for i in range(1, s.radius):
            directions[3].append(Vector(x, y + i * length))

        for direction in directions:
            overlap = False

            for p in direction:
                rect = Rectangle(p, p + Vector(length, length))

                # Checks if a bomb overlap in this direction.
                bombs = s.pjs.bombs
                for bomb in bombs:
                    block = bomb.rects[0]

                    # If overlaps, makes the bomb explode.
                    if block.overlap(rect):
                        bomb.explode()
                        overlap = True
                        break

                for dblock in s.pjs.dblocks:
                    if dblock.rects[0].overlap(rect):
                        overlap = True
                        dblock.explode(s)

                if not overlap:
                    # Checks if the fire block to insert overlaps the grid.
                    blocks = s.physics.blocks['sblock']
                    for block in blocks:
                        if block.overlap(rect):
                            overlap = True
                            break

                if not overlap:
                    s.rects.append(rect)
                    s.physics.add_block(rect, s.stype)

                else:
                    break

    def figure(self):
        glBegin(GL_QUADS)
        glColor3f(255 / 255, 165.0 / 255, 0 / 255)

        for block in self.rects:
            lower = self.physics.scl_coord_res(block.inf)
            upper = self.physics.scl_coord_res(block.sup)

            clower = self.physics.scl_coord_res(self.rects[0].inf)

            upper += clower * -1
            lower += clower * -1

            glVertex2f(lower.x, lower.y)
            glVertex2f(lower.x, upper.y)
            glVertex2f(upper.x, upper.y)
            glVertex2f(upper.x, lower.y)

        glEnd()

    def extinguish(self):
        s = self
        for b in s.rects:
            s.physics.blocks[s.stype].remove(b)
        s.pjs.fires.remove(s)

    def update(self):
        self.lifetime += 1
        if self.lifetime > self.timeout:
            self.extinguish()
