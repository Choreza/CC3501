#####################################################################
# Mauricio Araneda H.
# CC3501
#####################################################################

# Ejemplo.py
# ---------------
# Ejemplo para aux
# ---------------

# Implementación testeada con:
## Python 3.5
## PyOpenGL 3.1.0
## PyGame 1.9.3
#####################################################################
import os
import random
from CC3501Utils import *
from Grid import *
from vista import *
from Bomberman import *
#from pickle import *
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
    bomberman = Bomberman(walls, clock, Vector(50, 50))
    pjs.append(walls)
    pjs.append(bomberman)
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == QUIT:  # cerrar ventana
                run = False

        keys = pygame.key.get_pressed()
        if keys[K_RIGHT]:
            bomberman.move(Vector(50, 0))
        if keys[K_LEFT]:
            bomberman.move(Vector(-50, 0))
        if keys[K_UP]:
            bomberman.move(Vector(0, 50))
        if keys[K_DOWN]:
            bomberman.move(Vector(0, -50))
        if keys[K_SPACE]:
            bomberman.put_bomb(pjs)
        vista.dibujar(pjs)
        pygame.display.flip()  # actualizar pantalla
        clock.tick(int(1000/30))  # ajusta a 30 fps

    pygame.quit()

main()