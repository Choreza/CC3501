from OpenGL.GL import *


class View:
    def draw(self, pjs):
        # limpia la pantalla
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        pjs.grid.draw()
        pjs.exit.draw()

        for fire in pjs.fires:
            fire.draw()

        for bomb in pjs.bombs:
            bomb.draw()

        for powerup in pjs.powerups:
            powerup.draw()

        for dblock in pjs.dblocks:
            dblock.draw()

        for bomberman in pjs.bombermen:
            bomberman.draw()

        for enemy in pjs.enemies:
            enemy.draw()

