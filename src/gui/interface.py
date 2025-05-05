import tkinter as tk
from tkinter import ttk, Label, Frame, Scrollbar
from tkinter import PhotoImage
from tkinter import font  # Importar para personalizar la fuente
import os
import shutil
from PIL import Image, ImageTk
import cv2

class Interface:
    def __init__(self, master):
        self.master = master
        self.master.title("PiMediaManager")
        self.master.geometry("900x750")  # Incrementar la altura de 700 a 750
        self.master.configure(bg="#f0f0f0")  # Fondo gris claro
        self.selected_file = None
        self.selected_frame = None
        self.selected_files = []

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

        header_label = Label(header_frame, text="Alejandro Avila", font=("Arial", 20, "bold"), bg="#4CAF50", fg="white")
        header_label.pack(pady=10)

        # Botones de acción
        self.button_frame = Frame(self.master, bg="#f0f0f0")    
        self.button_frame.pack(pady=10)

        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=5)

        self.create_folder_button = ttk.Button(self.button_frame, text="Crear Carpeta", command=self.create_folder)
        self.create_folder_button.grid(row=0, column=6, padx=5)

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

        self.import_button = ttk.Button(self.button_frame, text="Importar", command=self.import_files)
        self.import_button.grid(row=0, column=5, padx=5)

        # Contenedor desplazable para los archivos
        self.canvas = tk.Canvas(self.master, bg="white", width=850, height=500, highlightthickness=0)
        self.scrollbar = Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas, bg="white")

        # Asociar el evento de configuración del canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Crear ventana dentro del canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Empaquetar el canvas y el scrollbar
        self.canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.scrollbar.pack(side="right", fill="y")

        # Footer container para el texto
        footer_frame = Frame(self.master, bg="#f0f0f0")
        footer_frame.pack(side="bottom", fill="x")  # Colocar al final de la ventana

        # Texto en la parte inferior
        pixel_font = font.Font(family="Courier", size=10, weight="bold")  # Fuente estilo pixel
        footer_label = Label(
            footer_frame,
            text="Designed by Lorente ❤️",
            font=pixel_font,
            bg="#f0f0f0",  # Fondo gris claro
            fg="#333333"   # Color del texto
        )
        footer_label.pack(pady=5)  # Añadir un pequeño margen

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
        if file_path.endswith((".jpg", ".png", ".JPG", ".PNG")):
            self.load_image(file_path)
        elif file_path.endswith((".mp4", ".avi")):
            self.load_video(file_path)

    def load_image(self, file_path):
        from PIL import Image, ImageTk 

        # Cargar la imagen
        img = Image.open(file_path)
        img = img.resize((600, 400), Image.ANTIALIAS)  # Redimensionar para ajustarse al canvas
        self.img_tk = ImageTk.PhotoImage(img)  # Convertir a formato compatible con Tkinter

        # Mostrar la imagen en el canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)

    def load_video(self, file_path):
        import cv2 

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

        # Mostrar botón para volver a la carpeta anterior si no estamos en la raíz
        if self.storage_path != os.path.abspath(os.path.join(os.path.dirname(__file__), "../media_storage")):
            back_button = Frame(self.scrollable_frame, bg="#e0e0e0", padx=2, pady=2, relief="solid", bd=1)
            back_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
            back_label = Label(back_button, text="🔙 Volver", font=("Arial", 8, "bold"), bg="#e0e0e0")
            back_label.pack()
            # Asociar el evento de clic al marco completo
            back_button.bind("<Button-1>", lambda e: self.go_back())

        # Listar carpetas y archivos en la carpeta actual
        items = os.listdir(self.storage_path)
        if not items:
            Label(self.scrollable_frame, text="No hay archivos o carpetas para mostrar.", bg="white", font=("Arial", 14)).grid(row=1, column=0, pady=20)
            return

        # Mostrar carpetas y archivos en una cuadrícula
        row, col = 1, 0
        for item in items:
            item_path = os.path.join(self.storage_path, item)

            # Crear un marco para cada archivo o carpeta
            item_frame = Frame(self.scrollable_frame, bg="#f9f9f9", padx=5, pady=5, relief="solid", bd=1)
            item_frame.grid(row=row, column=col, padx=10, pady=10)

            # Hacer que todo el marco sea interactivo
            if os.path.isdir(item_path):
                folder_icon = Label(item_frame, text="📁", font=("Arial", 24), bg="#f9f9f9")
                folder_icon.pack()
                # Mostrar el nombre de la carpeta
                item_label = Label(item_frame, text=item, bg="#f9f9f9", wraplength=100, font=("Arial", 10))
                item_label.pack()
            elif item_path.endswith((".jpg", ".png", ".JPG", ".PNG")):
                try:
                    img = Image.open(item_path)
                    img.thumbnail((100, 100))  # Crear miniatura
                    img_tk = ImageTk.PhotoImage(img)

                    img_label = Label(item_frame, image=img_tk, bg="#f9f9f9")
                    img_label.image = img_tk  # Guardar referencia para evitar que se recolecte
                    img_label.pack()

                    # Guardar la referencia en la lista
                    self.image_references.append(img_tk)
                except Exception as e:
                    print(f"Error al cargar la miniatura de {item_path}: {e}")
            elif item_path.endswith((".mp4", ".avi")):
                video_icon = Label(item_frame, text="🎥", font=("Arial", 24), bg="#f9f9f9")
                video_icon.pack()

            # Mostrar nombre del archivo
            if not os.path.isdir(item_path):
                item_label = Label(item_frame, text=item, bg="#f9f9f9", wraplength=100, font=("Arial", 10))
                item_label.pack()

            # Asociar el evento de selección al marco completo y a sus hijos
            def bind_selection(widget, path=item_path, frame=item_frame):
                widget.bind("<Button-1>", lambda e: self.select_file(path, frame))

            bind_selection(item_frame)  # Asociar al marco
            for child in item_frame.winfo_children():  # Asociar a todos los hijos del marco
                bind_selection(child)

            # Cambiar de columna y fila
            col += 1
            if col >= 4:  # Cambiar a la siguiente fila después de 4 columnas
                col = 0
                row += 1

    def create_select_callback(self, file_path):
        def callback(event):
            self.select_file(file_path)
        return callback

    def create_enter_folder_callback(self, folder_path):
        def callback(event):
            self.enter_folder(folder_path)
        return callback

    def select_file(self, file_path, file_frame):
        # Si el archivo ya está seleccionado, deseleccionarlo
        if file_path in self.selected_files:
            self.selected_files.remove(file_path)
            file_frame.config(bg="#f9f9f9")  # Restaurar el color original
        else:
            # Si no está seleccionado, agregarlo a la lista
            self.selected_files.append(file_path)
            file_frame.config(bg="#cce5ff")  # Resaltar en azul claro

        # Imprimir la lista de archivos seleccionados
        print(f"Archivos seleccionados: {self.selected_files}")

    def open_file(self, file_path):
        from PIL import Image 
        import cv2 

        try:
            if file_path.endswith((".jpg", ".JPG",".png", ".PNG")):
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
        # Verificar si hay archivos o carpetas seleccionados
        if not self.selected_files:
            print("No se han seleccionado archivos o carpetas.")
            return

        try:
            for file_path in self.selected_files:
                if os.path.isdir(file_path):
                    # Eliminar carpeta y su contenido
                    shutil.rmtree(file_path)
                    print(f"Carpeta eliminada: {file_path}")
                else:
                    # Eliminar archivo
                    os.remove(file_path)
                    print(f"Archivo eliminado: {file_path}")
            
            # Restablecer selección
            self.selected_files = []
            self.load_files()  # Recargar la interfaz
        except Exception as e:
            print(f"Error al eliminar los archivos o carpetas: {e}")

    def open_selected_file(self):
        if not self.selected_files:
            print("No se ha seleccionado ningún archivo o carpeta.")
            return

        # Abrir el primer elemento seleccionado
        selected_path = self.selected_files[0]
        if os.path.isdir(selected_path):
            # Si es una carpeta, entrar en ella
            self.enter_folder(selected_path)
        else:
            # Si es un archivo, abrirlo
            self.open_file(selected_path)

    def import_files(self):
        from tkinter import filedialog

        # Abrir un cuadro de diálogo para seleccionar múltiples archivos
        file_paths = filedialog.askopenfilenames(
            title="Selecciona las fotos o videos",
            filetypes=[("Imágenes y Videos", "*.jpg *.png *.mp4 *.avi"), ("Todos los archivos", "*.*")]
        )

        if not file_paths:
            print("No se seleccionaron archivos.")
            return

        # Copiar los archivos seleccionados al directorio de media_storage
        for file_path in file_paths:
            dest = os.path.join(self.storage_path, os.path.basename(file_path))

            # Verificar si es un archivo válido (por ejemplo, imágenes o videos)
            if os.path.isfile(file_path) and file_path.lower().endswith((".jpg", ".JPG",".png", ".PNG", ".mp4", ".avi")):
                shutil.copy(file_path, dest)
                print(f"Archivo importado: {os.path.basename(file_path)}")

        # Recargar los archivos en la interfaz
        self.load_files()
        print("Importación completada.")

    def create_folder(self):
        from tkinter.simpledialog import askstring

        # Pedir al usuario el nombre de la carpeta
        folder_name = askstring("Crear Carpeta", "Introduce el nombre de la nueva carpeta:")
        if not folder_name:
            print("No se ingresó ningún nombre para la carpeta.")
            return

        # Crear la carpeta en la ubicación actual
        folder_path = os.path.join(self.storage_path, folder_name)
        try:
            os.makedirs(folder_path)
            print(f"Carpeta creada: {folder_path}")
            self.load_files()  # Recargar la interfaz
        except Exception as e:
            print(f"Error al crear la carpeta: {e}")

    def enter_folder(self, folder_path):
        # Cambiar la ruta actual a la carpeta seleccionada
        self.storage_path = folder_path
        self.load_files()

    def go_back(self):
        # Volver a la carpeta anterior
        self.storage_path = os.path.dirname(self.storage_path)
        self.load_files()

if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()
