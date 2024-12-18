# Escalado

Este código implementa un escalado manual de una imagen en escala de grises, donde se agranda la imagen duplicando sus píxeles según un factor de escala definido. A continuación se detalla el funcionamiento:

---

## Código Completo

```python
import cv2 as cv
import numpy as np

# Cargar la imagen en escala de grises
img = cv.imread('tr.png', 0)

# Obtener el tamaño de la imagen
x, y = img.shape

# Definir el factor de escala
scale_x, scale_y = 2, 2

# Crear una nueva imagen para almacenar el escalado
scaled_img = np.zeros((int(x * scale_y), int(y * scale_x)), dtype=np.uint8)

# Aplicar el escalado
for i in range(x):
    for j in range(y):
        scaled_img[i * scale_y, j * scale_x] = img[i, j]

# Mostrar la imagen original y la escalada
cv.imshow('Imagen Original', img)
cv.imshow('Imagen Escalada (modo raw)', scaled_img)
cv.waitKey(0)
cv.destroyAllWindows()
