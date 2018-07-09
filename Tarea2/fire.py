from cc3501utils.vector import Vector
from cc3501utils.figure import Figure
from OpenGL.GL import *
from rectangle import Rectangle


class Fire(Figure):
    def __init__(self, pjs, radius, fps, pos, rgb=(1.0, 1.0, 1.0)):
        """
        Fire builder.
        :param pjs: The list of characters.
        :param radius: Integer representing the radius of the bomb.
        :param fps: Integer representing the number of fps, used to calculate the time to explode.
        :param pos: Vector representative of the position in the screen.
        :param rgb: Not used. Required for the superclass builder.
        """
        self.pjs = pjs
        self.physics = pjs.physics
        self.pos = pos
        self.radius = radius

        self.lifetime = 0
        self.timeout = 2*fps

        self.stype = 'fire'
        self.rpos = pos
        self.rects = list()
        self.pos = self.physics.scl_coord_res(self.rpos)
        self.init_blocks()
        super().__init__(self.pos, rgb)

    def init_blocks(self):
        """
        Initializes the blocks at the discrete grid of blocks, representatives of the character.
        :return:
        """
        s = self

        x = s.rpos.x
        y = s.rpos.y

        length = s.physics.len_blocks
        block = Rectangle(s.rpos, s.rpos + Vector(length, length))

        s.physics.add_block(block, s.stype)
        s.rects.append(block)

        directions = list()
        directions.append([])
        for i in range(1, s.radius):
            directions[0].append(Vector(x - i * length, y))

        directions.append([])
        for i in range(1, s.radius):
            directions[1].append(Vector(x + i * length, y))

        directions.append([])
        for i in range(1, s.radius):
            directions[2].append(Vector(x, y - i * length))

        directions.append([])
        for i in range(1, s.radius):
            directions[3].append(Vector(x, y + i * length))

        for direction in directions:
            overlap = False

            for p in direction:
                rect = Rectangle(p, p + Vector(length, length))

                # Checks if a bomb overlap in this direction.
                bombs = s.pjs.bombs
                for bomb in bombs:
                    block = bomb.rects[0]

                    # If overlaps, makes the bomb explode.
                    if block.overlap(rect):
                        bomb.explode()
                        overlap = True
                        break

                for dblock in s.pjs.dblocks:
                    if dblock.rects[0].overlap(rect):
                        overlap = True
                        dblock.explode(s)

                if not overlap:
                    # Checks if the fire block to insert overlaps the grid.
                    blocks = s.physics.blocks['sblock']
                    for block in blocks:
                        if block.overlap(rect):
                            overlap = True
                            break

                if not overlap:
                    s.rects.append(rect)
                    s.physics.add_block(rect, s.stype)

                else:
                    break

    def figure(self):
        """
        Draws the character in the screen.
        :return:
        """
        top = 0
        for block in self.rects:
            if block.inf.y > self.rects[0].inf.y:
                top += 1

        bot = 0
        for block in self.rects:
            if block.inf.y < self.rects[0].inf.y:
                bot += 1

        left = 0
        for block in self.rects:
            if block.inf.x < self.rects[0].inf.x:
                left += 1

        right = 0
        for block in self.rects:
            if block.inf.x > self.rects[0].inf.x:
                right += 1

        lower = self.physics.scl_coord_res(self.rects[0].inf)
        upper = self.physics.scl_coord_res(self.rects[0].sup)
        upper += lower * -1
        lower += lower * -1

        glBegin(GL_QUADS)
        glColor3f(255 / 255, 69.0 / 255, 0.0 / 255)
        glVertex2f(upper.x, upper.y)
        glVertex2f(upper.x, lower.y)
        glVertex2f(lower.x, lower.y)
        glVertex2f(lower.x, upper.y)

        glColor3f(255 / 255, 165.0 / 255, 0.0 / 255)
        glVertex2f(upper.x, 0.75 * upper.y)
        glVertex2f(upper.x, 0.25 * upper.y)
        glVertex2f(lower.x, 0.25 * upper.y)
        glVertex2f(lower.x, 0.75 * upper.y)

        glVertex2f(upper.x * 0.75, upper.y)
        glVertex2f(upper.x * 0.75, lower.y)
        glVertex2f(upper.x * 0.25, lower.y)
        glVertex2f(upper.x * 0.25, upper.y)

        glEnd()

        glBegin(GL_TRIANGLES)
        glColor3f(255 / 255, 165.0 / 255, 0.0 / 255)
        glVertex2f(upper.x * 0.75, upper.y * 0.75)
        glVertex2f(upper.x * 0.75, upper.y)
        glVertex2f(upper.x, 0.75 * upper.y)

        glVertex2f(upper.x * 0.75, upper.y * 0.25)
        glVertex2f(upper.x, upper.y * 0.25)
        glVertex2f(upper.x * 0.75, lower.x)

        glVertex2f(upper.x * 0.25, upper.y)
        glVertex2f(upper.x * 0.25, upper.y * 0.75)
        glVertex2f(lower.x, upper.y * 0.75)

        glVertex2f(upper.x * 0.25, upper.y * 0.25)
        glVertex2f(upper.x * 0.25, lower.y)
        glVertex2f(lower.x, upper.y * 0.25)
        glEnd()

        if top:
            glBegin(GL_TRIANGLES)
            glColor3f(255 / 255, 69.0 / 255, 0.0 / 255)
            glVertex2f(upper.x, upper.y)
            glVertex2f(upper.x / 2, upper.y + top * upper.y)
            glVertex2f(lower.x, upper.y)
            glEnd()

            glBegin(GL_TRIANGLES)
            glColor3f(255 / 255, 165.0 / 255, 0.0 / 255)
            glVertex2f(0.75 * upper.x, upper.y)
            glVertex2f(upper.x / 2, upper.y + top * upper.y * 0.8)
            glVertex2f(0.25 * upper.x, upper.y)
            glEnd()

        if bot:
            glBegin(GL_TRIANGLES)
            glColor3f(255 / 255, 69.0 / 255, 0.0 / 255)
            glVertex2f(upper.x, lower.y)
            glVertex2f(upper.x / 2, -bot * upper.y)
            glVertex2f(lower.x, lower.y)
            glEnd()

            glBegin(GL_TRIANGLES)
            glColor3f(255 / 255, 165.0 / 255, 0.0 / 255)
            glVertex2f(0.75 * upper.x, lower.y)
            glVertex2f(upper.x / 2, -bot * upper.y * 0.8)
            glVertex2f(0.25 * upper.x, lower.y)
            glEnd()

        if right:
            glBegin(GL_TRIANGLES)
            glColor3f(255 / 255, 69.0 / 255, 0.0 / 255)
            glVertex2f(upper.x, upper.y)
            glVertex2f(upper.x + right * upper.x, upper.y / 2)
            glVertex2f(upper.x, lower.y)
            glEnd()

            glBegin(GL_TRIANGLES)
            glColor3f(255 / 255, 165.0 / 255, 0.0 / 255)
            glVertex2f(upper.x, 0.75 * upper.y)
            glVertex2f(upper.x + right * upper.x * 0.8, upper.y / 2)
            glVertex2f(upper.x, 0.25 * upper.y)
            glEnd()

        if left:
            glBegin(GL_TRIANGLES)
            glColor3f(255 / 255, 69.0 / 255, 0.0 / 255)
            glVertex2f(lower.x, upper.y)
            glVertex2f(-left * upper.x, upper.y / 2)
            glVertex2f(lower.x, lower.y)
            glEnd()

            glBegin(GL_TRIANGLES)
            glColor3f(255 / 255, 165.0 / 255, 0.0 / 255)
            glVertex2f(lower.x, upper.y * 0.75)
            glVertex2f(-left * upper.x * 0.8, upper.y / 2)
            glVertex2f(lower.x, upper.y * 0.25)
            glEnd()

    def extinguish(self):
        """
        Removes this fire and all the interactions from the screen.
        :return:
        """
        s = self
        for b in s.rects:
            s.physics.blocks[s.stype].remove(b)
        s.pjs.fires.remove(s)

    def update(self):
        """
        Checks if it's time to extinguish.
        :return:
        """
        self.lifetime += 1
        if self.lifetime > self.timeout:
            self.extinguish()
