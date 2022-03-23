#pip install pyopengl
#pip install glfw
from cmath import cos, pi, sin
import dis
from scipy import rand
from asteroide import asteroide
from OpenGL.GL import *
from glew_wish import *
import glfw
import math
import random
from Nave import *

window = None
nave = Nave()
asteroides = []
tiempo_anterior = 0.0 

def actualizar():
    global tiempo_anterior
    global window

    tiempo_actual = glfw.get_time()
    tiempo_delta = tiempo_actual - tiempo_anterior
   
    nave.actualizar(window, tiempo_delta)
    for asteroide in asteroides:
        if asteroide.vivo:
            asteroide.actualizar(tiempo_delta)
            if asteroide.colisionando(nave):
                nave.herido = True
            for bala in nave.balas:
                if bala.disparando:
                    if asteroide.colisionando(bala):
                        bala.disparando = False
                        asteroide.vivo = False
    tiempo_anterior = tiempo_actual
    
def colisionando():
    colisionando = False
    return colisionando

def draw():
    for asteroide in asteroides:
        asteroide.dibujar()
    #draw_bala()
    nave.dibujar()

def inicializar_asteroides():
    for i in range(10):
        posicion_x = (random.random() * 2) - 1 
        posicion_y = (random.random() * 2) - 1 
        direccion = random.random() * 360
        velocidad = (random.random() * 0.5) + 0.6
        asteroides.append(asteroide(posicion_x, posicion_y, direccion, velocidad))

def main():
    global window
    width = 700
    height = 700
    if not glfw.init():
        return

    window = glfw.create_window(width, height, "Mi ventana", None, None)

    glfw.window_hint(glfw.SAMPLES, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glewExperimental = True

    if glewInit() != GLEW_OK:
        print("No se pudo inicializar GLEW")
        return

    version = glGetString(GL_VERSION)
    print(version)

    inicializar_asteroides()

    while not glfw.window_should_close(window):
        glClearColor(0.7,0.7,0.7,1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        actualizar()
        draw()
        glfw.poll_events()
        glfw.swap_buffers(window)

    glfw.destroy_window(window)
    glfw.terminate()

if __name__ == "__main__":
    main()