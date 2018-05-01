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

    pjs = []
    walls = Grid(13, 15)
    bomberman = Bomberman(walls, Vector(50, 50))
    pjs.append(walls)
    pjs.append(bomberman)

    run = True
    while run:

        for event in pygame.event.get():
            if event.type == QUIT:  # cerrar ventana
                run = False

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    pass
                if event.key == K_RIGHT:
                    bomberman.move(50, 0)
                if event.key == K_LEFT:
                    bomberman.move(-50, 0)
                if event.key == K_UP:
                    bomberman.move(0, 50)
                if event.key == K_DOWN:
                    bomberman.move(0, -50)

        vista.dibujar(pjs)

    
        pygame.display.flip()  # actualizar pantalla
        pygame.time.wait(int(1000 / 30))  # ajusta a 30 fps

    pygame.quit()

main()