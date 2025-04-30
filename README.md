# PiMediaManager 📂🎞️

**PiMediaManager** es una aplicación ligera escrita en Python diseñada para la Raspberry Pi Zero 2. Su propósito es actuar como un gestor de archivos multimedia (fotos y videos), permitiendo mover, copiar, cortar, pegar, previsualizar y transferir contenido entre la Raspberry y otros dispositivos como teléfonos móviles.

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
- Tkinter o PySimpleGUI (para la interfaz gráfica)
- Pillow / OpenCV (para previsualización)
- os, shutil (para manipulación de archivos)
- Flask o Samba (opcional, para compartir por red)
- go-mtpfs o alternativa (opcional, para MTP vía USB)

---

## 💡 Requisitos

- Raspberry Pi Zero 2 W (recomendado con Raspbian Lite o Desktop)
- Python 3.x instalado
- Dependencias (instalables vía `pip`)
- Accesorios: cable OTG, lector USB o red Wi-Fi

---

## 📦 Instalación

```bash
git clone https://github.com/tu_usuario/PiMediaManager.git
cd PiMediaManager
pip install -r requirements.txt
python main.py
