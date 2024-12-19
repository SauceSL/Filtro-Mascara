import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluNewQuadric, gluSphere, gluPerspective, gluCylinder, gluLookAt
import sys
import math

# Variables globales
window = None
jump_offset = 0.0       # Para el movimiento de salto vertical
jump_speed = 0.000005       # Velocidad del salto
jump_direction = 0.0001      # Dirección del salto (1 hacia arriba, -1 hacia abajo)
rotation_angle = 0.0    # Ángulo de rotación del muñeco de nieve

def init():
    glClearColor(0.5, 0.7, 1.0, 1.0)  # Fondo de cielo
    glEnable(GL_DEPTH_TEST)
    # Configuración de la perspectiva
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 1.0, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

def draw_sphere(radius=1, x=0, y=0, z=0):
    glPushMatrix()
    glTranslatef(x, y, z)
    quadric = gluNewQuadric()
    gluSphere(quadric, radius, 32, 32)
    glPopMatrix()

def draw_cone(base=0.1, height=0.5, x=0, y=0, z=0):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(-90, 1, 0, 0)  # Orientar el cono hacia adelante
    quadric = gluNewQuadric()
    gluCylinder(quadric, base, 0, height, 32, 32)
    glPopMatrix()

def draw_snowman():
    global jump_offset, rotation_angle
    glPushMatrix()
    glTranslatef(0.0 + jump_offset, 0, 0)  # Posición del muñeco de nieve y altura
    # Cuerpo
    glColor3f(1, 1, 1)
    draw_sphere(1.0, 0, 0, 0)     # Base
    draw_sphere(0.75, 0, 1.2, 0)  # Cuerpo medio
    draw_sphere(0.5, 0, 2.2, 0)   # Cabeza
    # Ojos
    glColor3f(0, 0, 0)
    draw_sphere(0.05, -0.15, 2.3, 0.4)  # Ojo izquierdo
    draw_sphere(0.05, 0.15, 2.3, 0.4)   # Ojo derecho
    # Nariz (cono)
    glColor3f(1, 0.5, 0)  # Color naranja
    draw_cone(0.05, 0.2, 0, 2.2, 0.5)  # Nariz
    glPopMatrix()

def draw_cube():
    """Dibuja el cubo (base de la casa)"""
    glBegin(GL_QUADS)
    glColor3f(0.9, 0.7, 0.5)  # Marrón para todas las caras
    # Frente
    glVertex3f(-1, 0, 1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)
    # Atrás
    glVertex3f(-1, 0, -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(-1, 1, -1)
    # Izquierda
    glVertex3f(-1, 0, -1)
    glVertex3f(-1, 0, 1)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, 1, -1)
    # Derecha
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(1, 1, -1)
    # Arriba
    glColor3f(0.9, 0.6, 0.3)  # Color diferente para el techo
    glVertex3f(-1, 1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)
    # Abajo
    glColor3f(0.6, 0.4, 0.2)  # Suelo más oscuro
    glVertex3f(-1, 0, -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 1)
    glVertex3f(-1, 0, 1)
    glEnd()
    
def draw_cube2():
    """Dibuja el cubo (base de la casa)"""
    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 1.0)  # Marrón para todas las caras
    # Frente
    glVertex3f(-3, 0, 3)
    glVertex3f(3, 0, 3)
    glVertex3f(3, 3, 3)
    glVertex3f(-3, 3, 3)
    # Atrás
    glVertex3f(-3, 0, -3)
    glVertex3f(3, 0, -3)
    glVertex3f(3, 3, -3)
    glVertex3f(-3, 3, -3)
    # Izquierda
    glVertex3f(-3, 0, -3)
    glVertex3f(-3, 0, 3)
    glVertex3f(-3, 3, 3)
    glVertex3f(-3, 3, -3)
    # Derecha
    glVertex3f(3, 0, -3)
    glVertex3f(3, 0, 3)
    glVertex3f(3, 3, 3)
    glVertex3f(3, 3, -3)
    # Arriba
    glColor3f(0.2, 0.2, 0.2)  # Color diferente para el techo
    glVertex3f(-3, 3, -3)
    glVertex3f(3, 3, -3)
    glVertex3f(3, 3, 3)
    glVertex3f(-3, 3, 3)
    # Abajo
    glColor3f(0.6, 0.4, 0.2)  # Suelo más oscuro
    glVertex3f(-3, 0, -3)
    glVertex3f(3, 0, -3)
    glVertex3f(3, 0, 3)
    glVertex3f(-3, 0, 3)
    glEnd()

