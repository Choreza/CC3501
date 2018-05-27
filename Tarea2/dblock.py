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
        self.choose_pos()
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

    def choose_pos(self):
        s = self
        length = s.physics.len_blocks

        x = 0
        y = 0

        for i in range(len(s.pjs.grid.rects)):
            x = max(x, s.pjs.grid.rects[i].inf.x)
            y = max(y, s.pjs.grid.rects[i].inf.y)

        i = 0
        j = 0
        availablecoords = list()
        while i <= x:
            while j <= y:
                arect = Rectangle(Vector(i, j), Vector(i + length, j + length))

                isavailable = True
                for rect in s.pjs.grid.rects:
                    if rect.overlap(arect):
                        isavailable = False
                        break

                if isavailable:
                    for dblock in s.pjs.dblocks:
                        for rect in dblock.rects:
                            if rect.overlap(arect):
                                isavailable = False
                                break

                if isavailable:
                    for bomberman in s.pjs.bombermen:
                        if bomberman.rects[0].overlap(arect):
                            isavailable = False

                if isavailable:
                    availablecoords.append(arect)
                j += length
            j = 0
            i += length

        ran = random.randint(0, len(availablecoords) - 1)
        s.rpos = availablecoords[ran].inf

    def explode(self, fire):
        self.fire = fire

    def update(self):
        if self.is_destroyed():
            self.pjs.dblocks.remove(self)
            for rect in self.rects:
                if rect in self.physics.blocks[self.stype]:
                    self.physics.blocks[self.stype].remove(rect)
