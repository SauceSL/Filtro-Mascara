import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt
import sys
import math
import cv2
import numpy as np

# Variables globales para el movimiento de la cámara
camera_x = 0
camera_y = 0
window = None

def init():
    """Configuración inicial de OpenGL"""
    glClearColor(0.5, 0.8, 1.0, 1.0)  # Fondo azul cielo
    glEnable(GL_DEPTH_TEST)           # Activar prueba de profundidad

    # Configuración de la perspectiva
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1.0, 0.1, 100.0)  # Campo de visión más amplio
    glMatrixMode(GL_MODELVIEW)

def draw_cube():
    """Dibuja el cubo (base de la casa)"""
    glBegin(GL_QUADS)
    glColor3f(0.8, 0.5, 0.2)  # Marrón para todas las caras

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

def draw_roof():
    """Dibuja el techo (pirámide)"""
    glBegin(GL_TRIANGLES)
    glColor3f(0.9, 0.1, 0.1)  # Rojo brillante

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
    
def draw_circle(radius, segments):
    """Dibuja un círculo en el plano XZ"""
    glBegin(GL_LINE_LOOP)
    glColor3f(0.0, 1.0, 0.0)  # Gris para el círculo
    for i in range(segments):
        theta = 2.0 * math.pi * float(i) / float(segments)
        x = radius * math.cos(theta)
        z = radius * math.sin(theta)
        glVertex3f(x, 0.01, z)
    glEnd()

def draw_house():
    """Dibuja una casa (base + techo)"""
    draw_cube()  # Base de la casa
    draw_roof()  # Techo

def draw_sphere(x, y, z, radius, slices, stacks, color):
    """Dibuja una esfera manualmente."""
    glColor3f(*color)
    glPushMatrix()
    glTranslatef(x, y, z)
    for i in range(stacks):
        lat0 = math.pi * (-0.5 + float(i) / stacks)
        z0 = radius * math.sin(lat0)
        zr0 = radius * math.cos(lat0)
        lat1 = math.pi * (-0.5 + float(i + 1) / stacks)
        z1 = radius * math.sin(lat1)
        zr1 = radius * math.cos(lat1)
        glBegin(GL_QUAD_STRIP)
        for j in range(slices + 1):
            lng = 2 * math.pi * float(j) / slices
            x = math.cos(lng)
            y = math.sin(lng)
            glNormal3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr0, y * zr0, z0)
            glNormal3f(x * zr1, y * zr1, z1)
            glVertex3f(x * zr1, y * zr1, z1)
        glEnd()
    glPopMatrix()

def draw_bush():
    """Dibuja un arbusto compuesto por varias esferas."""
    spheres = [
        (0, 0, 0, 1),      # Esfera central
        (-1, 1, 0, 0.8),   # Esfera izquierda
        (1, 1, 0, 0.8),    # Esfera derecha
        (0, 1.5, 0, 0.6),  # Esfera superior
        (0, -1, 0, 0.8)    # Esfera inferior
    ]
    for x, y, z, radius in spheres:
        # Dibujar borde oscuro
        draw_sphere(x, y, z, radius + 0.05, 32, 16, (0.0, 0.4, 0.0))  # Verde más oscuro
        # Dibujar esfera principal
        draw_sphere(x, y, z, radius, 32, 16, (0.0, 0.6, 0.0))  # Verde normal

def draw_cylinder(radius, height, slices):
    for i in range(slices):
        angle = 2 * math.pi * i / slices
        next_angle = 2 * math.pi * (i + 1) / slices
        # Base inferior
        glBegin(GL_TRIANGLES)
        glVertex3f(0, 0, 0)
        glVertex3f(radius * math.cos(angle), radius * math.sin(angle), 0)
        glVertex3f(radius * math.cos(next_angle), radius * math.sin(next_angle), 0)
        glEnd()
        # Paredes del cilindro
        glBegin(GL_QUADS)
        glVertex3f(radius * math.cos(angle), radius * math.sin(angle), 0)
        glVertex3f(radius * math.cos(next_angle), radius * math.sin(next_angle), 0)
        glVertex3f(radius * math.cos(next_angle), radius * math.sin(next_angle), height)
        glVertex3f(radius * math.cos(angle), radius * math.sin(angle), height)
        glEnd()
    # Base superior
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0, 0, height)
    for i in range(slices + 1):
        angle = 2 * math.pi * i / slices
        glVertex3f(radius * math.cos(angle), radius * math.sin(angle), height)
    glEnd()

