# Filtro Máscara

Este programa utiliza la biblioteca OpenCV para simular un filtro en el que se coloca una máscara (como una imagen PNG con transparencia) sobre la región de la cara detectada en tiempo real a través de la cámara. La detección de rostros se realiza utilizando un clasificador Haar Cascade, lo que permite posicionar y ajustar la máscara a las dimensiones del rostro detectado. 

## Código

```python
import cv2
import numpy as np

# Cargar la máscara (PNG con transparencia)
mascara = cv2.imread('C:\\Users\\Sauce\\Desktop\\graficacion\\phyton\\PUG.png', cv2.IMREAD_UNCHANGED)

# Cargar el clasificador Haar Cascade para detectar rostros
face_cascade = cv2.CascadeClassifier('C:\\Users\\Sauce\\Desktop\\graficacion\\phyton\\haarcascade_frontalface_alt2.xml')

# Capturar video desde la cámara (o un archivo de video)
video = cv2.VideoCapture(0)  # Cambia 0 por la ruta de un archivo si usas video pregrabado

# Ajustes de desplazamiento de la máscara
desplazamiento_x = 0
desplazamiento_y = 10

while True:
    # Leer cada frame del video
    ret, frame = video.read()
    if not ret:
        break

    # Convertir el frame a escala de grises
    frame_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar rostros en el frame
    rostros = face_cascade.detectMultiScale(frame_gris, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Procesar cada rostro detectado
    for (x, y, w, h) in rostros:
        # Redimensionar la máscara al tamaño del rostro
        mascara_redimensionada = cv2.resize(mascara, (w, h))

        # Separar los canales de la máscara: color y alfa (transparencia)
        mascara_rgb = mascara_redimensionada[:, :, :3]  # Canal de color
        mascara_alpha = mascara_redimensionada[:, :, 3]  # Canal alfa

        # Crear una región de interés (ROI) en el frame
        roi = frame[y:y+h, x:x+w]

        # Invertir la máscara alfa para el fondo del rostro
        mascara_alpha_inv = cv2.bitwise_not(mascara_alpha)

        # Enmascarar la región del rostro
        fondo = cv2.bitwise_and(roi, roi, mask=mascara_alpha_inv)

        # Enmascarar la máscara RGB
        mascara_fg = cv2.bitwise_and(mascara_rgb, mascara_rgb, mask=mascara_alpha)

        # Combinar el fondo y la máscara
        resultado = cv2.add(fondo, mascara_fg)

        # Reemplazar la región del rostro con la imagen combinada
        frame[y:y+h, x:x+w] = resultado

    # Mostrar el frame con la máscara aplicada
    cv2.imshow('Video con máscara', frame)

    # Presionar 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la captura de video y cerrar las ventanas
video.release()
cv2.destroyAllWindows()
