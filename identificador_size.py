# Utilizando OpenCV para segmentar y clasificar dos manzanas dentro de una imagen, el primer método utilizado fue la detección 
#de contornos mediante conversión a escala de grises, suavizado con filtro Gaussiano y aplicación del detector de bordes Canny,
#seguido de operaciones morfológicas para cerrar los contornos. Una vez identificadas las regiones de cada manzana, se clasificaron
#en “chica” o “grande” según el área de sus contornos.
 
import cv2
import numpy as np
import matplotlib.pyplot as plt
 
# ---------------------------------------------------
# 1. Cargar imagen
# ---------------------------------------------------
img = cv2.imread("manzanas/manzana_chica_grande.JPG")
orig = img.copy()
 
 
# ---------------------------------------------------
# 2. Preprocesamiento: gris + blur
# ---------------------------------------------------
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (7, 7), 0)
 
 
# ---------------------------------------------------
# 3. Segmentar usando Canny (mismo método que antes)
# ---------------------------------------------------
edges = cv2.Canny(blur, 40, 120)
 
# Cerrar bordes desconectados
kernel = np.ones((7, 7), np.uint8)
closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
 
 
# ---------------------------------------------------
# 4. Encontrar contornos (segmentación automática)
# ---------------------------------------------------
contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 
 
# ---------------------------------------------------
# 5. Generar GROUND TRUTH 
# ---------------------------------------------------
gt = np.zeros(img.shape[:2], dtype=np.uint8)
 
for c in contours:
    area = cv2.contourArea(c)
 
    # Clasificación por tamaño → para generar etiquetas GT
    if area > 20000:
        etiqueta = 2     # Manzana grande
    else:
        etiqueta = 1     # Manzana chica
 
    # Dibujar el contorno en la máscara GT con su etiqueta
    cv2.drawContours(gt, [c], -1, etiqueta, thickness=-1)
 
 
# ---------------------------------------------------
# 6. Dibujar clasificaciones sobre la imagen real
# ---------------------------------------------------
for c in contours:
    area = cv2.contourArea(c)
    x, y, w, h = cv2.boundingRect(c)
 
    if area > 20000:
        tipo = "Grande"
    else:
        tipo = "Chica"
 
    cv2.rectangle(orig, (x, y), (x+w, y+h), (0,255,0), 2)
    cv2.putText(orig, tipo, (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
 
 
# ---------------------------------------------------
# 7. Preparar imágenes para mostrar
# ---------------------------------------------------
img_rgb  = cv2.cvtColor(img,  cv2.COLOR_BGR2RGB)
orig_rgb = cv2.cvtColor(orig, cv2.COLOR_BGR2RGB)
 
# Escalar GT para que matplotlib lo pinte con colores
gt_display = gt.copy()
 
 
# ---------------------------------------------------
# 8. Visualización con Matplotlib
# ---------------------------------------------------
plt.figure(figsize=(14,6))
 
plt.subplot(1,4,1)
plt.title("Original")
plt.imshow(img_rgb)
plt.axis("off")
 
plt.subplot(1,4,2)
plt.title("Canny + cierre morfológico")
plt.imshow(closed, cmap="gray")
plt.axis("off")
 
plt.subplot(1,4,3)
plt.title("Ground Truth generado")
plt.imshow(gt_display, cmap="jet")
plt.axis("off")
 
plt.subplot(1,4,4)
plt.title("Clasificación Final")
plt.imshow(orig_rgb)
plt.axis("off")
 
plt.tight_layout()
plt.show()