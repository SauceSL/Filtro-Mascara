import numpy as np
import cv2

# Crear una matriz de ceros (negro)
size = 400  # Tamaño de la imagen
heart = np.zeros((size, size), dtype=np.uint8)

# Dibujar el corazón
for y in range(size):
    for x in range(size):
        # Fórmulas para el corazón
        if ((x - size // 2) ** 2 + (y - size // 2) ** 2 - 25) ** 3 - (x - size // 2) ** 2 * (y - size // 2) ** 3 <= 0:
            heart[y, x] = 255  # Color blanco (255)

# Usar cv2 para mostrar la imagen
cv2.imshow('Corazón', heart)
cv2.waitKey(0)  # Esperar a que se presione una tecla
cv2.destroyAllWindows()  # Cerrar la ventana