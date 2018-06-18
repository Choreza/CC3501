from cc3501utils.figure import Figure
from cc3501utils.vector import Vector
from OpenGL.GL import *
import random
from rectangle import Rectangle


class DBlock(Figure):
    def __init__(self, pjs, rgb=(1.0, 1.0, 1.0)):
        self.pjs = pjs
        self.physics = pjs.physics
        self.fire = None
        self.stype = 'dblock'

        self.rpos = None
        self.choose_rpos()
        self.pos = self.physics.scl_coord_res(self.rpos)
        self.rects = list()
        self.init_blocks()

        super().__init__(self.pos, rgb)

    def figure(self):
        lower = self.physics.scl_coord_res(self.rects[0].inf)
        upper = self.physics.scl_coord_res(self.rects[0].sup)
        upper += lower * -1
        lower += lower * -1

        glBegin(GL_QUADS)

        # Brick Background
        glColor3f(50 / 255, 50 / 255, 50 / 255)
        glVertex2f(lower.x, lower.y)
        glVertex2f(lower.x, upper.y)
        glVertex2f(upper.x, upper.y)
        glVertex2f(upper.x, lower.y)

        glEnd()

        glBegin(GL_QUADS)

        # Upper Brick
        glColor3f(80 / 255, 80 / 255, 80 / 255)
        glVertex2f(0.1 * upper.x, upper.y)
        glVertex2f(0.1 * upper.x, 0.72 * upper.y)
        glVertex2f(upper.x, 0.72 * upper.y)
        glVertex2f(upper.x, upper.y)

        # Mid left brick
        glVertex2f(lower.x, 0.67 * upper.y)
        glVertex2f(0.3 * upper.x, 0.67 * upper.y)
        glVertex2f(0.3 * upper.x, 0.39 * upper.y)
        glVertex2f(lower.x, 0.39 * upper.y)

        # Mid right brick
        glVertex2f(0.4 * upper.x, 0.67 * upper.y)
        glVertex2f(upper.x, 0.67 * upper.y)
        glVertex2f(upper.x, 0.39 * upper.y)
        glVertex2f(0.4 * upper.x, 0.39 * upper.y)

        # Bot left brick
        glVertex2f(lower.x, 0.34 * upper.y)
        glVertex2f(lower.x, 0.06 * upper.y)
        glVertex2f(0.6 * upper.x, 0.06 * upper.y)
        glVertex2f(0.6 * upper.x, 0.34 * upper.y)

        # Bot right brick
        glVertex2f(0.7 * upper.x, 0.34 * upper.y)
        glVertex2f(upper.x, 0.34 * upper.y)
        glVertex2f(upper.x, 0.06 * upper.y)
        glVertex2f(0.7 * upper.x, 0.06 * upper.y)

        glEnd()

        glBegin(GL_QUADS)
        glColor3f(100 / 255, 100 / 255, 100 / 255)

        # Top brick brightness
        glVertex2f(0.1 * upper.x, upper.y)
        glVertex2f(0.1 * upper.x, 0.95 * upper.y)
        glVertex2f(upper.x, 0.95 * upper.y)
        glVertex2f(upper.x, upper.y)

        glVertex2f(0.95 * upper.x, upper.y)
        glVertex2f(0.95 * upper.x, 0.72 * upper.y)
        glVertex2f(upper.x, 0.72 * upper.y)
        glVertex2f(upper.x, upper.y)

        # Mid left brightness
        glVertex2f(lower.x, 0.67 * upper.y)
        glVertex2f(0.3 * upper.x, 0.67 * upper.y)
        glVertex2f(0.3 * upper.x, 0.62 * upper.y)
        glVertex2f(lower.x, 0.62 * upper.y)

        glVertex2f(0.25 * upper.x, 0.67 * upper.y)
        glVertex2f(0.3 * upper.x, 0.67 * upper.y)
        glVertex2f(0.3 * upper.x, 0.39 * upper.y)
        glVertex2f(0.25 * upper.x, 0.39 * upper.y)

        # Mid right brightness
        glVertex2f(0.4 * upper.x, 0.67 * upper.y)
        glVertex2f(upper.x, 0.67 * upper.y)
        glVertex2f(upper.x, 0.62 * upper.y)
        glVertex2f(0.4 * upper.x, 0.62 * upper.y)

        # Bot left brightness
        glVertex2f(lower.x, 0.34 * upper.y)
        glVertex2f(lower.x, 0.29 * upper.y)
        glVertex2f(0.6 * upper.x, 0.29 * upper.y)
        glVertex2f(0.6 * upper.x, 0.34 * upper.y)

        glVertex2f(0.55 * upper.x, 0.34 * upper.y)
        glVertex2f(0.55 * upper.x, 0.06 * upper.y)
        glVertex2f(0.6 * upper.x, 0.06 * upper.y)
        glVertex2f(0.6 * upper.x, 0.34 * upper.y)

        # Bot right brightness
        glVertex2f(0.7 * upper.x, 0.34 * upper.y)
        glVertex2f(upper.x, 0.34 * upper.y)
        glVertex2f(upper.x, 0.29 * upper.y)
        glVertex2f(0.7 * upper.x, 0.29 * upper.y)

        glEnd()

    def is_destroyed(self):
        if self.fire and not(self.fire in self.pjs.fires):
            return True
        else:
            return False

    def init_blocks(self):
        length = self.physics.len_blocks
        rect = Rectangle(Vector(self.rpos.x, self.rpos.y),
                         Vector(self.rpos.x + length, self.rpos.y + length))
        self.rects.append(rect)
        self.physics.add_block(rect, self.stype)

    def choose_rpos(self):
        s = self
        blocks = s.physics.available_blocks
        block = blocks[random.randint(0, len(blocks) - 1)]
        s.physics.available_blocks.remove(block)
        s.rpos = block.inf

    def explode(self, fire):
        self.fire = fire

    def update(self):
        if self.is_destroyed():
            self.pjs.dblocks.remove(self)
            for rect in self.rects:
                if rect in self.physics.blocks[self.stype]:
                    self.physics.blocks[self.stype].remove(rect)
