from cc3501utils.vector import Vector
from cc3501utils.figure import Figure
from OpenGL.GL import *
from bomb import Bomb
import numpy as np
from rectangle import Rectangle


class Bomberman(Figure):
    def __init__(self, pjs, fps, rpos):
        """
        Bomberman builder
        :param pjs: The list of characters.
        :param fps: Integer representing the fps of the game.
        :param rpos: Vector of the position in the discrete grid.
        """
        self.pjs = pjs
        self.physics = pjs.physics

        self.stype = 'bomberman'
        self.bombs = 3
        self.bombradius = 2
        self.last_bomb = None
        self.killer = None

        self.direction = Vector(0, -1)

        # Speed must be smaller than max_steps
        self.speed = self.physics.len_blocks/64
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
        """
        Puts a bomb at the current position.
        :return:
        """
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
        """
        Move the character to the given direction
        :param direction: The direction to move
        :param is_update: boolean representative of an update, if true, will ignore the orders given by the
                          user until finish moving.
        :return:
        """
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
        """
        Gives a singles step in the given direction. Is used by the move method.
        :param direction:
        :return:
        """
        s = self
        s.steps += s.speed
        s.physics.move_bomberman(self, direction)
        s.update_pos()

    def update_pos(self):
        """
        Updates the character's position, at the discrete grid and the scaled version.
        :return:
        """
        s = self
        s.rpos = s.rects[0].inf
        s.pos = s.physics.scl_coord_res(s.rpos)

    def is_moving(self):
        """
        Checks if the character is moving, by looking the current steps.
        :return: True if isn't moving, else False.
        """
        return self.steps < self.max_steps

    def is_dead(self):
        """
        Checks if the character was burnt or touched by an enemy.
        :return: If one of the conditions above is met, return True.
        """
        if self.killer:
            if self.killer.stype == 'fire' and not (self.killer in self.pjs.fires):
                return True
            elif self.killer.stype == 'enemy' and self.timeout == 0:
                return True
        else:
            return False

    def init_blocks(self):
        """
        Initializes the blocks at the discrete grid of blocks, representatives of the character.
        :return:
        """
        length = self.physics.len_blocks
        rect = Rectangle(self.rpos, self.rpos + Vector(length, length))
        self.rects.append(rect)
        self.physics.add_block(rect, 'bomberman')

    def figure(self):
        """
        Draws the character.
        :return:
        """
        lower = self.physics.scl_coord_res(self.rects[0].inf)
        upper = self.physics.scl_coord_res(self.rects[0].sup)

        upper += lower * -1
        lower += lower * -1

        # Legs
        glBegin(GL_QUADS)
        glColor3f(255.0 / 255, 255.0 / 255, 255.0 / 255)
        glVertex2f(0.60 * upper.x, 0.35 * upper.y)
        glVertex2f(0.78 * upper.x, 0.35 * upper.y)
        glVertex2f(0.78 * upper.x, 0.00 * upper.y)
        glVertex2f(0.60 * upper.x, 0.00 * upper.y)

        glVertex2f(0.40 * upper.x, 0.35 * upper.y)
        glVertex2f(0.22 * upper.x, 0.35 * upper.y)
        glVertex2f(0.22 * upper.x, 0.00 * upper.y)
        glVertex2f(0.40 * upper.x, 0.00 * upper.y)

        # Foots
        glColor3f(255.0 / 255, 0.0 / 255, 255.0 / 255)
        glVertex2f(0.60 * upper.x, 0.15 * upper.y)
        glVertex2f(0.78 * upper.x, 0.15 * upper.y)
        glVertex2f(0.78 * upper.x, 0.00 * upper.y)
        glVertex2f(0.60 * upper.x, 0.00 * upper.y)

        glVertex2f(0.40 * upper.x, 0.15 * upper.y)
        glVertex2f(0.22 * upper.x, 0.15 * upper.y)
        glVertex2f(0.22 * upper.x, 0.00 * upper.y)
        glVertex2f(0.40 * upper.x, 0.00 * upper.y)
        glEnd()

        # Torso
        center = upper / 2
        radius = 0.6 * center.x

        n = 30
        d_theta = 2 * np.pi / n
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(0.0 / 255, 0 / 255, 255.0 / 255)
        glVertex2f(center.x, center.y)
        for i in range(n + 1):
            rx = center.x + 0.95 * radius * np.cos(i * d_theta)
            ry = center.y + radius * np.sin(i * d_theta)
            glVertex2f(rx, ry)
        glEnd()

        # Arms
        glBegin(GL_QUADS)
        glColor3f(255.0 / 255, 255.0 / 255, 255.0 / 255)
        glVertex2f(0.78 * upper.x, 0.65 * upper.y)
        glVertex2f(0.90 * upper.x, 0.65 * upper.y)
        glVertex2f(0.90 * upper.x, 0.30 * upper.y)
        glVertex2f(0.78 * upper.x, 0.30 * upper.y)

        glVertex2f(0.22 * upper.x, 0.65 * upper.y)
        glVertex2f(0.10 * upper.x, 0.65 * upper.y)
        glVertex2f(0.10 * upper.x, 0.30 * upper.y)
        glVertex2f(0.22 * upper.x, 0.30 * upper.y)

        # Hands
        glColor3f(255.0 / 255, 0.0 / 255, 255.0 / 255)
        glVertex2f(0.78 * upper.x, 0.42 * upper.y)
        glVertex2f(0.90 * upper.x, 0.42 * upper.y)
        glVertex2f(0.90 * upper.x, 0.30 * upper.y)
        glVertex2f(0.78 * upper.x, 0.30 * upper.y)

        glVertex2f(0.22 * upper.x, 0.42 * upper.y)
        glVertex2f(0.10 * upper.x, 0.42 * upper.y)
        glVertex2f(0.10 * upper.x, 0.30 * upper.y)
        glVertex2f(0.22 * upper.x, 0.30 * upper.y)

        # Belt
        glColor3f(0.0 / 255, 0.0 / 255, 0.0 / 255)
        glVertex2f(0.25 * upper.x, 0.40 * upper.y)
        glVertex2f(0.25 * upper.x, 0.45 * upper.y)
        glVertex2f(0.75 * upper.x, 0.45 * upper.y)
        glVertex2f(0.75 * upper.x, 0.40 * upper.y)

        glColor3f(255.0 / 255, 255.0 / 255, 0.0 / 255)
        glVertex2f(0.45 * upper.x, 0.40 * upper.y)
        glVertex2f(0.45 * upper.x, 0.45 * upper.y)
        glVertex2f(0.55 * upper.x, 0.45 * upper.y)
        glVertex2f(0.55 * upper.x, 0.40 * upper.y)
        glEnd()

        # Bonnet

        center = upper / 2
        radius = 0.2 * center.x
        center += Vector(0, 0.9 * upper.y)

        n = 30
        d_theta = 2 * np.pi / n
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(255.0 / 255, 0.0 / 255, 255.0 / 255)
        glVertex2f(center.x, center.y)
        for i in range(n + 1):
            rx = center.x + radius * np.cos(i * d_theta)
            ry = center.y + radius * np.sin(i * d_theta)
            glVertex2f(rx, ry)
        glEnd()


        # Head
        center = upper / 2
        radius = 0.9 * center.x
        center += Vector(0, upper.y/2)

        n = 30
        d_theta = 2 * np.pi / n
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(255.0 / 255, 255.0 / 255, 255.0 / 255)
        glVertex2f(center.x, center.y)
        for i in range(n + 1):
            rx = center.x + radius * np.cos(i * d_theta)
            ry = center.y + 0.95 * radius * np.sin(i * d_theta)
            glVertex2f(rx, ry)
        glEnd()

        glBegin(GL_QUADS)
        # Skin
        glColor3f(255.0 / 255, 173.0 / 255, 96.0 / 255)
        glVertex2f(0.82 * upper.x, 0.70 * upper.y)
        glVertex2f(0.82 * upper.x, 1.00 * upper.y)
        glVertex2f(0.18 * upper.x, 1.00 * upper.y)
        glVertex2f(0.18 * upper.x, 0.70 * upper.y)

        # Mask
        glColor3f(255.0 / 255, 0.0 / 255, 0.0 / 255)
        glVertex2f(0.77 * upper.x, 0.70 * upper.y)
        glVertex2f(0.77 * upper.x, 1.00 * upper.y)
        glVertex2f(0.82 * upper.x, 1.00 * upper.y)
        glVertex2f(0.82 * upper.x, 0.70 * upper.y)

        glVertex2f(0.25 * upper.x, 0.70 * upper.y)
        glVertex2f(0.25 * upper.x, 1.00 * upper.y)
        glVertex2f(0.18 * upper.x, 1.00 * upper.y)
        glVertex2f(0.18 * upper.x, 0.70 * upper.y)

        glVertex2f(0.77 * upper.x, 0.70 * upper.y)
        glVertex2f(0.77 * upper.x, 0.62 * upper.y)
        glVertex2f(0.25 * upper.x, 0.62 * upper.y)
        glVertex2f(0.25 * upper.x, 0.70 * upper.y)

        glVertex2f(0.77 * upper.x, 1.08 * upper.y)
        glVertex2f(0.77 * upper.x, 1.00 * upper.y)
        glVertex2f(0.25 * upper.x, 1.00 * upper.y)
        glVertex2f(0.25 * upper.x, 1.08 * upper.y)

        # Eyes
        glColor3f(0.0 / 255, 0.0 / 255, 0.0 / 255)
        glVertex2f(0.60 * upper.x, 0.70 * upper.y)
        glVertex2f(0.60 * upper.x, 1.00 * upper.y)
        glVertex2f(0.66 * upper.x, 1.00 * upper.y)
        glVertex2f(0.66 * upper.x, 0.70 * upper.y)

        glVertex2f(0.35 * upper.x, 0.70 * upper.y)
        glVertex2f(0.35 * upper.x, 1.00 * upper.y)
        glVertex2f(0.40 * upper.x, 1.00 * upper.y)
        glVertex2f(0.40 * upper.x, 0.70 * upper.y)
        glEnd()
        
    def clear_radius(self, radius):
        """
        Clear the radius around the character, removing destructive blocks, to guarantee initial movement.
        :param radius: Integer representing the radius to clear.
        :return:
        """
        s = self
        length = self.physics.len_blocks
        for i in range(-radius, radius + 1):
            for j in range(-radius, radius + 1):
                block = Rectangle(Vector(i * length, j * length), Vector(length * (i + 1), length * (j + 1)))
                if not(block in self.physics.unavailable_blocks):
                    self.physics.unavailable_blocks.append(block)

    def check_powerups(self):
        """
        Checks if the character is walking over a powerup.
        :return:
        """
        for powerup in self.pjs.powerups:
            block = powerup.rects[0]
            if block.overlap(self.rects[0]):
                self.eat(powerup)

    def check_fires(self):
        """
        Checks if the character is burnt by a fire object.
        :return:
        """
        for fire in self.pjs.fires:
            for block in fire.rects:
                if block.overlap(self.rects[0]):
                    self.killer = fire
                    return
        return

    def check_enemies(self):
        """
        Check if the character is touched by an enemy.
        :return:
        """
        for enemy in self.pjs.enemies:
            for block in enemy.rects:
                if block.overlap(self.rects[0]):
                    self.killer = enemy
                    return

    def eat(self, powerup):
        """
        Consume the given powerup.
        :param powerup:
        :return:
        """
        powerup.consume_by(self)

    def win(self):
        """
        Disappear if win the game.
        :return:
        """
        self.die()

    def die(self):
        """
        Remove the character from the game.
        :return:
        """
        self.pjs.bombermen.remove(self)
        for block in self.physics.blocks[self.stype]:
            if block == self.rects[0]:
                self.physics.blocks[self.stype].remove(block)

    def update(self):
        """
        Checks the possibles ways to day or to win, executing the corresponding action. If the character doesn't
        die or win, then moves.
        :return:
        """
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
