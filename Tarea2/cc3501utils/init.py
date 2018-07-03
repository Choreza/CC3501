import pygame
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *


# funcion para inicializar pygame y opengl en 2D
def init(ancho, alto, titulo):
    # inicializar pygame
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_mode((ancho, alto), OPENGL | DOUBLEBUF)
    pygame.display.set_caption(titulo)

    # inicializar opengl
    glViewport(0, 0, ancho, alto)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, ancho, 0.0, alto)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # definir variables de opengl
    glClearColor(46/255.0, 139/255.0, 47/255.0, 255.0)  # color del fondo
    glShadeModel(GL_SMOOTH)
    glClearDepth(1.0)
    # glDisable(GL_DEPTH_TEST)
    return
