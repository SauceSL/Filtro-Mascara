# Configurar Cámara

Este código utiliza OpenCV para capturar video en tiempo real desde una cámara conectada al sistema. Se procesan imágenes en diferentes formatos, como escala de grises, HSV y la imagen negativa. A continuación se explica cada parte:

---

## Código Completo

```python
import cv2 as cv
import numpy as np

# Iniciar la captura de video desde la cámara predeterminada
cap = cv.VideoCapture(0)

while True:
    ret, img = cap.read()  # Leer un cuadro de la cámara
    if ret:  # Si la cámara está funcionando
        cv.imshow('video', img)  # Mostrar el video en color

        # Convertir la imagen a escala de grises
        img2 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # Convertir la imagen al espacio de color HSV
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        # Obtener el tamaño de la imagen en escala de grises
        w, h = img2.shape

        # Crear la imagen negativa (inversión de colores)
        img3 = 255 - img2

        # Mostrar las imágenes procesadas
        cv.imshow('img2', img2)  # Escala de grises
        cv.imshow('hsv', hsv)   # Espacio de color HSV
        cv.imshow('img3', img3)  # Imagen negativa

        # Verificar si se presiona la tecla 'ESC' para salir
        k = cv.waitKey(1) & 0xFF
        if k == 27:  # Código ASCII de la tecla 'ESC'
            break
    else:
        break

# Liberar la cámara y cerrar todas las ventanas
cap.release()
cv.destroyAllWindows()
