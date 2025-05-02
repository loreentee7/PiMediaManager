import tkinter as tk
from tkinter import ttk, Label, Frame, Scrollbar
from tkinter import PhotoImage
import os
import shutil
from PIL import Image, ImageTk # type: ignore

class Interface:
    def __init__(self, master):
        self.master = master
        self.master.title("PiMediaManager")
        self.master.geometry("900x700")
        self.master.configure(bg="#f0f0f0")  # Fondo gris claro
        self.selected_file = None
        self.selected_frame = None

        # Crear carpeta de almacenamiento si no existe
        self.storage_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../media_storage"))
        os.makedirs(self.storage_path, exist_ok=True)

        # Crear widgets
        self.create_widgets()

        # Cargar archivos automáticamente
        self.load_files()

    def create_widgets(self):
        # Encabezado
        header_frame = Frame(self.master, bg="#4CAF50", height=60)
        header_frame.pack(fill="x")

        header_label = Label(header_frame, text="PiMediaManager", font=("Arial", 24, "bold"), bg="#4CAF50", fg="white")
        header_label.pack(pady=10)

        # Botones de acción
        self.button_frame = Frame(self.master, bg="#f0f0f0")
        self.button_frame.pack(pady=10)

        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=5)

        self.cut_button = ttk.Button(self.button_frame, text="Cortar", command=self.cut_file)
        self.cut_button.grid(row=0, column=0, padx=5)

        self.copy_button = ttk.Button(self.button_frame, text="Copiar", command=self.copy_file)
        self.copy_button.grid(row=0, column=1, padx=5)

        self.paste_button = ttk.Button(self.button_frame, text="Pegar", command=self.paste_file)
        self.paste_button.grid(row=0, column=2, padx=5)

        self.delete_button = ttk.Button(self.button_frame, text="Eliminar", command=self.delete_file)
        self.delete_button.grid(row=0, column=3, padx=5)

        self.open_button = ttk.Button(self.button_frame, text="Abrir", command=self.open_selected_file)
        self.open_button.grid(row=0, column=4, padx=5)

        # Contenedor desplazable para los archivos
        self.canvas = tk.Canvas(self.master, bg="white", width=850, height=500, highlightthickness=0)
        self.scrollbar = Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas, bg="white")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.scrollbar.pack(side="right", fill="y")

    def explore_folders(self):
        # Método para explorar los archivos en la carpeta de almacenamiento
        from tkinter import Listbox, Scrollbar

        # Crear una nueva ventana para mostrar los archivos
        explore_window = tk.Toplevel(self.master)
        explore_window.title("Archivos Multimedia")
        explore_window.geometry("600x400")

        # Lista de archivos
        scrollbar = Scrollbar(explore_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        file_list = Listbox(explore_window, yscrollcommand=scrollbar.set, width=80, height=20)
        file_list.pack(side=tk.LEFT, fill=tk.BOTH)

        # Listar archivos en la carpeta de almacenamiento
        files = os.listdir(self.storage_path)
        for file in files:
            file_list.insert(tk.END, file)

        scrollbar.config(command=file_list.yview)

    def transfer_files(self):
        # Método para transferir archivos
        pass

    def preview_media(self):
        # Listar archivos en la carpeta de almacenamiento
        files = os.listdir(self.storage_path)
        if not files:
            print("No hay archivos para mostrar.")
            return

        # Seleccionar el primer archivo
        file_path = os.path.join(self.storage_path, files[0])

        # Mostrar imagen o video según el tipo de archivo
        if file_path.endswith((".jpg", ".png")):
            self.load_image(file_path)
        elif file_path.endswith((".mp4", ".avi")):
            self.load_video(file_path)

    def load_image(self, file_path):
        from PIL import Image, ImageTk # type: ignore

        # Cargar la imagen
        img = Image.open(file_path)
        img = img.resize((600, 400), Image.ANTIALIAS)  # Redimensionar para ajustarse al canvas
        self.img_tk = ImageTk.PhotoImage(img)  # Convertir a formato compatible con Tkinter

        # Mostrar la imagen en el canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)

    def load_video(self, file_path):
        import cv2 # type: ignore

        def play_video():
            cap = cv2.VideoCapture(file_path)
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # Convertir el frame de OpenCV (BGR) a un formato compatible con Tkinter (RGB)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (600, 400))
                img = Image.fromarray(frame)
                self.img_tk = ImageTk.PhotoImage(img)

                # Mostrar el frame en el canvas
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)
                self.master.update()  # Actualizar la interfaz gráfica

            cap.release()

        # Ejecutar la reproducción en un hilo separado para no bloquear la interfaz
        import threading
        threading.Thread(target=play_video).start()

    def load_files(self):
        # Limpiar el contenedor
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Lista para almacenar referencias a las imágenes
        self.image_references = []

        # Listar archivos en la carpeta de almacenamiento
        files = os.listdir(self.storage_path)
        if not files:
            Label(self.scrollable_frame, text="No hay archivos para mostrar.", bg="white", font=("Arial", 14)).grid(row=0, column=0, pady=20)
            return

        # Mostrar miniaturas en una cuadrícula
        row, col = 0, 0
        for file in files:
            file_path = os.path.join(self.storage_path, file)

            # Crear un marco para cada archivo
            file_frame = Frame(self.scrollable_frame, bg="#f9f9f9", padx=5, pady=5, relief="solid", bd=1)
            file_frame.grid(row=row, column=col, padx=10, pady=10)

            # Mostrar miniatura
            if file_path.endswith((".jpg", ".png")):
                try:
                    img = Image.open(file_path)
                    img.thumbnail((100, 100))  # Crear miniatura
                    img_tk = ImageTk.PhotoImage(img)

                    img_label = Label(file_frame, image=img_tk, bg="#f9f9f9")
                    img_label.image = img_tk  # Guardar referencia para evitar que se recolecte
                    img_label.pack()

                    # Guardar la referencia en la lista
                    self.image_references.append(img_tk)
                except Exception as e:
                    print(f"Error al cargar la miniatura de {file_path}: {e}")
            elif file_path.endswith((".mp4", ".avi")):
                # Mostrar un icono genérico para videos
                video_icon = Label(file_frame, text="🎥", font=("Arial", 24), bg="#f9f9f9")
                video_icon.pack()

            # Mostrar nombre del archivo
            file_label = Label(file_frame, text=file, bg="#f9f9f9", wraplength=100, font=("Arial", 10))
            file_label.pack()

            # Hacer clic para seleccionar el archivo
            for widget in file_frame.winfo_children():
                widget.bind("<Button-1>", lambda e, path=file_path, frame=file_frame: self.select_file(path, frame))

            # Cambiar de columna y fila
            col += 1
            if col >= 4:  # Cambiar a la siguiente fila después de 4 columnas
                col = 0
                row += 1

    def create_select_callback(self, file_path):
        def callback(event):
            self.select_file(file_path)
        return callback

    def select_file(self, file_path, file_frame):
        # Restablecer el color del marco previamente seleccionado
        if self.selected_frame and self.selected_frame.winfo_exists():
            self.selected_frame.config(bg="#f9f9f9")

        # Actualizar el archivo seleccionado y resaltar el marco
        self.selected_file = file_path
        self.selected_frame = file_frame
        self.selected_frame.config(bg="#cce5ff")  # Resaltar en azul claro

        # Imprimir el archivo seleccionado
        print(f"Archivo seleccionado: {self.selected_file}")

    def open_file(self, file_path):
        from PIL import Image # type: ignore
        import cv2 # type: ignore

        try:
            if file_path.endswith((".jpg", ".png")):
                # Abrir imagen
                img = Image.open(file_path)
                img.show()
            elif file_path.endswith((".mp4", ".avi")):
                # Reproducir video
                cap = cv2.VideoCapture(file_path)
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break

                    # Mostrar el frame
                    cv2.imshow("Video", frame)
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        break
                cap.release()
                cv2.destroyAllWindows()
        except Exception as e:
            print(f"Error al abrir el archivo {file_path}: {e}")

    def cut_file(self):
        # Seleccionar archivo para cortar
        if not self.selected_file:
            print("No se ha seleccionado ningún archivo.")
            return
        self.cut_path = self.selected_file
        print(f"Archivo seleccionado para cortar: {self.cut_path}")

    def copy_file(self):
        # Seleccionar archivo para copiar
        if not self.selected_file:
            print("No se ha seleccionado ningún archivo.")
            return
        self.copy_path = self.selected_file
        print(f"Archivo seleccionado para copiar: {self.copy_path}")

    def paste_file(self):
        # Pegar archivo cortado o copiado
        if hasattr(self, "cut_path") and self.cut_path:
            dest_path = os.path.join(self.storage_path, os.path.basename(self.cut_path))
            shutil.move(self.cut_path, dest_path)
            print(f"Archivo movido a: {dest_path}")
            del self.cut_path
        elif hasattr(self, "copy_path") and self.copy_path:
            dest_path = os.path.join(self.storage_path, os.path.basename(self.copy_path))
            shutil.copy(self.copy_path, dest_path)
            print(f"Archivo copiado a: {dest_path}")
        else:
            print("No hay archivo para pegar.")
        self.load_files()

    def delete_file(self):
        # Eliminar archivo seleccionado
        if not self.selected_file:
            print("No se ha seleccionado ningún archivo.")
            return
        os.remove(self.selected_file)
        print(f"Archivo eliminado: {self.selected_file}")
        self.selected_file = None
        self.selected_frame = None  # Restablecer el marco seleccionado
        self.load_files()

    def open_selected_file(self):
        if not self.selected_file:
            print("No se ha seleccionado ningún archivo.")
            return
        self.open_file(self.selected_file)

    def import_files(self):
        # Ruta donde se montará el teléfono
        phone_path = "/media/phone"

        # Verificar si el directorio existe
        if not os.path.exists(phone_path):
            print("El teléfono no está montado.")
            return

        # Copiar archivos desde el teléfono a la carpeta de la aplicación
        for file in os.listdir(phone_path):
            src = os.path.join(phone_path, file)
            dest = os.path.join(self.storage_path, file)
            shutil.copy(src, dest)
            print(f"Archivo importado: {file}")

        # Recargar los archivos en la interfaz
        self.load_files()

if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()
