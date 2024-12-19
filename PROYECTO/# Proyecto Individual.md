# Proyecto Individual

Este documento describe un script en Python que utiliza las bibliotecas OpenGL y OpenCV para crear una escena en 2D donde se dibuja un octágono que se puede mover, escalar y rotar en función del movimiento detectado por la cámara. A continuación se detalla cada parte del código y su funcionamiento.

## Código

```python
import numpy as np
import cv2 as cv
from OpenGL.GL import *
from OpenGL.GLU import *
import glfw

# Variables globales
window_width, window_height = 800, 600
translation = [0, 0]  # Traslación inicial (x, y)
scale = 1.0  # Escalamiento inicial
rotation = 0.0  # Rotación inicial en el eje Z

sensitivity = 2.0  # Sensibilidad de movimiento
rotation_sensitivity = 5.0  # Sensibilidad de rotación

# Margen
margin_color = (0.0, 1.0, 0.0)  # Verde en OpenGL
margin_thickness = 0.9  # Margen en coordenadas normalizadas

def init_gl():
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, window_width / window_height, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

def draw_octagon():
    glBegin(GL_POLYGON)
    vertices = [
        (0.5, 0.0),
        (0.35, 0.35),
        (0.0, 0.5),
        (-0.35, 0.35),
        (-0.5, 0.0),
        (-0.35, -0.35),
        (0.0, -0.5),
        (0.35, -0.35)
    ]
    glColor3f(1.0, 0.0, 0.0)
    for vertex in vertices:
        glVertex2fv(vertex)
    glEnd()

def draw_margin():
    glColor3f(*margin_color)
    glBegin(GL_LINE_LOOP)
    vertices = [
        (margin_thickness, margin_thickness),
        (margin_thickness, -margin_thickness),
        (-margin_thickness, -margin_thickness),
        (-margin_thickness, margin_thickness)
    ]
    for vertex in vertices:
        glVertex2fv(vertex)
    glEnd()

def render():
    global translation, scale, rotation
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(translation[0], translation[1], -5)
    glScalef(scale, scale, scale)
    glRotatef(rotation, 0, 0, 1)  # Rotación en el eje Z
    draw_margin()  # Dibujar el margen
    draw_octagon()  # Dibujar el octágono
    glfw.swap_buffers(window)

def calculate_translation_and_rotation(mask, grid_points):
    global rotation
    # Calcular el centroide de los puntos tocados
    touched_points = []
    for point in grid_points:
        x, y = map(int, point.ravel())
        if mask[y, x] == 255:  # Punto tocado por color negro
            touched_points.append((x, y))

    if touched_points:
        cx, cy = np.mean(touched_points, axis=0)  # Centroide de los puntos tocados
        # Normalizar la traslación en relación al centro de la matriz
        tx = (cx - window_width / 2) / (window_width / 2) * sensitivity
        ty = -(cy - window_height / 2) / (window_height / 2) * sensitivity
        # Calcular rotación en función del movimiento horizontal
        rotation += -tx * rotation_sensitivity
        return [tx, ty]
    return [0, 0]

def calculate_scale(mask, grid_points):
    touched_points = 0
    for point in grid_points:
        x, y = map(int, point.ravel())
        if mask[y, x] == 255:  # Punto tocado por color negro
            touched_points += 1
    total_points = len(grid_points)
    return 1.0 + (touched_points / total_points) * 1.5  # Escala proporcional

def check_bounds():
    global translation
    # Verificar si la figura está fuera del margen
    if abs(translation[0]) > margin_thickness or abs(translation[1]) > margin_thickness:
        translation = [0, 0]  # Regresar al centro

def main():
    global window, translation, scale

    if not glfw.init():
        raise Exception("No se pudo inicializar GLFW")

    window = glfw.create_window(window_width, window_height, "Figura 2D con GLFW", None, None)
    if not window:
        glfw.terminate()
        raise Exception("No se pudo crear la ventana GLFW")

    glfw.make_context_current(window)
    init_gl()

    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("No se pudo acceder a la cámara")

    # Crear matriz de puntos fija
    grid_size = 20
    step = 20
    grid_points = np.array([(x, y) for y in range(100, 400, step) for x in range(200,