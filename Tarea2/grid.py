from cc3501utils.figure import Figure
from cc3501utils.vector import Vector
from OpenGL.GL import *
from rectangle import Rectangle


class Grid(Figure):
    def __init__(self, pjs, pos=Vector(0, 0), rgb=(1.0, 1.0, 1.0)):
        self.cols = pjs.physics.cols
        self.rows = pjs.physics.rows

        self.pjs = pjs
        self.physics = pjs.physics

        self.rects = list()
        self.init_blocks()
        super().__init__(pos, rgb)

    def init_blocks(self):
        """
        Initializes the blocks of the grid, adding them to the list of blocks
        of the physics.
        :return:
        """
        col = self.cols
        row = self.rows
        matrix = [[1 for x in range(col)] for y in range(row)]
        for i in range(1, row - 1):
            for j in range(1, col - 1):
                if (i % 2 == 1 and j % 2 == 1) or (i % 2 != j % 2):
                    matrix[i][j] = 0

        length = self.physics.len_blocks
        for i in range(col):
            for j in range(row):
                if matrix[j][i]:
                    x = i * length
                    y = j * length
                    block = Rectangle(Vector(x, y), Vector(x + length, y + length))
                    self.physics.add_block(block, 'sblock')
                    self.rects.append(block)

    def scale_resolution(self, blocks):
        """
        Takes the discrete version for the coordinates list of the blocks
        and returns a list scaled according to the screen resolution.
        :param blocks:
        :return:
        """
        real_x = self.physics.real_width
        real_y = self.physics.real_height

        discrete_x = self.physics.width
        discrete_y = self.physics.height

        xf = float(real_x)/discrete_x
        yf = float(real_y)/discrete_y
        real_blocks = list()
        for block in blocks:
            b = Rectangle(Vector(block.inf.x * xf, block.inf.y * yf),
                          Vector(block.sup.x * xf, block.sup.y * yf))
            real_blocks.append(b)
        return real_blocks

    def figure(self):
        glBegin(GL_QUADS)

        glColor3f(80 / 255, 80 / 255, 80 / 255)

        blocks = self.scale_resolution(self.physics.blocks['sblock'])
        for block in blocks:
            glVertex2f(block.inf.x, block.inf.y)
            glVertex2f(block.sup.x, block.inf.y)
            glVertex2f(block.sup.x, block.sup.y)
            glVertex2f(block.inf.x, block.sup.y)

        glEnd()

