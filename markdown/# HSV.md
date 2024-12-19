# Primitivas en espacio de color HSV

Este documento detalla un script en Python que utiliza la biblioteca OpenCV para crear y manipular imágenes mediante primitivas gráficas como círculos, líneas y polígonos, empleando el espacio de color HSV (Hue, Saturation, Value) en lugar de RGB. A continuación, se desglosa cada parte del código y su funcionalidad.

## Código

```python
import cv2 as cv
import numpy as np

# Crear una imagen en blanco de 500x500 píxeles con 3 canales de color (HSV)
img = np.ones((500, 500, 3), dtype=np.uint8) * 255 
img_hsv = cv.cvtColor(img, cv.COLOR_RGB2HSV) # Convertir la imagen a HSV

# Definir el color en HSV: (H, S, V)
# Color verde en HSV
verde = np.array([60, 255, 255], dtype=np.uint8) 

# Dibujar un círculo verde (en HSV) de radio 50
cv.circle(img, (250, 250), 50, cv.cvtColor(np.array([[verde]], dtype=np.uint8), cv.COLOR_HSV2BGR)[0][0].tolist(), -1)

# Dibujar un círculo negro (usando BGR) de radio 30 en el mismo centro
cv.circle(img, (250, 250), 30, (0, 0, 0), -1)

# Dibujar una línea verde desde el punto (1, 1) hasta el punto (230, 240) con un grosor de 3
cv.line(img, (1, 1), (230, 240), cv.cvtColor(np.array([[verde]], dtype=np.uint8), cv.COLOR_HSV2BGR)[0][0].tolist(), 3)

# Dibujar un rectángulo negro en la posición (20, 20) hasta (50, 60) con un grosor de 3
cv.rectangle(img, (20, 20), (50, 60), (0, 0, 0), 3)

# Definir un conjunto de puntos para dibujar un polígono
pts = np.array([[10, 5], [20, 30], [70, 20], [50, 10]], np.int32)
pts = pts.reshape((-1, 1, 2))

# Dibujar el polígono utilizando los puntos definidos con un grosor de 3
cv.polylines(img, [pts], True, (0, 0, 0), 3)

# Crear una segunda imagen en blanco de 500x500 píxeles, pero en escala de grises
img2 = np.ones((500, 500), dtype=np.uint8) * 255 

# Dibujar círculos en diferentes posiciones y tamaños en la primera imagen en un bucle
for i in range(50):
    # Dibujar círculos de tamaño creciente
    cv.circle(img, (250 + i, 250 + i), 20 + i, cv.cvtColor(np.array([[verde]], dtype=np.uint8), cv.COLOR_HSV2BGR)[0][0].tolist(), -1)
    cv.imshow('img2', img2) # Mostrar img2 que permanece blanco en este caso
    cv.waitKey(40) # Esperar 40 milisegundos antes de la siguiente iteración

# Mostrar la imagen final con todas las primitivas graficadas
cv.imshow('img', img)
cv.imshow('img2', img2) # Mostrar img2 que sigue siendo blanco
cv.waitKey() # Esperar a que se pulse alguna tecla
cv.destroyAllWindows() # Cerrar todas las ventanas abiertas