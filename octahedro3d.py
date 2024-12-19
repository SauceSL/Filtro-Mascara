import glfw
from OpenGL.GL import glClearColor, glEnable, glClear, glLoadIdentity, glTranslatef, glRotatef, glMatrixMode
from OpenGL.GL import glBegin, glColor3f, glVertex3f, glEnd, glFlush, glViewport
from OpenGL.GL import GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST, GL_TRIANGLES, GL_PROJECTION, GL_MODELVIEW
from OpenGL.GLU import gluPerspective
import sys

# Variables globales
window = None
angle = 0  # Declaramos angle en el nivel superior

def init():
    # Configuración inicial de OpenGL
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Color de fondo
    glEnable(GL_DEPTH_TEST)  # Activar prueba de profundidad para 3D
    # Configuración de proyección
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(240, 1.0, 1.0, 50.0)
    # Cambiar a la matriz de modelo para los objetos
    glMatrixMode(GL_MODELVIEW)

def draw_octahedron():
    global angle
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Limpiar pantalla y buffer de profundidad
    # Configuración de la vista del octaedro
    glLoadIdentity()
    glTranslatef(0.0, 0, -1)  # Alejar el octaedro para que sea visible
    glRotatef(angle, 0, 0.5, 1)   # Rotar el octaedro en todos los ejes
    glBegin(GL_TRIANGLES)  # Iniciar el octaedro como un conjunto de caras (triángulos)
    
    # Vértices del octaedro
    vertices = [
        (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)
    ]
    
    # Caras del octaedro (cada cara es un triángulo)
    caras = [
        (0, 2, 4), (2, 1, 4), (1, 3, 4), (3, 0, 4),
        (0, 2, 5), (2, 1, 5), (1, 3, 5), (3, 0, 5)
    ]
    
    # Colores para cada cara
    colores = [
        (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0), (1.0, 1.0, 0.0),
        (1.0, 0.0, 1.0), (0.0, 1.0, 1.0), (0.5, 0.5, 0.5), (1.0, 0.5, 0.0)
    ]
    
    for i, cara in enumerate(caras):
        glColor3f(*colores[i])
        for vertice in cara:
            glVertex3f(*vertices[vertice])
    
    glEnd()
    glFlush()
    glfw.swap_buffers(window)  # Intercambiar buffers para animación suave
    angle += 0.2  # Incrementar el ángulo para rotación

def main():
    global window
    # Inicializar GLFW
    if not glfw.init():
        sys.exit()
    # Crear ventana de GLFW
    width, height = 500, 500
    window = glfw.create_window(width, height, "Octaedro 3D Rotando con GLFW", None, None)
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
        draw_octahedron()
        glfw.poll_events()
    glfw.terminate()  # Cerrar GLFW al salir

if __name__ == "__main__":
    main()
