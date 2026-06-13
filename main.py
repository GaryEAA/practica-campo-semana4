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

# --------------------------------------------------
# MENÚ PRINCIPAL
# --------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Práctica de Campo – Semana 4")
    root.geometry("500x300")
    root.configure(bg="#E8F0FE")

    titulo = tk.Label(
        root,
        text="ALGORITMOS DE BACKTRACKING",
        font=("Arial", 16, "bold"),
        bg="#E8F0FE"
    )
    titulo.pack(pady=30)

    btn_hanoi = tk.Button(
        root,
        text="Torres de Hanoi",
        font=("Arial", 12),
        width=20,
        height=2,
        bg="#4CAF50",
        fg="white",
        command=lambda: lanzar_algoritmo("torres_hanoi.py")
    )
    btn_hanoi.pack(pady=10)

    btn_caballo = tk.Button(
        root,
        text="Salto del Caballo",
        font=("Arial", 12),
        width=20,
        height=2,
        bg="#2196F3",
        fg="white",
        command=lambda: lanzar_algoritmo("salto_caballo.py")
    )
    btn_caballo.pack(pady=10)

    root.mainloop()