# Implementación testeada con:
#
# Python 3.5
# PyOpenGL 3.1.0
# PyGame 1.9.3
#####################################################################
import os
from cc3501utils.init import *
from cc3501utils.vector import Vector
from exit import Exit
from grid import Grid
from physics import Physics
from view import View
from characters import Characters
from bomberman import Bomberman
from powerup import PowerUp
from dblock import DBlock
from enemy import Enemy
#####################################################################

os.environ['SDL_VIDEO_CENTERED'] = '1'  # centrar pantalla


def main():
    rectlen = 50
    width = 15*rectlen
    height = 13*rectlen
    init(width, height, "Bomberman")
    view = View()
    clock = pygame.time.Clock()
    fps = 60
    pjs = Characters()
    physics = Physics(pjs, 15, 13, (1 << 11), width, height)
    pjs.set_physics(physics)

    grid = Grid(pjs)
    bomberman = Bomberman(pjs, fps, Vector(physics.len_blocks, physics.len_blocks))

    nofenemies = 5
    nofdblocks = 50
    nofpowerup = 3

    pjs.add_bomberman(bomberman)
    pjs.set_grid(grid)

    physics.find_available_blocks()
    for i in range(nofdblocks):
        pjs.dblocks.append(DBlock(pjs))

    for i in range(nofpowerup):
        pjs.add_powerup(PowerUp(pjs))

    for i in range(nofenemies):
        pjs.add_enemy(Enemy(pjs, fps))

    exit = Exit(pjs)
    pjs.add_exit(exit)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == QUIT:  # cerrar ventana
                run = False

        if not bomberman.is_dead():
            keys = pygame.key.get_pressed()
            if keys[K_RIGHT]:
                bomberman.move(Vector(1, 0))
            if keys[K_LEFT]:
                bomberman.move(Vector(-1, 0))
            if keys[K_UP]:
                bomberman.move(Vector(0, 1))
            if keys[K_DOWN]:
                bomberman.move(Vector(0, -1))
            if keys[K_SPACE]:
                bomberman.put_bomb()

        pjs.update()
        view.draw(pjs)
        pygame.display.flip()  # actualizar pantalla
        clock.tick(30)

    pygame.quit()


main()
