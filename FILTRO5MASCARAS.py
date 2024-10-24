import cv2
import numpy as np

# Cargar las 5 máscaras con transparencia (PNG)
mascaras = [
    cv2.imread('C:\\Users\\Sauce\\Desktop\\graficacion\\phyton\\LOBO.png', cv2.IMREAD_UNCHANGED),
    cv2.imread('C:\\Users\\Sauce\\Desktop\\graficacion\\phyton\\ROSA.png', cv2.IMREAD_UNCHANGED),
    cv2.imread('C:\\Users\\Sauce\\Desktop\\graficacion\\phyton\\GAFAS.png', cv2.IMREAD_UNCHANGED),
    cv2.imread('C:\\Users\\Sauce\\Desktop\\graficacion\\phyton\\SOMBRERO.png', cv2.IMREAD_UNCHANGED),
    cv2.imread('C:\\Users\\Sauce\\Desktop\\graficacion\\phyton\\BIGOTE.png', cv2.IMREAD_UNCHANGED)
]

# Ajustes de escala y desplazamiento para cada máscara
escalas = [0.1, 0.1, 0.6, 0.75, 0.5]  # Escala para cada máscara (1.0 = tamaño original del rostro)
desplazamientos_x = [20, 40, 35, 25, 50]  # Desplazamiento en X para cada máscara
desplazamientos_y = [40, 40, 25, -100, 130]  # Desplazamiento en Y para cada máscara

# Cargar el clasificador de rostros
face_cascade = cv2.CascadeClassifier('C:\\Users\\Sauce\\Desktop\\graficacion\\phyton\\haarcascade_frontalface_alt2.xml')

# Iniciar captura de video
video = cv2.VideoCapture(0)

while True:
    # Leer cada frame del video
    ret, frame = video.read()
    if not ret:
        break

    # Convertir el frame a escala de grises
    frame_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar los rostros en el frame
    rostros = face_cascade.detectMultiScale(frame_gris, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Procesar cada rostro detectado
    for (x, y, w, h) in rostros:
        for idx, mascara in enumerate(mascaras):
            # Obtener escala y desplazamiento específicos de cada máscara
            escala = escalas[idx]
            dx = desplazamientos_x[idx]
            dy = desplazamientos_y[idx]

            # Redimensionar la máscara según la escala
            ancho_mascara = int(w * escala)
            alto_mascara = int(h * escala)
            mascara_redimensionada = cv2.resize(mascara, (ancho_mascara, alto_mascara))

            # Separar los canales de la máscara: color y alfa
            mascara_rgb = mascara_redimensionada[:, :, :3]
            mascara_alpha = mascara_redimensionada[:, :, 3]

            # Calcular la nueva posición con los desplazamientos
            x_mascara = x + dx
            y_mascara = y + dy

            # Asegurar que la máscara no se salga de los bordes del frame
            x_mascara = max(0, min(x_mascara, frame.shape[1] - ancho_mascara))
            y_mascara = max(0, min(y_mascara, frame.shape[0] - alto_mascara))

            # Crear un ROI para la máscara en la nueva posición
            roi_mascara = frame[y_mascara:y_mascara + alto_mascara, x_mascara:x_mascara + ancho_mascara]

            # Invertir la máscara alfa
            mascara_alpha_inv = cv2.bitwise_not(mascara_alpha)

            # Enmascarar la región del ROI
            fondo = cv2.bitwise_and(roi_mascara, roi_mascara, mask=mascara_alpha_inv)

            # Enmascarar la máscara RGB
            mascara_fg = cv2.bitwise_and(mascara_rgb, mascara_rgb, mask=mascara_alpha)

            # Combinar fondo y máscara
            resultado = cv2.add(fondo, mascara_fg)

            # Colocar el resultado en el frame
            frame[y_mascara:y_mascara + alto_mascara, x_mascara:x_mascara + ancho_mascara] = resultado

    # Mostrar el frame con las máscaras aplicadas
    cv2.imshow('Video con Mascaras en un Rostro', frame)

    # Presionar 'q' para salir del loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la captura de video y cerrar las ventanas
video.release()
cv2.destroyAllWindows()