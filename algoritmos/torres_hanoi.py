import tkinter as tk

# ─────────────────────────────────────────────────────────────
#  ALGORITMO DE BACKTRACKING
# ─────────────────────────────────────────────────────────────

# TODO: implementar el algoritmo de backtracking para las Torres de Hanoi

# ─────────────────────────────────────────────────────────────
#  INTERFAZ GRÁFICA
# ─────────────────────────────────────────────────────────────

class TorresHanoiApp:
    """Ventana con animación de Torres de Hanoi."""

    def __init__(self, root):
        self.root = root
        self.root.title("Torres de Hanoi – Backtracking")

        # TODO: construir la interfaz (canvas, botones, controles)

    def _dibujar(self):
        """Dibuja el estado actual de las tres torres en el canvas."""
        # TODO: implementar el dibujo de torres y discos
        pass

    def _iniciar_animacion(self):
        """Reproduce los movimientos uno a uno con animación."""
        # TODO: implementar la animación paso a paso
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = TorresHanoiApp(root)
    root.mainloop()