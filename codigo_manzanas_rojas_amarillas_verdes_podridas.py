# TÉCNICA 1: SEGMENTACIÓN POR COLOR HSV
# Se implementó un segmentador basado en color, utilizando el espacio HSV 
# para detectar manzanas rojas, verdes, amarillas y podridas. 
# Se aplicaron máscaras y limpieza morfológica para aislar cada tipo, 
# generando imágenes segmentadas y sus ground truths para su evaluación.

import cv2
import numpy as np
import matplotlib.pyplot as plt
import requests
import os
# ----------------------------------------------------------------------------
# 1. Cargar imagen desde Google Drive
file_id = "1NhXPnYDxchFQZtu-4zmNOTjfSztKT2rw"
url = f"https://drive.google.com/uc?export=download&id={file_id}"
response = requests.get(url, timeout=10)
if response.status_code != 200:
    raise ValueError(f"❌ No se pudo descargar la imagen desde Google Drive")
# Convertir la imagen descargada a array de OpenCV
img_array = np.frombuffer(response.content, np.uint8)
img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
if img is None:
    raise ValueError("❌ La imagen no se pudo decodificar")
# Convertir a RGB porque matplotlib NO usa BGR
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# ----------------------------------------------------------------------------
# 2. Convertir imagen a espacio de color HSV
# HSV permite detectar colores según tono (Hue), saturación y brillo
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# ----------------------------------------------------------------------------
# 3. Definir rangos de color para segmentar cada tipo de manzana
# MANZANAS ROJAS
lower_red1 = np.array([0, 100, 70])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([160, 100, 70])
upper_red2 = np.array([180, 255, 255])
# MANZANAS AMARILLAS
lower_yellow = np.array([15, 80, 80])
upper_yellow = np.array([35, 255, 255])
# MANZANAS VERDES
lower_green = np.array([35, 40, 40])
upper_green = np.array([95, 255, 255])
# MANZANAS PODRIDAS (CAFÉS)
lower_brown = np.array([5, 100, 20])
upper_brown = np.array([20, 255, 180])
# ----------------------------------------------------------------------------
# 4. Crear máscaras binarias (detección de cada color)
mask_red = cv2.bitwise_or(
    cv2.inRange(hsv, lower_red1, upper_red1),
    cv2.inRange(hsv, lower_red2, upper_red2))
mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
mask_green  = cv2.inRange(hsv, lower_green,  upper_green)
mask_brown  = cv2.inRange(hsv, lower_brown,  upper_brown)
# ----------------------------------------------------------------------------
# 5. Aplicar limpieza morfológica para eliminar ruido
kernel = np.ones((5, 5), np.uint8)
def limpiar(mask):
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)   # elimina ruido
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # rellena huecos
    return mask
mask_red    = limpiar(mask_red)
mask_yellow = limpiar(mask_yellow)
mask_green  = limpiar(mask_green)
mask_brown  = limpiar(mask_brown)
# ----------------------------------------------------------------------------
# 6. Crear imágenes segmentadas
seg_red    = cv2.bitwise_and(img_rgb, img_rgb, mask=mask_red)
seg_yellow = cv2.bitwise_and(img_rgb, img_rgb, mask=mask_yellow)
seg_green  = cv2.bitwise_and(img_rgb, img_rgb, mask=mask_green)
seg_brown  = cv2.bitwise_and(img_rgb, img_rgb, mask=mask_brown)
# ----------------------------------------------------------------------------
# 7. Guardar las Ground Truth en carpetas
output_dir = r"manzanas_result"
os.makedirs(output_dir, exist_ok=True)
paths = {
    "rojas":    os.path.join(output_dir, "ground_truth_rojas.png"),
    "amarillas":os.path.join(output_dir, "ground_truth_amarillas.png"),
    "verdes":   os.path.join(output_dir, "ground_truth_verdes.png"),
    "podridas": os.path.join(output_dir, "ground_truth_podridas.png"),}
cv2.imwrite(paths["rojas"],    mask_red)
cv2.imwrite(paths["amarillas"],mask_yellow)
cv2.imwrite(paths["verdes"],   mask_green)
cv2.imwrite(paths["podridas"], mask_brown)
# ----------------------------------------------------------------------------
# 8. Mostrar resultados
# Imagen original sola
plt.figure(figsize=(3.25,3.25))
plt.imshow(img_rgb)
plt.title("Imagen Original")
plt.axis("off")
plt.show()
# Tabla 4x2: Ground truth y segmentación
fig, axes = plt.subplots(2, 4, figsize=(20,10))
colores = [
    ("ROJAS", mask_red, seg_red),
    ("AMARILLAS", mask_yellow, seg_yellow),
    ("VERDES", mask_green, seg_green),
    ("PODRIDAS", mask_brown, seg_brown)]
for i, (nombre, mask, seg) in enumerate(colores):
    # Ground Truth
    axes[0, i].imshow(mask, cmap='gray')
    axes[0, i].set_title(f"GROUND TRUTH - {nombre}")
    axes[0, i].axis("off")
    # Segmentación
    axes[1, i].imshow(seg)
    axes[1, i].set_title(f"SEGMENTACIÓN - {nombre}")
    axes[1, i].axis("off")
plt.tight_layout()
plt.show()

