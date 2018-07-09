from cc3501utils.figure import Figure
from cc3501utils.vector import Vector
from OpenGL.GL import *
import random
from rectangle import Rectangle


class Exit(Figure):
    def __init__(self, pjs, rgb=(1.0, 1.0, 1.0)):
        """
        Exit's builder.
        :param pjs: Vector representative of the initial position at the discrete grid.
        :param rgb: Not used. Required for superclass builder.
        """
        self.pjs = pjs
        self.physics = pjs.physics
        self.stype = 'exit'

        self.rpos = None
        self.choose_rpos()
        self.pos = self.physics.scl_coord_res(self.rpos)
        self.rects = list()
        self.init_blocks()

        super().__init__(self.pos, rgb)

    def figure(self):
        """
        Draws the character.
        :return:
        """
        lower = self.physics.scl_coord_res(self.rects[0].inf)
        upper = self.physics.scl_coord_res(self.rects[0].sup)
        upper += lower * -1
        lower += lower * -1

        glBegin(GL_QUADS)

        # Brick Background
        glColor3f(0.0 / 255, 255.0 / 255, 255.0 / 255)
        glVertex2f(lower.x, lower.y)
        glVertex2f(lower.x, upper.y)
        glVertex2f(upper.x, upper.y)
        glVertex2f(upper.x, lower.y)

        glColor3f(200.0 / 255, 200.0 / 255, 200.0 / 255)
        glVertex2f(lower.x, lower.y)
        glVertex2f(lower.x, 0.10 * upper.y)
        glVertex2f(upper.x, 0.10 * upper.y)
        glVertex2f(upper.x, lower.y)

        glVertex2f(lower.x, upper.y)
        glVertex2f(lower.x, 0.90 * upper.y)
        glVertex2f(upper.x, 0.90 * upper.y)
        glVertex2f(upper.x, upper.y)

        glVertex2f(lower.x, lower.y)
        glVertex2f(0.10 * upper.x, lower.y)
        glVertex2f(0.10 * upper.x, upper.y)
        glVertex2f(lower.x, upper.y)

        glVertex2f(upper.x, lower.y)
        glVertex2f(0.90 * upper.x, lower.y)
        glVertex2f(0.90 * upper.x, upper.y)
        glVertex2f(upper.x, upper.y)
        glEnd()

    def init_blocks(self):
        """
        Initializes the blocks at the discrete grid of blocks, representatives of the character.
        :return:
        """
        length = self.physics.len_blocks
        rect = Rectangle(Vector(self.rpos.x, self.rpos.y),
                         Vector(self.rpos.x + length, self.rpos.y + length))
        self.rects.append(rect)
        self.physics.add_block(rect, self.stype)

    def choose_rpos(self):
        """
        Choose a random position at the grid.
        :return:
        """
        s = self

        availablepos = []
        for dblock in s.pjs.dblocks:
            is_available = True

            for powerup in s.pjs.powerups:
                if powerup.rects[0].overlap(dblock.rects[0]):
                    is_available = False
                    break

            if is_available:
                availablepos.append(dblock.rpos)

        pos = random.randint(0, len(availablepos) - 1)
        s.rpos = availablepos[pos]
        print(s.rpos)

    def update(self):
        """
        Checks if a bombermen is over this exit.
        :return:
        """
        if self.pjs.bombermen:
            if self.rects[0] == self.pjs.bombermen[0].rects[0] and not self.pjs.enemies:
                self.pjs.bombermen[0].win()
