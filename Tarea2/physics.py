from cc3501utils.vector import Vector
from rectangle import Rectangle


class Physics:
    def __init__(self, pjs, cols, rows, len_blocks, rwidth, rheight):
        """
        Builder of physics class, used to model a discrete grid that will
        be used to get the position of every element in the game at every
        frame. Receives the horizontal and vertical blocks number, and the
        blocks length. Calculates the height and width for the kodhcoreza_11
        nitializes the list of blocks.
        :param cols: Number of blocks horizontally.
        :param rows: Number of blocks vertically.
        :param len_blocks: Length for all blocks.
        """
        self.pjs = pjs
        self.cols = cols
        self.rows = rows
        self.len_blocks = len_blocks

        self.height = rows * len_blocks
        self.width = cols * len_blocks
        print('height and witdth', self.height, self.width)

        self.real_height = rheight
        self.real_width = rwidth

        self.blocks = dict()
        self.available_blocks = list()
        self.unavailable_blocks = list()

    def find_available_blocks(self):
        s = self
        length = self.len_blocks

        for i in range(0, s.cols):
            for j in range(0, s.rows):
                block = Rectangle(Vector(length * i, length * j), Vector(length * (i + 1), length * (j + 1)))
                if block not in self.unavailable_blocks:
                    self.available_blocks.append(block)

    def add_block(self, block, type):
        """
        Adds a block to list of the given type.
        :param block:
        :param type:
        :return:
        """
        if not (type in self.blocks):
            self.blocks[type] = list()
        self.blocks[type].append(block)
        self.unavailable_blocks.append(block)

    def is_valid_move(self, block, direction):
        """
        Verifies if the new position for the given block is valid
        according to the dimensions of the discrete grid.
        :param block:
        :param direction:
        :return:
        """
        block += direction
        hor_move = 0 <= block.inf.x and self.width > block.sup.x
        ver_move = 0 <= block.inf.y and self.height > block.sup.y
        return hor_move and ver_move

    def move_bomberman(self, bomberman, direction):
        if 'bomberman' in self.blocks:
            for i in range(len(self.blocks['bomberman'])):
                if self.blocks['bomberman'][i] == bomberman.rects[0]:
                    self.blocks['bomberman'][i] += direction
                    break
            bomberman.rects[0] += direction

    def can_move_bomberman(self, character, direction):
        """
        Checks if a block can directly move to te given direction, this method
        assumes that block object has a direction parameter.
        :param character:
        :param direction:
        :return:
        """
        s = self
        c = character
        d = direction
        cblock = c.rects[0]

        if 'bomb' in s.blocks:
            blocks = s.blocks['bomb']

            for block in blocks:
                if c.last_bomb:
                    # Checks if bomberman still over the last bomb, to pass over it.
                    if block == c.last_bomb.rects[0] and block.overlap(cblock + d * c.max_steps):
                        break

                    # If he isn't over, forget the last bomb.
                    if block == c.last_bomb.rects[0] and not(block.overlap(cblock + d * c.max_steps)):
                        c.last_bomb = None

                if block.overlap(cblock + d * c.max_steps):
                    return False

        blocks = s.blocks['dblock']
        for block in blocks:
            if block.overlap(cblock + d * c.max_steps):
                return False

        # If a block from blocks overlaps c's block in the new position
        # can't directly move, then return False
        blocks = s.blocks['sblock']
        for block in blocks:
            if block.overlap(cblock + d * c.max_steps):
                return False
        return True

    def can_move_enemy(self, character, direction):
        """
                Checks if a block can directly move to te given direction, this method
                assumes that block object has a direction parameter.
                :param character:
                :param direction:
                :return:
                """
        s = self
        c = character
        d = direction
        cblock = c.rects[0]

        if 'bomb' in s.blocks:
            blocks = s.blocks['bomb']

            for block in blocks:
                if block.overlap(cblock + d * c.max_steps):
                    return False

        blocks = s.blocks['dblock']
        for block in blocks:
            if block.overlap(cblock + d * c.max_steps):
                return False

        blocks = s.blocks['sblock']
        for block in blocks:
            if block.overlap(cblock + d * c.max_steps):
                return False

        for enemy in s.pjs.enemies:
            if enemy.rects[0] != cblock and enemy.rects[0].overlap(cblock + d * c.max_steps):
                return False

        return True

    def scl_coord_res(self, coord):
        real_x = self.real_width
        real_y = self.real_height

        discrete_x = self.width
        discrete_y = self.height

        xf = float(real_x) / discrete_x
        yf = float(real_y) / discrete_y

        return Vector(coord.x * xf, coord.y * yf)

    def scl_block_res(self, blocks):
        real_x = self.real_width
        real_y = self.real_height

        discrete_x = self.width
        discrete_y = self.height

        xf = float(real_x) / discrete_x
        yf = float(real_y) / discrete_y
        real_blocks = list()
        for block in blocks:
            b = Rectangle(Vector(block.inf.x * xf, block.inf.y * yf),
                          Vector(block.sup.x * xf, block.sup.y * yf))
            real_blocks.append(b)
        return real_blocks
