from cc3501utils.figure import Figure
from cc3501utils.vector import Vector
from OpenGL.GL import *
from rectangle import Rectangle
from fire import Fire
import numpy as np


class Bomb(Figure):
    def __init__(self, bomberman, pjs, radius, fps, pos, rgb=(1.0, 1.0, 1.0)):
        self.pjs = pjs
        self.bomberman = bomberman
        self.physics = pjs.physics

        self.fps = fps
        self.lifetime = 0
        self.timeout = 3*fps

        self.radius = radius
        self.rects = list()
        self.stype = 'bomb'
        self.rpos = pos
        self.init_blocks()
        self.pos = self.physics.scl_coord_res(pos)
        super().__init__(self.pos, rgb)

    def init_blocks(self):
        length = self.physics.len_blocks
        rect = Rectangle(Vector(self.rpos.x, self.rpos.y),
                         Vector(self.rpos.x + length, self.rpos.y + length))
        self.rects.append(rect)
        self.physics.add_block(rect, self.stype)

    def explode(self):
        s = self
        s.pjs.bombs.remove(s)
        s.bomberman.bombs += 1
        s.physics.blocks[s.stype].remove(s.rects[0])
        s.pjs.fires.append(Fire(s.pjs, s.radius, s.fps, s.rpos))

    def figure(self):
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(0 / 255, 0 / 255, 0 / 255)

        lower = self.physics.scl_coord_res(self.rects[0].inf)
        upper = self.physics.scl_coord_res(self.rects[0].sup)

        upper += lower * -1
        lower += lower * -1

        cx = upper.x/2.0
        cy = upper.y/2.0
        r = cx
        delta = 2 * np.pi / 20
        glVertex2f(cx, cy)
        for i in range(21):
            glVertex2f(cx + r * np.cos(i * delta), cy + r * np.sin(i * delta))
        glEnd()

    def update(self):
        self.lifetime += 1
        if self.lifetime >= self.timeout:
            self.explode()
