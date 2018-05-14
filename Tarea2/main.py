# Implementación testeada con:
## Python 3.5
## PyOpenGL 3.1.0
## PyGame 1.9.3
#####################################################################
import os
import random
from CC3501Utils import *
from grid import Grid
from vista import *
from bomberman import Bomberman
from destructiveblock import DestructiveBlock
#####################################################################

os.environ['SDL_VIDEO_CENTERED'] = '1'  # centrar pantalla

def main():
    ancho = 15*50
    alto = 650
    init(ancho, alto, "Ejemplo Aux")
    vista = Vista()
    clock = pygame.time.Clock()

    pjs = []
    walls = Grid(13, 15)
    bomberman = Bomberman(pjs, Vector(50, 50))
    destructiveblocks = 50
    powerups = 5

    pjs.append(walls)
    pjs.append(bomberman)
    for i in range(destructiveblocks):
        pjs.append(DestructiveBlock(pjs))

    bomberman.clear_radius(2)

    for i in range(powerups):
        pjs.append(PowerUp(pjs))
    
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == QUIT:  # cerrar ventana
                run = False
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
            
        vista.dibujar(pjs)
        pygame.display.flip()  # actualizar pantalla
        clock.tick(int(1000/60))  # ajusta a 30 fps

    pygame.quit()

main()