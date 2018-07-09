

class Characters:
    def __init__(self):
        """
        Initializes different class parameters, to be added using the methods
        above. Is important to add the different characters in the correct
        order, because there are some characters whose initialization depends
        on other characters.
        """
        self.physics = None

        self.bombermen = []
        self.grid = None
        self.enemies = []
        self.bombs = []
        self.fires = []
        self.powerups = []
        self.dblocks = []
        self.exit = None

    def add_bomberman(self, bomberman):
        """
        Adds a bomberman of the list of bombermen.
        :param bomberman: Bomberman character of Bomberman type.
        :return:
        """
        self.bombermen.append(bomberman)

    def set_grid(self, grid):
        """
        Sets the grid of the game where the Bomberman and the other
        game characters will interact.
        :param grid: Grid from the class Grid containing a distribution
                     of blocks, used to represent the path that can be
                     used by the characters.
        :return:
        """
        self.grid = grid

    def set_physics(self, physics):
        """
        Sets the physics grid of the game.
        :param physics:
        :return:
        """
        self.physics = physics

    def add_enemy(self, enemy):
        """
        Adds an enemy to the list of enemies.
        :param enemy: Enemy from the class TO DO
        :return:
        """
        self.enemies.append(enemy)

    def add_bomb(self, bomb):
        """
        Adds a bomb to the list of bombs created by the Bomberman.
        :param bomb: Bomb from the class Bomb.
        :return:
        """
        self.bombs.append(bomb)

    def add_fires(self, fire):
        """
        Adds a fire created by a bomb in the list of bombs.
        :param fire: Fire from the class Fire.
        :return:
        """
        self.fires.append(fire)

    def add_powerup(self, powerup):
        """
        Adds a powerup behind a destructive block.
        :param powerup: Powerup from the class Powerup.
        :return:
        """
        self.powerups.append(powerup)

    def add_dblock(self, dblock):
        """
        Adds a destructive block to the dblocks, the list of destructive
        blocks
        :param dblock: Destructive Block from the DestructiveBlock class.
        :return:
        """
        self.dblocks.append(dblock)

    def add_exit(self, exit):
        """
        Adds an exit object to the set of characters.
        :param exit:
        :return:
        """
        self.exit = exit

    def update(self):
        """
        Update the different elements of the model. Is used by the view.
        :return:
        """
        s = self
        for bomberman in s.bombermen:
            bomberman.update()

        for enemy in s.enemies:
            enemy.update()

        for dblock in s.dblocks:
            dblock.update()

        for fire in s.fires:
            fire.update()

        for bomb in s.bombs:
            bomb.update()

        self.exit.update()