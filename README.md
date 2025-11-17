# 🍎🍅 Sistema de Segmentación y Detección de Frutas

Sistema de visión por computadora para la detección, segmentación y clasificación de frutas utilizando técnicas de procesamiento de imágenes con OpenCV. Este proyecto implementa diferentes algoritmos de segmentación aplicados a la clasificación de frutas, comparando su desempeño frente a máscaras de referencia (ground truth).

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Características](#-características)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Resultados](#-resultados)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)

## 🎯 Descripción

La segmentación de imágenes es una técnica fundamental en visión por computadora que permite identificar y aislar regiones de interés dentro de una imagen, facilitando la clasificación de objetos. Este proyecto implementa varios segmentadores aplicados a la detección de frutas (jitomates y manzanas), evaluando su desempeño mediante comparación con máscaras de referencia (ground truth).

### Funcionalidades Principales

- **Detección de Jitomates Rojos**: Identifica y cuenta jitomates rojos maduros en imágenes, manejando oclusiones y fragmentaciones causadas por ramas.
- **Detección de Manzanas Amarillas**: Segmenta manzanas amarillas utilizando detección por color en espacio HSV.
- **Segmentación Multiclase de Manzanas**: Detecta simultáneamente manzanas rojas, amarillas, verdes y podridas a partir de una sola imagen con generación automática de ground truths.
- **Clasificación por Tamaño**: Clasifica manzanas en "chica" o "grande" según el área de sus contornos.

## ✨ Características

- ✅ Segmentación por color en espacio HSV
- ✅ Operaciones morfológicas para limpieza de máscaras
- ✅ Detección de contornos y bounding boxes
- ✅ Unión de regiones fragmentadas
- ✅ Generación de ground truth automático
- ✅ Visualización de resultados con matplotlib
- ✅ Manejo de oclusiones y ruido

## 📦 Requisitos

- Python 3.11 o superior
- pip (gestor de paquetes de Python)

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone <git@github.com:alexgsisc/practicas-percepcion-computacional.git>
cd practicas
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv venv
```

### 3. Activar entorno virtual

**En macOS/Linux:**
```bash
source venv/bin/activate
```

**En Windows:**
```bash
venv\Scripts\activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 💻 Uso

### Detección de Jitomates Rojos

```bash
python codigo_jitomates.py
```

Este script:
- Carga una imagen de jitomates
- Detecta jitomates rojos mediante segmentación por color
- Une partes fragmentadas por ramas
- Cuenta el número total de jitomates detectados
- Muestra los resultados con bounding boxes

### Detección de Manzanas Amarillas

```bash
python codigo_manzanas_amarillas.py
```

Este script:
- Carga una imagen de manzanas amarillas
- Genera una máscara binaria (ground truth)
- Resalta las manzanas detectadas
- Dibuja contornos alrededor de las manzanas
- Guarda los resultados en archivos PNG

### Clasificación de Manzanas por Tamaño

```bash
python identificador_size.py
```

Este script:
- Detecta manzanas en la imagen
- Clasifica cada manzana como "chica" o "grande"
- Muestra los resultados con etiquetas

### Segmentación Multiclase de Manzanas

```bash
python codigo_manzanas_rojas_amarillas_verdes_podridas.py
```

Este script:
- Descarga y carga automáticamente una imagen de referencia desde Google Drive
- Segmenta manzanas rojas, amarillas, verdes y podridas en el espacio HSV
- Genera y guarda las máscaras (ground truth) por categoría en `manzanas_result/`
- Visualiza las máscaras y las segmentaciones en una cuadrícula 4×2

## 📊 Resultados

A continuación se muestran los resultados obtenidos por cada uno de los scripts implementados:

### Detección de Jitomates Rojos

Los siguientes resultados muestran la detección exitosa de jitomates rojos, incluyendo el manejo de oclusiones y fragmentaciones:

![Resultado 1 - Detección de Jitomates](results/jitomates_resultado1.png)

![Resultado 2 - Detección de Jitomates](results/jitomates_resultado2.png)

![Resultado 3 - Detección de Jitomates](results/jitomates_resultado3.png)

### Detección de Manzanas Amarillas

Resultado de la segmentación de manzanas amarillas utilizando detección por color en espacio HSV:

![Resultado - Detección de Manzanas Amarillas](results/manzanas_amarillar_resultado1.png)

### Clasificación de Manzanas por Tamaño

Resultado de la clasificación automática de manzanas según su tamaño (chica/grande):

![Resultado - Clasificación por Tamaño](results/identificar_size_resultado1.png)

### Segmentación Multiclase de Manzanas

Ground truths y segmentaciones obtenidas para manzanas rojas, amarillas, verdes y podridas en una sola figura:

![Resultado - Segmentación Multiclase](results/manzanas_rojas_amarillas_podridas_result.png)

## 📁 Estructura del Proyecto

```
practicas/
│
├── codigo_jitomates.py              # Detección de jitomates rojos
├── codigo_manzanas_amarillas.py     # Detección de manzanas amarillas
├── identificador_size.py            # Clasificación de manzanas por tamaño
├── codigo_manzanas_rojas_amarillas_verdes_podridas.py
│                                     # Segmentación multiclase de manzanas
│
├── jitomates/                       # Imágenes de jitomates
│   ├── jitomates1.jpg
│   ├── jitomates2.jpg
│   └── ...
│
├── manzanas/                        # Imágenes de manzanas
│   ├── manzana_amarilla.jpg
│   ├── manzana_chica_grande.JPG
│   └── ...
├── manzanas_result/                 # codigo_manzanas_rojas_amarillas_verdes_podridas.py
│   ├── ground_truth_amarillas.png
│   ├── ground_truth_podridas.png
│   └── ...
|
├── results/                         # Resultados de los scripts
│   ├── jitomates_resultado1.png
│   ├── jitomates_resultado2.png
│   ├── jitomates_resultado3.png
│   ├── manzanas_amarillar_resultado1.png
│   ├── identificar_size_resultado1.png
│   └── manzanas_rojas_amarillas_podridas_result.png
│
├── requirements.txt                 # Dependencias del proyecto
├── README.md                        # Este archivo
```

## 🛠️ Tecnologías Utilizadas

- **OpenCV** (4.12.0.88): Procesamiento de imágenes y visión por computadora
- **NumPy** (2.2.6): Operaciones numéricas y manejo de arrays
- **Matplotlib** (3.10.7): Visualización de imágenes y resultados

## 🔧 Configuración

### Modificar rutas de imágenes

En cada script, puedes modificar las rutas de las imágenes:

```python
# Ejemplo en codigo_manzanas_amarillas.py
ruta_imagen = "manzanas/manzana_amarilla.jpg"
ruta_groundtruth = "manzanas/groundtruth_manzana.png"
ruta_resaltada = "manzanas/manzana_resaltada_contornos.png"
```

### Ajustar parámetros de detección

Los rangos de color HSV pueden ajustarse según tus necesidades:

```python
# Para manzanas amarillas
lower_yellow = np.array([15, 40, 80])
upper_yellow = np.array([35, 255, 255])

# Para jitomates rojos
lower_red1 = np.array([0, 50, 50])
upper_red1 = np.array([10, 255, 255])
```

## 📝 Notas

- Las imágenes de entrada deben estar en formato JPG o PNG
- Los resultados se guardan automáticamente en las carpetas correspondientes
- El sistema está optimizado para condiciones de iluminación normales
- Para mejores resultados, asegúrate de que haya buen contraste entre las frutas y el fondo

## 🤝 Contribuciones

Este es un proyecto académico. Las contribuciones y sugerencias son bienvenidas.

## 📄 Licencia

Este proyecto es parte de un trabajo académico de maestría.

---

**Percepcion Computacional**: Trabajo de segmentación de imágenes en visión por computadora

