# Dibujo

Este código utiliza NumPy y OpenCV para dibujar un conjunto de letras sobre una imagen en escala de grises. A continuación se explica el código:

## Código Completo

```python
import numpy as np   # Importa la librería NumPy
import cv2 as cv     # Importa la librería OpenCV

# Crea una imagen de 500x500 píxeles, todos con valor 240 (gris claro).
img = np.ones((500, 500), dtype=np.uint8) * 240

# Dibuja la letra 'H'
img[30:40, 30] = 1   # Línea vertical izquierda
img[30:40, 50] = 1   # Línea vertical derecha
img[35, 30:50] = 1   # Línea horizontal media

# Dibuja la letra 'O'
cv.circle(img, (80, 35), 10, 1, -1)  # Circulo lleno en (80, 35) con radio 10

# Dibuja la letra 'L'
img[30:40, 110] = 1  # Línea vertical
img[38:40, 100:120] = 1  # Línea horizontal

# Dibuja la letra 'A'
img[30:40, 150] = 1  # Línea vertical izquierda
img[30:40, 170] = 1  # Línea vertical derecha
img[35, 150:170] = 1  # Línea horizontal media
img[30:35, 150:170] = 1  # Línea diagonal izquierda
img[30:35, 170:150] = 1  # Línea diagonal derecha

# Muestra la imagen en una ventana con el título 'img'.
cv.imshow('img', img)

# Espera a que el usuario presione cualquier tecla para continuar.
cv.waitKey()

# Cierra todas las ventanas creadas por OpenCV.
cv.destroyAllWindows()