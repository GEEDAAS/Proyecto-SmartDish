
# 🐾 SmartDish - Dispensador Inteligente para Mascotas

**SmartDish** es un proyecto universitario desarrollado para la materia de **Sistemas Programables**. Consiste en un dispensador automático de comida y agua para mascotas pequeñas, controlado por una ESP32, una cámara ESP32-CAM, sensores, actuadores y un modelo de inteligencia artificial para el reconocimiento visual.

---

## 📌 Descripción General

SmartDish está diseñado para ofrecer una solución automatizada y eficiente para el cuidado de mascotas. Utiliza:

- Una **ESP32** para controlar los componentes físicos (servomotor, bomba de agua mediante relevador, sensores y LEDs).
- Una **ESP32-CAM** para capturar imágenes y detectar la presencia de la mascota.
- Un modelo de **IA basado en YOLOv5** para el reconocimiento visual (actualmente entrenado para detectar perros).
- Una **interfaz web** desarrollada en HTML y JavaScript para interactuar con el sistema.

---

## 🧠 Características

- 🥣 Dispensación automática de alimento y agua  
- 💡 Control de tres LEDs (verde, rojo y azul)  
- 🌡️ Monitoreo ambiental con sensores (LDR, DHT11, celda de carga)  
- 📷 Captura de imagen y análisis con IA para detectar mascotas  
- 🔐 Registro e inicio de sesión de usuarios (Google o correo/contraseña)  
- 🌐 Interfaz de usuario accesible desde navegador con XAMPP  
- ⚡ Control seguro de la bomba mediante **relevador de 12V**

---

## 📁 Estructura del Repositorio

```
Proyecto-SmartDish/
│
├── Codigos py/             # Código para el control físico (ESP32 y ESP32-CAM)
│   ├── esp32_control.py    # Control del servomotor, bomba, sensores y LEDs
│   ├── esp32cam.py         # Captura de imágenes y envío a la IA
│   └── boot.py             # Configuración de red para la ESP32-CAM
│
├── SmartDish_IA/           # IA para reconocimiento de imágenes
│   └── model/              # Contiene el modelo YOLOv5 (requiere clonar)
│
├── SmartDish/              # Página web y sistema de usuario
│   └── (colocar en htdocs de XAMPP para ejecución)
│
└── README.md               # Este archivo
```

---

## ⚙️ Requisitos

### 🧰 Hardware
- ESP32  
- ESP32-CAM  
- Relevador de 12V para la bomba de agua  
- Bomba de agua  
- Servomotor  
- LEDs (verde, rojo, azul)  
- LDR, DHT11, celda de carga  

### 💻 Software
- Python 3  
- Librerías: OpenCV, requests, flask, etc.  
- XAMPP  
- YOLOv5 (clonar desde [ultralytics/yolov5](https://github.com/ultralytics/yolov5))  

---

## 🚀 Instrucciones de Uso

### 1. Clonar el Repositorio

```bash
git clone https://github.com/GEEDAAS/Proyecto-SmartDish.git
```

### 2. Configurar la Carpeta `SmartDish_IA/`

```bash
cd Proyecto-SmartDish/SmartDish_IA/model
git clone https://github.com/ultralytics/yolov5
```

> Se recomienda crear un entorno virtual con `venv` dentro de `SmartDish_IA`.

### 3. Subir Código a ESP32 y ESP32-CAM

- Cargar el código correspondiente desde `Codigos py/` usando Arduino IDE o Thonny.

### 4. Configurar la Página Web

- Mover la carpeta `SmartDish/` a la carpeta `htdocs` de XAMPP.  
- Iniciar Apache desde el panel de XAMPP.

### 5. Acceder a la Interfaz

- Abrir el navegador y acceder a `http://localhost/SmartDish/`.

---

## 👨‍🎓 Proyecto Académico

Desarrollado por estudiantes de **Ingeniería** para la materia de **Sistemas Programables**. Este proyecto busca demostrar el uso integrado de microcontroladores, sensores, actuadores, visión artificial y desarrollo web en una solución real y funcional.

---

## 🤝 Contribuciones

Las contribuciones al proyecto son bienvenidas. Por favor abre un *pull request* con tus sugerencias o mejoras.

---

## 📄 Licencia

Este proyecto es de uso académico. Para usos comerciales o externos, se requiere permiso explícito de los autores.
