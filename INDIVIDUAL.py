import cv2
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys

# Variables globales
window = None
angle_x = 0  # Ángulo de rotación del cubo en el eje X
angle_y = 0  # Ángulo de rotación del cubo en el eje Y
x_opengl = 0.0
y_opengl = 0.0
scale = 0.1
prev_x = 0.0
prev_y = 0.0

# Capturar video desde la cámara
video = cv2.VideoCapture(0)

def init():
    # Configuración inicial de OpenGL
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Color de fondo
    glEnable(GL_DEPTH_TEST)  # Activar prueba de profundidad para 3D

    # Configuración de proyección
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0, 1.0, 50.0)

    # Cambiar a la matriz de modelo para los objetos
    glMatrixMode(GL_MODELVIEW)

def draw_cube(x, y, scale):
    global angle_x, angle_y
    glPushMatrix()
    glTranslatef(x, y, -5.0)  # Posición basada en los movimientos
    glScalef(scale, scale, scale)  # Escalar el cubo en función de la distancia
    glRotatef(angle_x, 1, 0, 0)  # Rotar el cubo en el eje X
    glRotatef(angle_y, 0, 1, 0)  # Rotar el cubo en el eje Y

    glBegin(GL_QUADS)

    glColor3f(1.0, 0.0, 0.0)  # Rojo
    glVertex3f(1, 1, -1)
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, 1, 1)
    glVertex3f(1, 1, 1)

    glColor3f(0.0, 1.0, 0.0)  # Verde
    glVertex3f(1, -1, 1)
    glVertex3f(-1, -1, 1)
    glVertex3f(-1, -1, -1)
    glVertex3f(1, -1, -1)

    glColor3f(0.0, 0.0, 1.0)  # Azul
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, -1, 1)
    glVertex3f(1, -1, 1)

    glColor3f(1.0, 1.0, 0.0)  # Amarillo
    glVertex3f(1, -1, -1)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, 1, -1)
    glVertex3f(1, 1, -1)

    glColor3f(1.0, 0.0, 1.0)  # Magenta
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, -1, 1)

    glColor3f(0.0, 1.0, 1.0)  # Cyan
    glVertex3f(1, 1, -1)
    glVertex3f(1, 1, 1)
    glVertex3f(1, -1, 1)
    glVertex3f(1, -1, -1)

    glEnd()
    glPopMatrix()

def process_frame():
    global x_opengl, y_opengl, scale, prev_x, prev_y, angle_x, angle_y

    ret, frame = video.read()
    if not ret:
        return

    # Convertir el frame a escala de grises
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Aplicar desenfoque para suavizar
    frame_blur = cv2.GaussianBlur(frame_gray, (15, 15), 0)

    # Detectar los contornos
    _, thresh = cv2.threshold(frame_blur, 60, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Encontrar el contorno más grande
        max_contour = max(contours, key=cv2.contourArea)

        # Calcular el rectángulo delimitador
        x, y, w, h = cv2.boundingRect(max_contour)

        # Convertir coordenadas a OpenGL
        new_x_opengl = (x + w / 2) / frame.shape[1] * 2 - 1
        new_y_opengl = -(y + h / 2) / frame.shape[0] * 2 + 1

        # Ajustar escala basada en el tamaño del rectángulo
        scale = w / 200.0

        # Calcular la diferencia de movimiento
        dx = new_x_opengl - prev_x
        dy = new_y_opengl - prev_y

        # Actualizar ángulos de rotación basados en el movimiento
        angle_x += dy * 180  # Ajustar el factor de multiplicación según sea necesario
        angle_y += dx * 180  # Ajustar el factor de multiplicación según sea necesario

        # Actualizar las posiciones previas
        prev_x = new_x_opengl
        prev_y = new_y_opengl

        # Actualizar las posiciones actuales
        x_opengl = new_x_opengl
        y_opengl = new_y_opengl

def main():
    global window

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()

    # Crear ventana de GLFW
    width, height = 640, 480
    window = glfw.create_window(width, height, "Cubo 3D con Control por Mano", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    # Configurar el contexto de OpenGL en la ventana
    glfw.make_context_current(window)

    # Configuración de viewport y OpenGL
    glViewport(0, 0, width, height)
    init()

    # Bucle principal
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Limpiar pantalla y buffer de profundidad
        glLoadIdentity()

        # Procesar el frame para actualizar la posición y escala
        process_frame()

        # Dibujar el cubo
        draw_cube(x_opengl, y_opengl, scale)

        glfw.swap_buffers(window)  # Intercambiar buffers para animación suave
        glfw.poll_events()

    glfw.terminate()  # Cerrar GLFW al salir
    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()