# main.py

import tkinter as tk
from gui.interface import Interface

def open_importer():
    """Abre el importador de fotos."""
    root = tk.Tk()
    app = Importer(root)
    root.mainloop()

def open_interface():
    """Abre la interfaz principal."""
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()

def main():
    open_interface()  # Luego abre la interfaz principal

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()