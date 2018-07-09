from cc3501utils.figure import Figure
from cc3501utils.vector import Vector
from OpenGL.GL import *
from rectangle import Rectangle
from fire import Fire
import numpy as np


class Bomb(Figure):
    def __init__(self, bomberman, pjs, radius, fps, pos, rgb=(1.0, 1.0, 1.0)):
        """
        Bomb builder, receives the bomberman who instantiated this bomb.
        :param bomberman: The bomberman who has instanciated this bomb.
        :param pjs: The list of characters.
        :param radius: Integer representing the radius of the bomb.
        :param fps: Integer representing the number of fps, used to calculate the time to explode.
        :param pos: Vector representative of the position in the screen.
        :param rgb: Not used. Required for the superclass builder.
        """
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
        """
        Initializes the list of blocks representatives of the bomb at the discrete grid.
        :return:
        """
        length = self.physics.len_blocks
        rect = Rectangle(Vector(self.rpos.x, self.rpos.y),
                         Vector(self.rpos.x + length, self.rpos.y + length))
        self.rects.append(rect)
        self.physics.add_block(rect, self.stype)

    def explode(self):
        """
        Makes the bomb disappear, creating a Fire object at the current position.
        :return:
        """
        s = self
        s.pjs.bombs.remove(s)
        s.bomberman.bombs += 1
        s.physics.blocks[s.stype].remove(s.rects[0])
        s.pjs.fires.append(Fire(s.pjs, s.radius, s.fps, s.rpos))

    def figure(self):
        """
        Draws the bomb.
        :return:
        """
        lower = self.physics.scl_coord_res(self.rects[0].inf)
        upper = self.physics.scl_coord_res(self.rects[0].sup)

        upper += lower * -1
        lower += lower * -1

        center = upper / 2
        radius = center.x

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
        b_radius = 0.5*(radius - abs(b_center))
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

    def update(self):
        """
        Checks if it's time to explode.
        :return:
        """
        self.lifetime += 1
        if self.lifetime >= self.timeout:
            self.explode()
