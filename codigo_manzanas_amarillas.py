#El programa realiza la detección automática de manzanas amarillas utilizando OpenCV . Primero, la imagen se convierte 
#al espacio de color y segmentacion utilizada HSV, ya que permite detectar colores de forma más estable que el espacio RGB, después se define 
#un rango de color amarillo para crear una máscara binaria, después se limpia el ruido para mejorar la mascara y guardarlo 
#como un Ground Truth. Al final resalta la zona amarilla en la imagen original aumentando su brillo y dibuja los contornos
#alrededor de la manzana detectada.

import cv2                 # Librería para procesamiento de imágenes y visión por computadora
import numpy as np         # Librería para manejo de arreglos numéricos
import matplotlib.pyplot as plt  # Librería para mostrar imágenes con gráficos


# 1. RUTAS EN WINDOWS 

ruta_imagen = "manzanas/manzana_amarilla.jpg"     # Ruta de la imagen original
ruta_groundtruth = "manzanas/groundtruth_manzana.png"  # Ruta donde se guardará la máscara (GT)
ruta_resaltada = "manzanas/manzana_resaltada_contornos.png"  # Ruta para la imagen final resaltada


# 2. Se carga la imagen original

img = cv2.imread(ruta_imagen) 

if img is None:                # Verifica si la imagen fue cargada correctamente
    print("ERROR: No se pudo cargar la imagen. Verifica la ruta.")
    exit()                     # Detiene la ejecución si no existe la imagen


# 3. Convierte a HSV y detecta el color amarillo

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # Convierteel formato de la imagen de BGR (formato OpenCV) a HSV

# Rango aproximado para detectar tonos amarillos
lower_yellow = np.array([15, 40, 80])       # Límite inferior del rango HSV
upper_yellow = np.array([35, 255, 255])     # Límite superior del rango HSV

# Se crea la máscara binaria: los píxeles dentro del rango serán blancos (255), los demás negros (0)
mask = cv2.inRange(hsv, lower_yellow, upper_yellow)


# 4. Se limpia la mascara del ruido con morfología

kernel = np.ones((5,5), np.uint8)           # Kernel para operaciones morfológicas (tamaño 5x5)

mask_clean = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)   # Elimina ruido pequeño
mask_clean = cv2.morphologyEx(mask_clean, cv2.MORPH_CLOSE, kernel)  # Rellena huecos dentro de la región


# 5. Guardar Ground Truth generado

cv2.imwrite(ruta_groundtruth, mask_clean)   # Guarda la máscara procesada como ground truth
print("Ground truth guardado en:", ruta_groundtruth)


# 6. Resaltar manzana manteniendo color original

resaltada = img.copy()                      # Copia la imagen para no modificar la original

# Aumenta el brillo únicamente en píxeles donde la máscara es blanca (255)
resaltada[mask_clean == 255] = np.clip(
    resaltada[mask_clean == 255] * 1.4,     # Multiplica el brillo unicamente del área detectada
    0, 255                                  # Limita valores entre 0 y 255
).astype(np.uint8)


# 7. Encontrar contornos y dibujarlos

contornos, _ = cv2.findContours(mask_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# Encuentra contornos externos basados en la máscara procesada

for cnt in contornos:                       # Recorre todos los contornos encontrados
    area = cv2.contourArea(cnt)             # Calcula el área del contorno

    if area > 100:                           # Evita dibujar contornos muy pequeños (ruido)
        cv2.drawContours(resaltada, [cnt], -1, (255, 0, 0), 3)  # Dibuja contorno en color azul (BGR)

# Guarda imagen resaltada final
cv2.imwrite(ruta_resaltada, resaltada)
print("Imagen resaltada con contornos guardada en:", ruta_resaltada)


# 8. Mostrar imágenes con Matplotlib


# OpenCV usa BGR, Matplotlib usa RGB → por lo que se procede a convertir
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
resaltada_rgb = cv2.cvtColor(resaltada, cv2.COLOR_BGR2RGB)

plt.figure(figsize=(15,8))

plt.subplot(1,3,1)
plt.imshow(img_rgb)
plt.title("Imagen Original")
plt.axis("off")

plt.subplot(1,3,2)
plt.imshow(mask_clean, cmap="gray")
plt.title("Ground Truth / Máscara")
plt.axis("off")

plt.subplot(1,3,3)
plt.imshow(resaltada_rgb)
plt.title("Imagen con Contornos")
plt.axis("off")

plt.tight_layout()
plt.show()