from PIL import Image, ImageTk
import cv2
import os
import tkinter as tk

def preview_image(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"El archivo {image_path} no existe.")
    
    image = Image.open(image_path)
    image.thumbnail((400, 400))  # Redimensionar la imagen
    return ImageTk.PhotoImage(image)

def preview_video(video_path, root):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"El archivo {video_path} no existe.")
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"No se puede abrir el video {video_path}.")
    
    def show_frame():
        ret, frame = cap.read()
        if ret:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            img = ImageTk.PhotoImage(img)
            label.imgtk = img
            label.configure(image=img)
            label.after(10, show_frame)
        else:
            cap.release()

    label = tk.Label(root)
    label.pack()
    show_frame()