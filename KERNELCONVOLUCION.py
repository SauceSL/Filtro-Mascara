import cv2 as cv
import numpy as np

# Cargar la imagen en escala de grises
img = cv.imread('C:\\Users\\Sauce\\Desktop\\graficacion\\phyton\\2PAC.jpg', 0)

# Obtener el tamaño de la imagen
x, y = img.shape

# Definir el factor de escala
scale_x, scale_y = 2, 2

# Crear una nueva imagen para almacenar el escalado
scaled_img = np.zeros((int(x * scale_y), int(y * scale_x)), dtype=np.uint8)

# Aplicar el escalado
for i in range(int(x * scale_y)):
    for j in range(int(y * scale_x)):
        orig_x = int(i / scale_y)
        orig_y = int(j / scale_x)
        if 0 <= orig_x < x and 0 <= orig_y < y:
            scaled_img[i, j] = img[orig_x, orig_y]

# Crear una nueva imagen para almacenar el resultado de la convolución
filtered_img = np.zeros_like(scaled_img)

# Definir el kernel de convolución 3x3 con un valor de 1/9
kernel = np.ones((3, 3), np.float32) / 9

# Aplicar la convolución manualmente
for i in range(1, scaled_img.shape[0] - 1):
    for j in range(1, scaled_img.shape[1] - 1):
        # Extraer la región 3x3
        region = scaled_img[i-1:i+2, j-1:j+2]
        # Aplicar el kernel a la región
        filtered_value = np.sum(region * kernel)
        # Asignar el valor filtrado a la imagen de salida
        filtered_img[i, j] = np.clip(filtered_value, 0, 255)

# Mostrar la imagen original, la escalada y la filtrada
cv.imshow('Imagen Original', img)
cv.imshow('Imagen Escalada (modo raw)', scaled_img)
cv.imshow('Imagen Filtrada', filtered_img)
cv.waitKey(0)
cv.destroyAllWindows()