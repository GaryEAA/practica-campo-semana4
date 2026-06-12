import tkinter as tk

# ─────────────────────────────────────────────────────────────
#  ALGORITMO DE BACKTRACKING
# ─────────────────────────────────────────────────────────────

def hanoi(n, origen, auxiliar, destino, movimientos):

    if n == 1:
        movimientos.append((origen, destino))
        return

    hanoi(n - 1, origen, destino, auxiliar, movimientos)
    movimientos.append((origen, destino))
    hanoi(n - 1, auxiliar, origen, destino, movimientos)

# ─────────────────────────────────────────────────────────────
#  INTERFAZ GRÁFICA
# ─────────────────────────────────────────────────────────────

class TorresHanoiApp:
    def __init__(self, root):

        self.root = root
        self.root.title("Torres de Hanoi - Backtracking")
        self.n_var = tk.IntVar(value=4)

        self.torres = []
        self.movimientos = []
        self.indice_movimiento = 0
        self.disco_animado = None
        self.posiciones_x = [150, 350, 550]

        self.BASE_Y = 300
        self.ALTURA_DISCO = 20
        self.Y_SUBIDA = 100

        self.colores = [
            "#E74C3C",
            "#F39C12",
            "#F1C40F",
            "#2ECC71",
            "#3498DB",
            "#9B59B6",
            "#1ABC9C",
            "#34495E"
        ]

        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="Número de discos:").pack(side="left")

        tk.Spinbox(
            frame,
            from_=1,
            to=8,
            width=5,
            textvariable=self.n_var
        ).pack(side="left", padx=10)

        tk.Button(
            frame,
            text="Iniciar",
            command=self._iniciar
        ).pack(side="left")

        self.lbl_movimientos = tk.Label(
            root,
            text=""
        )

        self.lbl_movimientos.pack()

        self.canvas = tk.Canvas(
            root,
            width=700,
            height=350,
            bg="white"
        )

        self.canvas.pack()

    def _dibujar(self):

        self.canvas.delete("all")

        self.canvas.create_line(
                50,
                300,
                650,
                300,
                width=4
            )

        for x in self.posiciones_x:

            self.canvas.create_line(
                x,
                100,
                x,
                300,
                width=6
            )

        for torre_idx, torre in enumerate(self.torres):

            x = self.posiciones_x[torre_idx]

            for nivel, disco in enumerate(torre):

                if (
                    self.disco_animado is not None
                    and torre_idx == self.disco_animado["origen"]
                    and nivel == 0
                ):
                    continue

                ancho = 30 + disco * 15

                y = self.BASE_Y - (
                    len(torre) - nivel
                ) * self.ALTURA_DISCO

                self.canvas.create_rectangle(
                    x - ancho,
                    y - 10,
                    x + ancho,
                    y + 10,
                    fill=self.colores[(disco - 1) % len(self.colores)],
                    outline="black"
                )


        if self.disco_animado is not None:

            disco = self.disco_animado["valor"]

            x = self.disco_animado["x"]

            y = self.disco_animado["y"]

            ancho = 30 + disco * 15

            self.canvas.create_rectangle(
                x - ancho,
                y - 10,
                x + ancho,
                y + 10,
                fill=self.colores[(disco - 1) % len(self.colores)],
                outline="black"
            )

    def _iniciar(self):
        n = self.n_var.get()

        self.torres = [
            list(range(1, n + 1)),
            [],
            []
        ]

        self.movimientos = []
        hanoi(
            n,
            0,
            1,
            2,
            self.movimientos
        )

        self.indice_movimiento = 0

        self.lbl_movimientos.config(
            text=f"Movimientos: 0 / {len(self.movimientos)}"
        )
        self._dibujar()
        self.root.after(
            700,
            self._siguiente_movimiento
        )

    def _siguiente_movimiento(self):

        if self.indice_movimiento >= len(self.movimientos):
            return

        origen, destino = self.movimientos[self.indice_movimiento]

        # Disco superior
        disco = self.torres[origen][0]

        x_inicial = self.posiciones_x[origen]
        x_final = self.posiciones_x[destino]

        y_inicial = self.BASE_Y - len(self.torres[origen]) * self.ALTURA_DISCO

        self.disco_animado = {
            "valor": disco,
            "origen": origen,
            "destino": destino,
            "x": x_inicial,
            "y": y_inicial,
            "x_final": x_final,
            "fase": "subir"
        }

        self._animar_movimiento()

    def _animar_movimiento(self):

        d = self.disco_animado

        if d["fase"] == "subir":

            if d["y"] > self.Y_SUBIDA:
                d["y"] -= 8

                self._dibujar()
                self.root.after(10, self._animar_movimiento)
                return
            d["fase"] = "horizontal"

        if d["fase"] == "horizontal":

            velocidad = 15

            if d["x"] < d["x_final"]:
                d["x"] += velocidad

            elif d["x"] > d["x_final"]:
                d["x"] -= velocidad

            if abs(d["x"] - d["x_final"]) <= velocidad:

                d["x"] = d["x_final"]
                d["fase"] = "bajar"

            self._dibujar()
            self.root.after(10, self._animar_movimiento)
            return

        if d["fase"] == "bajar":

            altura_destino = len(self.torres[d["destino"]])

            y_final = self.BASE_Y - len(self.torres[d["destino"]]) * self.ALTURA_DISCO

            if d["y"] < y_final:

                d["y"] += 8

                if d["y"] > y_final:
                    d["y"] = y_final

                self._dibujar()
                self.root.after(10, self._animar_movimiento)
                return

            d["y"] = y_final
            
            disco = self.torres[d["origen"]].pop(0)
            self.torres[d["destino"]].insert(0, disco)

            self.indice_movimiento += 1

            self.lbl_movimientos.config(
                text=f"Movimientos: {self.indice_movimiento} / {len(self.movimientos)}"
            )

            self.disco_animado = None

            self._dibujar()

            self.root.after(
                50,
                self._siguiente_movimiento
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = TorresHanoiApp(root)
    root.mainloop()