def draw_streetlamp():
    """Dibuja una farola"""
    # Dibujar base
    glPushMatrix()
    glColor3f(0.3, 0.3, 0.3)  # Gris oscuro
    draw_cylinder(0.5, 0.2, 32)
    glPopMatrix()
    # Dibujar poste
    glPushMatrix()
    glColor3f(0.1, 0.1, 0.5)  # Azul oscuro
    glTranslatef(0.0, 0.0, 0.2)
    draw_cylinder(0.1, 4, 32)
    glPopMatrix()
    # Dibujar lámpara (esfera)
    glPushMatrix()
    glColor3f(1.0, 1.0, 0.5)  # Amarillo claro
    glTranslatef(0.0, 0.0, 4.2)
    draw_sphere(0.3, 32, 16)
    glPopMatrix()

def draw_scene():
    """Dibuja toda la escena con casas en círculo, arbustos en el centro y farolas"""
    global camera_x, camera_y

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Configuración de la cámara
    gluLookAt(20 + camera_x, 15 + camera_y, 25,  # Posición de la cámara
              0, 0, 0,    # Punto al que mira
              0, 1, 0)    # Vector hacia arriba

    # Dibujar el suelo
    draw_ground()

    # Dibujar el círculo al final de la calle
    draw_circle(10, 50)

    # Dibujar las casas en posiciones circulares
    num_houses = 8
    radius = 10
    for i in range(num_houses):
        angle = 2 * math.pi * i / num_houses
        x = radius * math.cos(angle)
        z = radius * math.sin(angle)
        glPushMatrix()
        glTranslatef(x, 0, z)  # Mover la casa a la posición actual
        glRotatef(math.degrees(angle), 0, 1, 0)  # Rotar la casa para que mire hacia afuera
        draw_house()        # Dibujar la casa
        glPopMatrix()

    # Dibujar arbustos en el centro del círculo
    glPushMatrix()
    glTranslatef(0, 0, 0)  # Centrar los arbustos
    draw_bush()
    glPopMatrix()

    # Dibujar farolas en cuatro puntos diferentes
    streetlamp_positions = [
        (5, 0, 5),
        (-5, 0, 5),
        (5, 0, -5),
        (-5, 0, -5)
    ]
    for pos in streetlamp_positions:
        glPushMatrix()
        glTranslatef(*pos)
        draw_streetlamp()
        glPopMatrix()

    glfw.swap_buffers(window)

def process_optical_flow(cap):
    global camera_x, camera_y

    ret, frame1 = cap.read()
    prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    hsv_mask = np.zeros_like(frame1)
    hsv_mask[..., 1] = 255

    while True:
        ret, frame2 = cap.read()
        next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        hsv_mask[..., 0] = ang * 180 / np.pi / 2
        hsv_mask[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
        rgb_representation = cv2.cvtColor(hsv_mask, cv2.COLOR_HSV2BGR)

        # Calcular el movimiento promedio
        avg_flow = np.mean(flow, axis=(0, 1))
        camera_x += avg_flow[0] * 0.1
        camera_y -= avg_flow[1] * 0.1

        cv2.imshow('Optical Flow', rgb_representation)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        prvs = next

    cap.release()
    cv2.destroyAllWindows()

def main():
    global window

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()
    
    # Crear ventana de GLFW
    width, height = 800, 600
    window = glfw.create_window(width, height, "Escena con casas en círculo, arbustos y farolas", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    # Inicializar la captura de video
    cap = cv2.VideoCapture(0)

    # Crear un hilo para el flujo óptico
    import threading
    optical_flow_thread = threading.Thread(target=process_optical_flow, args=(cap,))
    optical_flow_thread.start()

    # Bucle principal
    while not glfw.window_should_close(window):
        draw_scene()
        glfw.poll_events()

    glfw.terminate()
    cap.release()
    optical_flow_thread.join()

if __name__ == "__main__":
    main()