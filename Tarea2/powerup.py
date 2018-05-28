from cc3501utils.figure import Figure
from cc3501utils.vector import Vector
from OpenGL.GL import *
from rectangle import Rectangle
import random


class PowerUp(Figure):
    def __init__(self, pjs, rgb=(1.0, 1.0, 1.0)):
        self.pjs = pjs
        self.physics = pjs.physics

        self.stype = 'powerup'

        self.rects = list()
        self.rpos = None
        self.choose_pos()
        self.pos = self.physics.scl_coord_res(self.rpos)
        self.init_blocks()

        self.options = ['bomb', 'radius', 'speed']
        self.power = random.randint(0, len(self.options) - 1)

        super().__init__(self.pos, rgb)

    def choose_pos(self):
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

    def init_blocks(self):
        length = self.physics.len_blocks
        rect = Rectangle(Vector(self.rpos.x, self.rpos.y),
                         Vector(self.rpos.x + length, self.rpos.y + length))
        self.rects.append(rect)
        self.physics.add_block(rect, self.stype)

    def increase_bombs(self, character):
        character.bombs += 1

    def increase_radius(self, character):
        character.bombradius += 1

    def increase_speed(self, character):
        character.speed = min(character.max_steps/4, character.speed * 2)

    def consume_by(self, character):
        power = self.options[self.power]
        if power == 'bomb':
            self.increase_bombs(character)

        elif power == 'radius':
            self.increase_radius(character)

        elif power == 'speed':
            self.increase_speed(character)

        self.physics.blocks['powerup'].remove(self.rects[0])
        self.pjs.powerups.remove(self)

    def figure(self):
        glBegin(GL_QUADS)
        glColor3f(0 / 255, 128.0 / 255, 0 / 255)
        cord = [(0, 0), (0, 50), (50, 50), (50, 0)]
        for p in cord:
            glVertex2f(p[0], p[1])
        glEnd()