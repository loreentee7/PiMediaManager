# main.py

import tkinter as tk
from gui.interface import Interface

def main():
    root = tk.Tk()
    root.title("PiMediaManager")
    app = Interface(root)
    root.mainloop()

if __name__ == "__main__":
    main()