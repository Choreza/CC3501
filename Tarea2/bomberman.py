from cc3501utils.vector import Vector
from cc3501utils.figure import Figure
from OpenGL.GL import *
from bomb import Bomb
from rectangle import Rectangle


class Bomberman(Figure):
    def __init__(self, pjs, fps, rpos):
        self.pjs = pjs
        self.physics = pjs.physics

        self.stype = 'bomberman'
        self.bombs = 3
        self.bombradius = 2
        self.last_bomb = None
        self.killer = None

        self.direction = Vector(0, -1)

        # Speed must be smaller than max_steps
        self.speed = self.physics.len_blocks/32
        self.max_steps = self.physics.len_blocks/2
        self.steps = self.max_steps

        self.fps = fps
        self.timeout = 2 * fps

        self.rpos = rpos
        self.rects = list()
        self.init_blocks()
        self.pos = self.physics.scl_coord_res(self.rpos)
        super().__init__(self.pos, (1.0, 1.0, 1.0))
        self.clear_radius(2)

    def put_bomb(self):
        s = self
        if s.bombs == 0:
            return

        block = s.physics.blocks[s.stype][0]
        xinf = block.inf.x - block.inf.x % s.physics.len_blocks
        yinf = block.inf.y - block.inf.y % s.physics.len_blocks

        length = s.physics.len_blocks
        new_bomb = Rectangle(Vector(xinf, yinf), Vector(xinf + length, yinf + length))

        bombs = list()
        if 'bomb' in s.physics.blocks:
            bombs = s.physics.blocks['bomb']

        for bomb in bombs:
            if bomb.overlap(new_bomb):
                return

        bomb = Bomb(s, s.pjs, s.bombradius, s.fps, Vector(xinf, yinf))
        s.last_bomb = bomb
        s.pjs.add_bomb(bomb)
        s.bombs -= 1

    def move(self, direction, is_update=False):
        s = self

        if not self.is_moving():
            self.check_powerups()
            self.check_fires()
            self.check_enemies()
            if is_update:
                return

            s.direction = direction
            if s.physics.can_move_bomberman(self, direction) and not self.killer:
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
        if self.killer:
            if self.killer.stype == 'fire' and not (self.killer in self.pjs.fires):
                return True
            elif self.killer.stype == 'enemy' and self.timeout == 0:
                return True
        else:
            return False

    def init_blocks(self):
        length = self.physics.len_blocks
        rect = Rectangle(self.rpos, self.rpos + Vector(length, length))
        self.rects.append(rect)
        self.physics.add_block(rect, 'bomberman')

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
        for i in range(-radius, radius + 1):
            for j in range(-radius, radius + 1):
                block = Rectangle(Vector(i * length, j * length), Vector(length * (i + 1), length * (j + 1)))
                if not(block in self.physics.unavailable_blocks):
                    self.physics.unavailable_blocks.append(block)

    def check_powerups(self):
        for powerup in self.pjs.powerups:
            block = powerup.rects[0]
            if block.overlap(self.rects[0]):
                self.eat(powerup)

    def check_fires(self):
        for fire in self.pjs.fires:
            for block in fire.rects:
                if block.overlap(self.rects[0]):
                    self.killer = fire
                    return
        return

    def check_enemies(self):
        for enemy in self.pjs.enemies:
            for block in enemy.rects:
                if block.overlap(self.rects[0]):
                    self.killer = enemy
                    return

    def eat(self, powerup):
        powerup.consume_by(self)

    def die(self):
        self.pjs.bombermen.remove(self)
        for block in self.physics.blocks[self.stype]:
            if block == self.rects[0]:
                self.physics.blocks[self.stype].remove(block)

    def update(self):
        if self.killer:
            if self.killer.stype == 'fire' and not(self.killer in self.pjs.fires):
                self.die()
            elif self.killer.stype == 'enemy':
                if self.timeout == 0:
                    self.die()
                else:
                    self.timeout -= 1
        else:
            self.move(self.direction, is_update=True)