def draw_roof():
    """Dibuja el techo (pirámide)"""
    glBegin(GL_TRIANGLES)
    glColor3f(0.65, 0.45, 0.25)  # Rojo brillante
    # Frente
    glVertex3f(-1, 1, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(0, 2, 0)
    # Atrás
    glVertex3f(-1, 1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(0, 2, 0)
    # Izquierda
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, 1, 1)
    glVertex3f(0, 2, 0)
    # Derecha
    glVertex3f(1, 1, -1)
    glVertex3f(1, 1, 1)
    glVertex3f(0, 2, 0)
    glEnd()
    
def draw_roof2():
    """Dibuja el techo (pirámide) adaptado al tamaño del cubo grande."""
    glBegin(GL_TRIANGLES)
    glColor3f(0.7, 0.5, 0.3)  # Azul para el techo
    # Frente
    glVertex3f(-3, 3, 3)
    glVertex3f(3, 3, 3)
    glVertex3f(0, 6, 0)
    # Atrás
    glVertex3f(-3, 3, -3)
    glVertex3f(3, 3, -3)
    glVertex3f(0, 6, 0)
    # Izquierda
    glVertex3f(-3, 3, -3)
    glVertex3f(-3, 3, 3)
    glVertex3f(0, 6, 0)
    # Derecha
    glVertex3f(3, 3, -3)
    glVertex3f(3, 3, 3)
    glVertex3f(0, 6, 0)
    glEnd()


def draw_ground():
    """Dibuja un plano para representar el suelo o calle"""
    glBegin(GL_QUADS)
    glColor3f(0.3, 0.3, 0.3)  # Gris oscuro para la calle
    # Coordenadas del plano
    glVertex3f(-20, 0, 20)
    glVertex3f(20, 0, 20)
    glVertex3f(20, 0, -20)
    glVertex3f(-20, 0, -20)
    glEnd()

def draw_ground2():
    """Dibuja un plano para representar el suelo o calle"""
    glBegin(GL_QUADS)
    glColor3f(0.5, 0.5, 0.5)  # Gris oscuro para la calle
    # Coordenadas del plano
    glVertex3f(-7, 0.01, 2)
    glVertex3f(7, 0.01, 2)
    glVertex3f(7, 0.01, -2)
    glVertex3f(-7, 0.01, -2)
    glEnd()

def draw_house():
    """Dibuja una casa (base + techo)"""
    draw_cube()  # Base de la casa
    draw_roof()  # Techo
    
def draw_house2():
    """Dibuja una casa (base + techo)"""
    draw_cube2()  # Base de la casa
    draw_roof2()  # Techo
    

def draw_scene():
    """Dibuja toda la escena con casas y un muñeco de nieve"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    # Configuración de la cámara
    gluLookAt(10, 8, 15,  # Posición de la cámara
              0, 0, 0,    # Punto al que mira
              0, 1, 0)    # Vector hacia arriba
    # Dibujar el suelo
    draw_ground()
    draw_ground2()
    # Dibujar las casas en diferentes posiciones
    positions = [
        (0, 0, -5),  # Casa 0
        (0, 0, 5),  # Casa 0.1
        (-5, 0, -5),  # Casa 1
        (5, 0, -5),   # Casa 2
        (-5, 0, 5),   # Casa 3
        (5, 0, 5)     # Casa 4
    ]
    for pos in positions:
        glPushMatrix()
        glTranslatef(*pos)  # Mover la casa a la posición actual
        draw_house()        # Dibujar la casa
        glPopMatrix()
    
    # Dibujar el muñeco de nieve al lado de una casa
    glPushMatrix()
    glTranslatef(2, 0, -5)  # Posición del muñeco de nieve al lado de una casa
    draw_snowman()
    glPopMatrix()
    #Edificio
    glPushMatrix()
    glTranslatef(-10, 0, 0)  
    draw_cube2()
    draw_roof2()
    glPopMatrix()

    glfw.swap_buffers(window)

def update_motion():
    global jump_offset, jump_direction, rotation_angle
    # Actualizar el movimiento de salto
    jump_offset += jump_speed * jump_direction
    if jump_offset > 1:        # Limite superior del salto
        jump_direction = -1      # Cambiar dirección hacia abajo
    elif jump_offset < 0.0:      # Limite inferior del salto
        jump_direction = 1       # Cambiar dirección hacia arriba

def main():
    global window
    # Inicializar GLFW
    if not glfw.init():
        sys.exit()
   
    # Crear ventana de GLFW
    width, height = 800, 600
    window = glfw.create_window(width, height, "Escena con Casas y Muñeco de Nieve", None, None)
    if not window:
        glfw.terminate()
        sys.exit()
    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()
    # Bucle principal
    while not glfw.window_should_close(window):
        draw_scene()
        update_motion()  # Actualizar el movimiento en cada cuadro
        glfw.poll_events()
    glfw.terminate()

if __name__ == "__main__":
    main()