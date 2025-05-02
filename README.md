# PiMediaManager 📂🎞️

**PiMediaManager** es una aplicación ligera escrita en Python diseñada para la Raspberry Pi Zero 2. Su propósito es actuar como un gestor de archivos multimedia (fotos y videos), permitiendo mover, copiar, cortar, pegar, previsualizar y transferir contenido entre la Raspberry y otros dispositivos como teléfonos móviles.

Esta desarrollado para un amigo el cual me pidio un gestor de archivos y fotos...

---

## 🚀 Funcionalidades

- 📁 Exploración de carpetas
- ✂️ Mover, copiar, cortar y pegar fotos y videos
- 🖼️ Previsualización rápida de imágenes y videos
- 🔗 Conexión con teléfonos móviles para transferencias
- 💾 Uso de la Raspberry Pi como disco duro multimedia

---

## 🛠️ Tecnologías utilizadas

- Python 3
- Tkinter (para la interfaz gráfica)
- Pillow / OpenCV (para previsualización)
- os, shutil (para manipulación de archivos)
- go-mtpfs o alternativa (opcional, para MTP vía USB)

---

## 💡 Requisitos

- Raspberry Pi Zero 2 W (recomendado con Raspbian Lite o Desktop)
- Python 3.x instalado
- Dependencias (instalables vía `pip`)
- Accesorios: cable OTG, lector USB o red Wi-Fi

---

## 📦 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/loreentee7/PiMediaManager.git
cd PiMediaManager
```

### 2. Instalar Python y Pip
Si estás en una Raspberry Pi o en un sistema basado en Linux, Python y Pip ya deberían estar instalados. Si no, instálalos con:
```bash
sudo apt update
sudo apt install python3 python3-pip
```

En Windows, descarga Python desde [python.org](https://www.python.org/downloads/) y asegúrate de marcar la opción **"Add Python to PATH"** durante la instalación.

### 3. Instalar las dependencias
Ejecuta el siguiente comando para instalar las bibliotecas necesarias:
```bash
pip3 install pillow opencv-python
```

Si estás en una Raspberry Pi, también instala las siguientes dependencias del sistema para manejar videos:
```bash
sudo apt install libatlas-base-dev ffmpeg
```

### 4. Ejecutar la aplicación
Navega al directorio del proyecto y ejecuta la aplicación con:
```bash
python3 src/main.py
```

---

## Opcional: Configurar la aplicación en Raspberry Pi

### Crear un acceso directo en el escritorio
1. Crea un archivo `.desktop` en el escritorio:
   ```bash
   nano ~/Desktop/PiMediaManager.desktop
   ```
2. Agrega el siguiente contenido:
   ```ini
   [Desktop Entry]
   Name=PiMediaManager
   Comment=Gestor de fotos y videos
   Exec=python3 /ruta/a/tu/proyecto/src/main.py
   Icon=utilities-terminal
   Terminal=false
   Type=Application
   ```
   Reemplaza `/ruta/a/tu/proyecto` con la ruta real del proyecto.

3. Haz que el archivo sea ejecutable:
   ```bash
   chmod +x ~/Desktop/PiMediaManager.desktop
   ```

### Ejecutar la aplicación al iniciar la Raspberry Pi
1. Edita el archivo de autoinicio:
   ```bash
   nano ~/.config/lxsession/LXDE-pi/autostart
   ```
2. Agrega la siguiente línea al final del archivo:
   ```bash
   @python3 /ruta/a/tu/proyecto/src/main.py
   ```

---

## Problemas comunes

### Error: `ModuleNotFoundError: No module named 'tkinter'`
Instala `tkinter` con:
```bash
sudo apt install python3-tk
```

### Error: `cv2.error` al reproducir videos
Asegúrate de tener `ffmpeg` instalado:
```bash
sudo apt install ffmpeg
```

---

## Contribuciones

Si deseas contribuir al proyecto, por favor abre un issue o envía un pull request.

---

## Licencia

Este proyecto está bajo la licencia MIT.
