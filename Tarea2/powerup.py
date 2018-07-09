from cc3501utils.figure import Figure
from cc3501utils.vector import Vector
from OpenGL.GL import *
from rectangle import Rectangle
import random
import numpy as np


class PowerUp(Figure):
    def __init__(self, pjs, rgb=(1.0, 1.0, 1.0)):
        """
        DBlock builder.
        :param pjs: The list of characters.
        :param rgb: Not used. Required for the superclass builder.
        """
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

    def increase_bombs(self, character):
        """
        Increase in 1 the bombs of the given character.
        :param character: Character to give one bomb.
        :return:
        """
        character.bombs += 1

    def increase_radius(self, character):
        """
        Increase in 1 the radius of the bombs of the given character.
        :param character:
        :return:
        """
        character.bombradius += 1

    def increase_speed(self, character):
        """
        Multiplies by 0.25 the speed of the given character.
        :param character:
        :return:
        """
        character.speed = min(character.max_steps/4, character.speed * 1.25)

    def consume_by(self, character):
        """
        Removes itself, if the given character calls this method. Giving the corresponding powerup to the character.
        :param character: Character who calls this method.
        :return:
        """
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
        """
        Draws the powerup
        :return:
        """
        lower = self.physics.scl_coord_res(self.rects[0].inf)
        upper = self.physics.scl_coord_res(self.rects[0].sup)
        upper += lower * -1
        lower += lower * -1

        glBegin(GL_QUADS)
        glColor3f(255 / 255, 0 / 255, 0 / 255)

        glVertex2f(upper.x, upper.y)
        glVertex2f(upper.x, lower.y)
        glVertex2f(lower.x, lower.y)
        glVertex2f(lower.x, upper.y)

        power = self.options[self.power]
        if power == 'radius':
            glColor3f(153.0 / 255, 255 / 255, 204.0 / 255)
        elif power == 'speed':
            glColor3f(0 / 255, 255 / 255, 0 /255)
        elif power == 'bomb':
            glColor3f(153.0 / 255, 255 / 255, 204.0 / 255)
        glVertex2f(0.1 * upper.x, 0.1 * upper.y)
        glVertex2f(0.1 * upper.x, 0.9 * upper.y)
        glVertex2f(0.9 * upper.x, 0.9 * upper.y)
        glVertex2f(0.9 * upper.x, 0.1 * upper.y)

        glEnd()

        if power == 'radius':
            center = upper / 2
            radius = 0.7 * center.x

            # Fire Head
            n = 30
            d_theta = 2 * np.pi / n
            glBegin(GL_TRIANGLE_FAN)
            glColor3f(255 / 255, 69.0 / 255, 0.0 / 255)
            glVertex2f(center.x, center.y)
            for i in range(n + 1):
                rx = center.x + radius * np.cos(d_theta * i)
                ry = 0.9 * center.y + radius * np.sin(d_theta * i)
                glVertex2f(rx, ry)
            glEnd()

            # Fire hair
            glBegin(GL_TRIANGLES)

            glVertex2f(center.x, center.y)
            glVertex2f(center.x + radius, center.y)
            glVertex2f(center.x + radius, center.y + radius * 1.2)

            glVertex2f(0.7 * center.x, center.y)
            glVertex2f(0.7 * center.x + radius, center.y)
            glVertex2f(0.7 * center.x + radius, center.y + radius * 1.2)

            glVertex2f(0.4 * center.x, center.y)
            glVertex2f(0.4 * center.x + radius, center.y)
            glVertex2f(0.4 * center.x + radius, center.y + radius * 1.2)

            glEnd()

            # Fire eyes
            glBegin(GL_QUADS)
            glColor3f(255 / 255, 255.0 / 255, 255.0 / 255)

            glVertex2f(1.0 * center.x, 1.1 * center.y)
            glVertex2f(1.0 * center.x, 0.7 * center.y)
            glVertex2f(1.2 * center.x, 0.7 * center.y)
            glVertex2f(1.2 * center.x, 1.1 * center.y)

            glVertex2f(0.9 * center.x, 1.1 * center.y)
            glVertex2f(0.9 * center.x, 0.7 * center.y)
            glVertex2f(0.7 * center.x, 0.7 * center.y)
            glVertex2f(0.7 * center.x, 1.1 * center.y)

            glColor3f(0.0 / 255, 0.0 / 255, 0.0 / 255)

            glVertex2f(1.0 * center.x, 1.0 * center.y)
            glVertex2f(1.0 * center.x, 0.7 * center.y)
            glVertex2f(1.1 * center.x, 0.7 * center.y)
            glVertex2f(1.1 * center.x, 1.0 * center.y)

            glVertex2f(0.75 * center.x, 1.0 * center.y)
            glVertex2f(0.75 * center.x, 0.7 * center.y)
            glVertex2f(0.7 * center.x, 0.7 * center.y)
            glVertex2f(0.7 * center.x, 1.0 * center.y)

            glEnd()

            # Fire mouth
            glBegin(GL_LINES)
            glVertex2f(0.7 * center.x, 0.6 * center.y)
            glVertex2f(1.2 * center.x, 0.6 * center.y)

            glVertex2f(1.2 * center.x, 0.6 * center.y)
            glVertex2f(1.0 * center.x, 0.4 * center.y)

            glVertex2f(0.7 * center.x, 0.6 * center.y)
            glVertex2f(0.9 * center.x, 0.4 * center.y)

            glVertex2f(1.0 * center.x, 0.4 * center.y)
            glVertex2f(0.9 * center.x, 0.4 * center.y)
            glEnd()

        if power == 'speed':
            # Shoe
            center = upper / 2
            radius = 0.7 * center.x
            n = 30
            d_theta = 2 * np.pi / n
            glBegin(GL_TRIANGLE_FAN)
            glColor3f(0.0 / 255, 255.0 / 255, 255.0 / 255)
            glVertex2f(0.7 * center.x, 0.8 * center.y)
            for i in range(n + 1):
                rx = 0.7 * center.x + 0.5 * radius * np.cos(d_theta * i)
                ry = 0.8 * center.y + 0.5 * radius * np.sin(d_theta * i)
                glVertex2f(rx, ry)
            glEnd()

            glBegin(GL_TRIANGLE_FAN)
            glVertex2f(1.3 * center.x, 0.8 * center.y)
            for i in range(n + 1):
                rx = 1.3 * center.x + 0.5 * radius * np.cos(d_theta * i)
                ry = 0.8 * center.y + 0.5 * radius * np.sin(d_theta * i)
                glVertex2f(rx, ry)
            glEnd()

            glBegin(GL_QUADS)
            glVertex2f(0.7 * center.x, 0.8 * center.y + 0.5 * radius)
            glVertex2f(1.3 * center.x, 0.8 * center.y + 0.5 * radius)
            glVertex2f(0.7 * center.x, 0.8 * center.y - 0.5 * radius)
            glVertex2f(1.3 * center.x, 0.8 * center.y - 0.5 * radius)

            glVertex2f(0.9 * center.x, 0.8 * center.y + 1.3 * radius)
            glVertex2f(1.6 * center.x, 0.8 * center.y + 1.3 * radius)
            glVertex2f(1.6 * center.x, 0.8 * center.y - 0.5 * radius)
            glVertex2f(0.9 * center.x, 0.8 * center.y - 0.5 * radius)
            glEnd()

            # Shoe shoelaces
            glLineWidth(3.0)
            glBegin(GL_LINES)
            glColor3f(255.0 / 255, 0.0 / 255, 0.0 / 255)
            glVertex2f(0.9 * center.x, 0.8 * center.y + 1.3 * radius)
            glVertex2f(1.6 * center.x, 0.8 * center.y + 1.3 * radius)

            glVertex2f(0.8 * center.x, 0.8 * center.y + 1.0 * radius)
            glVertex2f(1.2 * center.x, 0.8 * center.y + 1.0 * radius)

            glVertex2f(0.8 * center.x, 0.8 * center.y + 0.7 * radius)
            glVertex2f(1.2 * center.x, 0.8 * center.y + 0.7 * radius)
            glEnd()

            # Shoe wheels
            center = upper / 2
            radius = 0.7 * center.x
            n = 30
            d_theta = 2 * np.pi / n
            glBegin(GL_TRIANGLE_FAN)
            glColor3f(255 / 255, 69.0 / 255, 0.0 / 255)
            glVertex2f(0.7 * center.x, 0.5 * center.y)
            for i in range(n + 1):
                rx = 0.7 * center.x + 0.3 * radius * np.cos(d_theta * i)
                ry = 0.5 * center.y + 0.3 * radius * np.sin(d_theta * i)
                glVertex2f(rx, ry)
            glEnd()

            glBegin(GL_TRIANGLE_FAN)
            glVertex2f(1.3 * center.x, 0.5 * center.y)
            for i in range(n + 1):
                rx = 1.3 * center.x + 0.3 * radius * np.cos(d_theta * i)
                ry = 0.5 * center.y + 0.3 * radius * np.sin(d_theta * i)
                glVertex2f(rx, ry)
            glEnd()

            center = upper / 2
            radius = 0.7 * center.x
            n = 30
            d_theta = 2 * np.pi / n
            glBegin(GL_TRIANGLE_FAN)
            glColor3f(0 / 255, 0.0 / 255, 0.0 / 255)
            glVertex2f(0.7 * center.x, 0.5 * center.y)
            for i in range(n + 1):
                rx = 0.7 * center.x + 0.1 * radius * np.cos(d_theta * i)
                ry = 0.5 * center.y + 0.1 * radius * np.sin(d_theta * i)
                glVertex2f(rx, ry)
            glEnd()

            glBegin(GL_TRIANGLE_FAN)
            glVertex2f(1.3 * center.x, 0.5 * center.y)
            for i in range(n + 1):
                rx = 1.3 * center.x + 0.1 * radius * np.cos(d_theta * i)
                ry = 0.5 * center.y + 0.1 * radius * np.sin(d_theta * i)
                glVertex2f(rx, ry)
            glEnd()
        elif power == 'bomb':
            center = upper / 2
            radius = 0.8 * center.x

            n = 30
            d_theta = 2 * np.pi / n
            glBegin(GL_TRIANGLE_FAN)
            glColor3f(0.0 / 255, 0.0 / 255, 0.0 / 255)
            glVertex2f(center.x, center.y)
            for i in range(n + 1):
                rx = center.x + radius * np.cos(d_theta * i)
                ry = center.y + radius * np.sin(d_theta * i)
                glVertex2f(rx, ry)
            glEnd()

            alpha = 0.75 * np.pi
            vec_radius = Vector(radius * np.cos(alpha), radius * np.sin(alpha))
            brightness = 10
            for b in range(1, brightness + 1):
                b_center = vec_radius * b / brightness
                b_radius = (radius - abs(b_center))

                glBegin(GL_TRIANGLE_FAN)
                glColor3f((100 / brightness) * (b + 1) / 255.0,
                          (100 / brightness) * (b + 1) / 255.0,
                          (100 / brightness) * (b + 1) / 255.0)

                glVertex2f(b_center.x + center.x, b_center.y + center.y)
                for i in range(n + 1):
                    rx = b_center.x + center.x + b_radius * np.cos(d_theta * i)
                    ry = b_center.y + center.y + b_radius * np.sin(d_theta * i)
                    glVertex2f(rx, ry)
                glEnd()

            alpha = 0.25 * np.pi
            vec_radius = Vector(radius * np.cos(alpha), radius * np.sin(alpha))
            b_center = vec_radius * 0.7
            b_radius = (radius - abs(b_center))
            glBegin(GL_TRIANGLE_FAN)
            glColor3f(0.0 / 255, 0.0 / 255, 0.0 / 255)
            glVertex2f(b_center.x + center.x, b_center.y + center.y)
            for i in range(n + 1):
                rx = b_center.x + center.x + b_radius * np.cos(d_theta * i)
                ry = b_center.y + center.y + b_radius * np.sin(d_theta * i)
                glVertex2f(rx, ry)
            glEnd()

            alpha = 0.25 * np.pi
            vec_radius = Vector(radius * np.cos(alpha), radius * np.sin(alpha))
            b_center = vec_radius * 0.7
            b_radius = 0.8 * (radius - abs(b_center))
            glBegin(GL_TRIANGLE_FAN)
            glColor3f(10.0 / 255, 10.0 / 255, 10.0 / 255)
            glVertex2f(b_center.x + center.x, b_center.y + center.y)
            for i in range(n + 1):
                rx = b_center.x + center.x + b_radius * np.cos(d_theta * i)
                ry = b_center.y + center.y + b_radius * np.sin(d_theta * i)
                glVertex2f(rx, ry)
            glEnd()

            alpha = 0.25 * np.pi
            vec_radius = Vector(radius * np.cos(alpha), radius * np.sin(alpha))
            b_center = vec_radius * 0.7
            b_radius = 0.5 * (radius - abs(b_center))
            glBegin(GL_TRIANGLE_FAN)
            glColor3f(20.0 / 255, 20.0 / 255, 20.0 / 255)
            glVertex2f(b_center.x + center.x, b_center.y + center.y)
            for i in range(n + 1):
                rx = b_center.x + center.x + b_radius * np.cos(d_theta * i)
                ry = b_center.y + center.y + b_radius * np.sin(d_theta * i)
                glVertex2f(rx, ry)
            glEnd()

            glLineWidth(5.0)
            glBegin(GL_LINES)
            glColor3f(255 / 255, 69.0 / 255, 0.0 / 255)
            glVertex2f(center.x + vec_radius.x * 0.7, center.y + vec_radius.y * 0.7)
            glVertex2f(upper.x, upper.y)

            glColor3f(255 / 255, 165.0 / 255, 0.0 / 255)
            glVertex2f(center.x + vec_radius.x * 0.7, center.y + vec_radius.y * 0.7)
            glVertex2f(upper.x * 0.95, upper.y * 0.95)

            glColor3f(180.0 / 255, 180.0 / 255, 180.0 / 255)
            glVertex2f(center.x + vec_radius.x * 0.7, center.y + vec_radius.y * 0.7)
            glVertex2f(upper.x * 0.9, upper.y * 0.9)

            glEnd()

            glLineWidth(2.0)
            glBegin(GL_LINES)
            glColor3f(20.0 / 255, 20.0 / 255, 20.0 / 255)
            glVertex2f(center.x + vec_radius.x * 0.7, center.y + vec_radius.y * 0.7)
            glVertex2f(center.x + vec_radius.x * 0.9, center.y + vec_radius.y * 0.7)

            glVertex2f(center.x + vec_radius.x * 0.7, center.y + vec_radius.y * 0.6)
            glVertex2f(center.x + vec_radius.x * 0.9, center.y + vec_radius.y * 0.7)
            glEnd()
