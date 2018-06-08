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
        glBegin(GL_QUADS)
        glColor3f(0 / 255, 255 / 255, 255 / 255)
        cord = [(0, 0), (0, 50), (50, 50), (50, 0)]
        for p in cord:
            glVertex2f(p[0], p[1])
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
