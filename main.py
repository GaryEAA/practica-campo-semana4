import tkinter as tk
import subprocess
import sys
import os

BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
ALGORITMOS_DIR = os.path.join(BASE_DIR, "algoritmos")


def lanzar_algoritmo(nombre_archivo):
    """Abre el algoritmo en una ventana independiente."""
    ruta = os.path.join(ALGORITMOS_DIR, nombre_archivo)
    subprocess.Popen([sys.executable, ruta])


# TODO: construir la ventana del menú principal con tkinter
#       - Botón → Torres de Hanoi    (llama a lanzar_algoritmo("torres_hanoi.py"))
#       - Botón → Salto del Caballo  (llama a lanzar_algoritmo("salto_caballo.py"))


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Práctica de Campo – Semana 4")
    root.geometry("500x300")

    # TODO: reemplazar este label por el menú completo
    tk.Label(root, text="Menú Principal – por implementar").pack(expand=True)

    root.mainloop()