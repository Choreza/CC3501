from OpenGL.GL import *
from cc3501utils.vector import Vector


class Figure:
    def __init__(self, pos: Vector, rgb=(1.0, 1.0, 1.0)):
        self.pos = pos
        self.color = rgb
        self.list = 0
        self.create()

    def create(self):
        self.list = glGenLists(1)
        glNewList(self.list, GL_COMPILE)

        self.figure()

        glEndList()

    def draw(self):
        glPushMatrix()

        glColor3fv(self.color)
        glTranslatef(self.pos.x, self.pos.y, 0.0)
        glCallList(self.list)

        glPopMatrix()

    def figure(self):
        pass