import cv2
import numpy as np
import math

# ================================
# 1. Cargar imagen
# ================================
img = cv2.imread("jitomates/jitomates3.jpg")
if img is None:
    raise Exception("No se pudo cargar la imagen.")

cv2.imshow("1 - Imagen Original", img)

# ================================
# 2. Convertir a HSV
# ================================
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# ================================
# 3. Crear máscara para MANTENER SOLO ROJO
# ================================
# El rojo en HSV está en dos rangos porque el círculo HSV tiene el rojo en ambos extremos
# Rango 1: Rojo bajo (0-10)
lower_red1 = np.array([0, 50, 50])
upper_red1 = np.array([10, 255, 255])

# Rango 2: Rojo alto (170-180)
lower_red2 = np.array([170, 50, 50])
upper_red2 = np.array([180, 255, 255])

# Crear máscaras
mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)

# Combinar ambas máscaras de rojo
mask_rojo = mask_red1 | mask_red2

# ================================
# 4. Filtros morfológicos para cerrar huecos y unir partes divididas
# ================================
height, width = img.shape[:2]
# Aumentar kernel size para unir mejor partes divididas por ramas
kernel_size = max(10, int(min(width, height) / 50))

# Cerrar huecos pequeños (unir partes cercanas divididas por ramas delgadas)
kernel_close = np.ones((kernel_size, kernel_size), np.uint8)
mask_close = cv2.morphologyEx(mask_rojo, cv2.MORPH_CLOSE, kernel_close)

# Eliminar ruido pequeño (kernel más pequeño para no eliminar partes importantes)
kernel_open = np.ones((max(3, kernel_size // 2), max(3, kernel_size // 2)), np.uint8)
mask_final = cv2.morphologyEx(mask_close, cv2.MORPH_OPEN, kernel_open)

cv2.imshow("2 - Máscara Final", mask_final)

# ================================
# 5. Detectar contornos
# ================================
contours, _ = cv2.findContours(mask_final, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# ================================
# 6. Unir contornos cercanos (jitomates divididos por ramas)
# ================================
def boxes_should_merge(box1, box2, threshold=0.6):
    """Verifica si dos bounding boxes deberían unirse"""
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    
    # Verificar superposición (aunque sea mínima)
    overlap_x = max(0, min(x1 + w1, x2 + w2) - max(x1, x2))
    overlap_y = max(0, min(y1 + h1, y2 + h2) - max(y1, y2))
    if overlap_x > 0 and overlap_y > 0:
        return True
    
    # Calcular distancia entre centros
    center1 = (x1 + w1/2, y1 + h1/2)
    center2 = (x2 + w2/2, y2 + h2/2)
    distance = math.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)
    
    # Calcular tamaño promedio
    size1 = math.sqrt(w1 * h1)
    size2 = math.sqrt(w2 * h2)
    avg_size = (size1 + size2) / 2
    
    # Si uno es mucho más pequeño, podría ser parte del otro (relajar validación)
    size_ratio = min(size1, size2) / max(size1, size2) if max(size1, size2) > 0 else 0
    # Si el más pequeño es al menos 20% del grande, o están muy cerca, unir
    if size_ratio < 0.2 and distance > avg_size * 0.8:
        return False
    
    # Si están cerca (distancia < umbral * tamaño promedio), unir
    return distance < avg_size * threshold

def merge_boxes(box1, box2):
    """Une dos bounding boxes"""
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    
    x_min = min(x1, x2)
    y_min = min(y1, y2)
    x_max = max(x1 + w1, x2 + w2)
    y_max = max(y1 + h1, y2 + h2)
    
    return (x_min, y_min, x_max - x_min, y_max - y_min)

# Obtener bounding boxes de todos los contornos
detections = []
min_area = (width * height) * 0.001  # Área mínima: 0.1% de la imagen
for c in contours:
    area = cv2.contourArea(c)
    if area < min_area:  # Filtrar ruido pequeño
        continue
    x, y, w, h = cv2.boundingRect(c)
    detections.append((x, y, w, h))

# Unir detecciones cercanas (algoritmo iterativo para unir múltiples partes)
merged_detections = []
used = [False] * len(detections)

for i in range(len(detections)):
    if used[i]:
        continue
    
    merged_box = detections[i]
    used[i] = True
    changed = True
    
    # Iterar hasta que no se puedan unir más partes
    while changed:
        changed = False
        for j in range(len(detections)):
            if used[j]:
                continue
            
            if boxes_should_merge(merged_box, detections[j]):
                merged_box = merge_boxes(merged_box, detections[j])
                used[j] = True
                changed = True
    
    merged_detections.append(merged_box)

# ================================
# 7. Dibujar resultados finales
# ================================
output = img.copy()
count = 0

for x, y, w, h in merged_detections:
    count += 1
    cv2.rectangle(output, (int(x), int(y)), (int(x+w), int(y+h)), (0, 255, 0), 3)
    cv2.putText(output, f"Tomate {count}", (int(x), int(y-10)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

cv2.imshow(f"3 - Jitomates Detectados {count}", output)

cv2.waitKey(0)
cv2.destroyAllWindows()
