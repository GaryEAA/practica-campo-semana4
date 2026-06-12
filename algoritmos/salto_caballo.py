import tkinter as tk

# ─────────────────────────────────────────────────────────────
#  ALGORITMO DE BACKTRACKING
# ─────────────────────────────────────────────────────────────

# TODO: implementar el algoritmo de backtracking para el salto del caballo

# ─────────────────────────────────────────────────────────────
#  INTERFAZ GRÁFICA
# ─────────────────────────────────────────────────────────────

class SaltoCaballoApp:
    """Ventana con tablero animado del Salto del Caballo."""

    def __init__(self, root):
        self.root = root
        self.root.title("Salto del Caballo – Backtracking")

        # TODO: construir la interfaz (canvas tablero, botones, controles)

    def _dibujar(self):
        """Dibuja el tablero y el recorrido hasta el paso actual."""
        # TODO: implementar el dibujo del tablero de ajedrez
        pass

    def _iniciar_animacion(self):
        """Anima el recorrido del caballo casilla por casilla."""
        # TODO: implementar la animación
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = SaltoCaballoApp(root)
    root.mainloop()