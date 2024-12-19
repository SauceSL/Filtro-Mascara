import cv2 as cv
import numpy as np
import time

# Cargar la imagen en escala de grises
img = cv.imread('C:\\Users\\Sauce\\Desktop\\graficacion\\phyton\\2PAC.jpg', 0)

# Verificar si la imagen se ha cargado correctamente
if img is None:
    print("Error al cargar la imagen.")
    exit()

# Obtener el tamaño de la imagen
x, y = img.shape

# Definir el factor de escala
scale_x, scale_y = 1, 1

# Crear una nueva imagen para almacenar el escalado
scaled_img = np.zeros((int(x * scale_y), int(y * scale_x)), dtype=np.uint8)

# Aplicar el escalado
for i in range(int(x * scale_y)):
    for j in range(int(y * scale_x)):
        orig_x = int(i / scale_y)
        orig_y = int(j / scale_x)
        if 0 <= orig_x < x and 0 <= orig_y < y:
            scaled_img[i, j] = img[orig_x, orig_y]

# Función para aplicar un filtro de convolución
def apply_convolution(image, kernel):
    filtered_img = np.zeros_like(image)
    kernel_size = kernel.shape[0]
    pad = kernel_size // 2
    padded_img = np.pad(image, pad, mode='constant', constant_values=0)
    
    for i in range(pad, padded_img.shape[0] - pad):
        for j in range(pad, padded_img.shape[1] - pad):
            region = padded_img[i-pad:i+pad+1, j-pad:j+pad+1]
            filtered_value = np.sum(region * kernel)
            filtered_img[i-pad, j-pad] = np.clip(filtered_value, 0, 255)
    
    return filtered_img

# Definir los kernels de convolución
kernel_3x3 = np.array([[1, 2, 1],
                       [2, 4, 2],
                       [1, 2, 1]], np.float32)
kernel_3x3 = kernel_3x3 / np.sum(kernel_3x3)

kernel_vertical = np.array([[1],
                            [2],
                            [1]], np.float32)
kernel_vertical = kernel_vertical / np.sum(kernel_vertical)

kernel_horizontal = np.array([[1, 2, 1]], np.float32)
kernel_horizontal = kernel_horizontal / np.sum(kernel_horizontal)

# Aplicar los filtros de convolución
filtered_img_3x3 = apply_convolution(scaled_img, kernel_3x3)
filtered_img_vertical = apply_convolution(scaled_img, kernel_vertical)
filtered_img_horizontal = apply_convolution(scaled_img, kernel_horizontal)

# Mostrar la imagen original, la escalada y las filtradas
cv.imshow('Imagen Original', img)
cv.imshow('Imagen Escalada (modo raw)', scaled_img)
cv.imshow('Imagen Filtrada (Kernel 3x3)', filtered_img_3x3)
cv.imshow('Imagen Filtrada (Kernel Vertical)', filtered_img_vertical)
cv.imshow('Imagen Filtrada (Kernel Horizontal)', filtered_img_horizontal)
cv.waitKey(0)
cv.destroyAllWindows()