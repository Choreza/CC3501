from cc3501utils.vector import Vector
from cc3501utils.figure import Figure
from OpenGL.GL import *
import random
from rectangle import Rectangle


class Enemy(Figure):
    def __init__(self, pjs, fps):
        self.pjs = pjs
        self.physics = pjs.physics

        self.stype = 'enemy'
        self.killer = None

        self.direction = Vector(0, -1)
        self.directions = [Vector(0, -1), Vector(0, 1), Vector(1, 0), Vector(-1, 0)]

        # Speed must be smaller than max_steps
        self.speed = self.physics.len_blocks/32
        self.max_steps = self.physics.len_blocks/2
        self.steps = self.max_steps

        self.fps = fps

        self.rpos = None
        self.choose_rpos()
        self.rects = list()
        self.init_blocks()
        self.pos = self.physics.scl_coord_res(self.rpos)
        super().__init__(self.pos, (1.0, 1.0, 1.0))

    def move(self, direction, is_update=False):
        s = self

        if not self.is_moving():
            self.check_fires()
            if is_update:
                return

            s.direction = direction
            can_move = False
            for d in s.directions:
                can_move = can_move or s.physics.can_move_enemy(self, d)

            if not can_move:
                return

            while not s.physics.can_move_enemy(self, s.direction):
                s.direction = s.directions[random.randint(0, 3)]

            if s.physics.can_move_enemy(self, s.direction) and not self.killer:
                    s.steps = 0
                    s.move(s.direction)

        else:
            speed = min(s.speed, s.max_steps - s.steps)
            s.step_to(s.direction * speed)

    def step_to(self, direction):
        s = self
        s.steps += s.speed
        s.physics.move_bomberman(self, direction)
        s.update_pos()

    def update_pos(self):
        s = self
        s.rpos = s.rects[0].inf
        s.pos = s.physics.scl_coord_res(s.rpos)

    def is_moving(self):
        return self.steps < self.max_steps

    def is_dead(self):
        is_dead = self.killer != None
        is_dead = is_dead and not(self.killer in self.pjs.fires)
        return is_dead

    def init_blocks(self):
        length = self.physics.len_blocks
        rect = Rectangle(self.rpos, self.rpos + Vector(length, length))
        self.rects.append(rect)
        self.physics.add_block(rect, self.stype)

    def figure(self):
        glBegin(GL_QUADS)
        glColor3f(255 / 255, 0 / 255, 0 / 255)

        lower = self.physics.scl_coord_res(self.rects[0].inf)
        upper = self.physics.scl_coord_res(self.rects[0].sup)

        upper += lower * -1
        lower += lower * -1

        glVertex2f(lower.x, lower.y)
        glVertex2f(lower.x, upper.y)
        glVertex2f(upper.x, upper.y)
        glVertex2f(upper.x, lower.y)

        glEnd()

    def clear_radius(self, radius):
        s = self
        length = self.physics.len_blocks

        i = -radius * length
        j = -radius * length

        while i < radius * length:
            while j < radius * length:
                arect = Rectangle(s.rpos + Vector(i, j), s.rpos + Vector(i + length, j + length))
                for dblock in s.pjs.dblocks:
                    for rect in dblock.rects:
                        if arect.overlap(rect):
                            s.pjs.dblocks.remove(dblock)
                            s.physics.blocks['dblock'].remove(rect)
                            break
                j += length
            j = -radius * length
            i += length

    def check_fires(self):
        for fire in self.pjs.fires:
            for block in fire.rects:
                if block.overlap(self.rects[0]):
                    self.killer = fire
                    return
        return

    def eat(self, powerup):
        powerup.consume_by(self)

    def die(self):
        self.pjs.enemies.remove(self)
        for block in self.physics.blocks[self.stype]:
            if block == self.rects[0]:
                self.physics.blocks[self.stype].remove(block)

    def choose_rpos(self):
        s = self
        blocks = s.physics.available_blocks
        block = blocks[random.randint(0, len(blocks) - 1)]
        s.physics.available_blocks.remove(block)
        s.rpos = block.inf

    def update(self):
        if self.killer and not(self.killer in self.pjs.fires):
            self.die()
        else:
            self.move(self.direction)
