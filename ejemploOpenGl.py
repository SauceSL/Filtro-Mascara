import glfw 
from OpenGL.GL import glClear, glClearColor, glBegin, glEnd, glVertex2f, glColor3f, GL_COLOR_BUFFER_BIT, GL_QUADS, GL_TRIANGLES

def main():
    # Inicializar GLFW
    if not glfw.init():
        return

    # Crear la ventana
    window = glfw.create_window(500, 500, "OpenGL con GLFW", None, None)
    if not window:
        glfw.terminate()
        return

    # Hacer el contexto de OpenGL actual
    glfw.make_context_current(window)

    # Establecer el color de fondo
    glClearColor(0.0, 0.0, 0.0, 1.0)

    # Bucle principal de renderizado
    while not glfw.window_should_close(window):
        # Limpiar la pantalla
        glClear(GL_COLOR_BUFFER_BIT)

        # Dibujar un triángulo
        glBegin(GL_QUADS)
        glColor3f(1.0, 0.0, 0.0)  # Rojo
        glColor3f(0.0, 0.25, 0.0)  # verde
        glColor3f(0.0, 0.0, 0.50)  # azul
        glVertex2f(-0.5,  0.5)  # Vértice superior izquierdo
        glVertex2f( 0.5,  0.5)  # Vértice superior derecho
        glVertex2f( 0.5, -0.5)  # Vértice inferior derecho
        glVertex2f(-0.5, -0.5) 

        glEnd()

        # Intercambiar buffers y procesar eventos
        glfw.swap_buffers(window)
        glfw.poll_events()

    # Terminar GLFW
    glfw.terminate()

if __name__ == "__main__":
    main()