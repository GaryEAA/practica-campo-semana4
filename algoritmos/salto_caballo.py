import tkinter as tk
from tkinter import ttk, messagebox

# ─────────────────────────────────────────────────────────────
#  ALGORITMO DE BACKTRACKING
# ─────────────────────────────────────────────────────────────

MOVIMIENTOS_CABALLO = [
    (-2, -1), (-2, +1),
    (-1, -2), (-1, +2),
    (+1, -2), (+1, +2),
    (+2, -1), (+2, +1)
]

def salidas(tablero, f, c, n):
    count = 0
    for df, dc in MOVIMIENTOS_CABALLO:
        nf, nc = f + df, c + dc
        if 0 <= nf < n and 0 <= nc < n and tablero[nf][nc] == -1:
            count += 1
    return count
 
def resolver(n, fi, ci):
    tablero = [[-1] * n for _ in range(n)]
    tablero[fi][ci] = 1
 
    def backtrack(f, c, paso):
        if paso > n * n:
            return True
        candidatos = []
        for df, dc in MOVIMIENTOS_CABALLO:
            nf, nc = f + df, c + dc
            if 0 <= nf < n and 0 <= nc < n and tablero[nf][nc] == -1:
                candidatos.append((salidas(tablero, nf, nc, n), nf, nc))
        candidatos.sort()
        for _, nf, nc in candidatos:
            tablero[nf][nc] = paso
            if backtrack(nf, nc, paso + 1):
                return True
            tablero[nf][nc] = -1
        return False
 
    return tablero if backtrack(fi, ci, 2) else None
 
# ─────────────────────────────────────────────────────────────
#  INTERFAZ GRÁFICA
# ─────────────────────────────────────────────────────────────
class SaltoCaballoApp:
    CELDA    = 70
    CLARA    = "#F0D9B5"
    OSCURA   = "#B58863"
    INICIO   = "#3498DB"
    ACTUAL   = "#E74C3C"
    VISITADA = "#2ECC71"
    FONDO    = "#1E2A3A"
    TEXTO    = "#ECF0F1"
 
    def __init__(self, root):
        self.root     = root
        self.root.title("Salto del Caballo")
        self.root.configure(bg=self.FONDO)
        self.root.resizable(False, False)
        self.n        = 5
        self.fi       = 0
        self.ci       = 0
        self.solucion = None
        self.secuencia= []
        self.paso     = 0
        self.animando = False
        self.pausado  = False
        self.after_id = None
        self.esperando_click = False
        self._ui()
        self._dibujar_inicio()
 
    def _ui(self):
        tk.Label(self.root, text="♞  Salto del Caballo",
                 font=("Helvetica", 18, "bold"),
                 bg=self.FONDO, fg=self.TEXTO).pack(pady=(16, 6))
 
        ctrl = tk.Frame(self.root, bg=self.FONDO)
        ctrl.pack()
 
        tk.Label(ctrl, text="Tablero n×n:", bg=self.FONDO,
                 fg=self.TEXTO, font=("Helvetica", 11)).grid(row=0, column=0, padx=8)
 
        self.spin = tk.Spinbox(ctrl, from_=5, to=8, width=4,
                               font=("Helvetica", 12, "bold"), justify="center",
                               command=self._cambiar_tablero)
        self.spin.delete(0, "end")
        self.spin.insert(0, "5")
        self.spin.grid(row=0, column=1, padx=8)
 
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(padx=20, pady=12)
        self.canvas.bind("<Button-1>", self._click)
 
        btns = tk.Frame(self.root, bg=self.FONDO)
        btns.pack(pady=4)
 
        def btn(texto, color, cmd, col):
            b = tk.Button(btns, text=texto, font=("Helvetica", 10, "bold"),
                          bg=color, fg="white", relief="flat",
                          padx=10, pady=6, cursor="hand2", command=cmd)
            b.grid(row=0, column=col, padx=4)
            return b
 
        self.btn_click = btn("📍 Elegir inicio", "#2980B9", self._activar_click, 0)
        self.btn_animar = btn("▶ Animar",      "#27AE60", self._animar,      1)
        self.btn_paso   = btn("⏭ Paso a paso", "#E67E22", self._paso_a_paso, 2)
        self.btn_stop   = btn("⏸ Pausar",      "#E74C3C", self._toggle_pausa, 3)
        self.btn_limpiar= btn("🗑 Limpiar",     "#566573", self._limpiar,     4)
 
        self.btn_stop.config(state="disabled")
 
        self.lbl = tk.Label(self.root, text="Presiona ▶ Animar o ⏭ Paso a paso",
                            font=("Helvetica", 11), bg=self.FONDO, fg="#F39C12")
        self.lbl.pack(pady=(4, 16))
  
    def _dibujar_inicio(self):
        """Tablero vacío con el caballo en la casilla (0,0) sin resolver."""
        self.solucion = None
        self.secuencia = []
        self.paso = 0
        self._dibujar_tablero_base(marcar_inicio=True)
        self.lbl.config(text="Presiona ▶ Animar o ⏭ Paso a paso")
 
    def _dibujar_tablero_base(self, marcar_inicio=False):
        c = self.CELDA
        n = self.n
        self.canvas.config(width=c * n, height=c * n)
        self.canvas.delete("all")
        for f in range(n):
            for col in range(n):
                x0, y0 = col * c, f * c
                color = self.CLARA if (f + col) % 2 == 0 else self.OSCURA
                self.canvas.create_rectangle(x0, y0, x0+c, y0+c,
                                             fill=color, outline="#111", width=1)
                if marcar_inicio and f == self.fi and col == self.ci:
                    self.canvas.create_rectangle(x0, y0, x0+c, y0+c,
                                                 fill=self.INICIO, outline="#111", width=1)
                    self.canvas.create_text(x0+c//2, y0+c//2,
                                            text="♞", fill="white",
                                            font=("Helvetica", 20))
  
    def _cambiar_tablero(self):
        self._cancelar_animacion()
        try:
            self.n = max(5, min(8, int(self.spin.get())))
        except ValueError:
            self.n = 5
        self.fi, self.ci = 0, 0
        self.pausado = False
        self._resetear_botones()
        self._dibujar_inicio()
 
    def _limpiar(self):
        self._cancelar_animacion()
        self.fi, self.ci = 0, 0
        self.pausado = False
        self._resetear_botones()
        self._dibujar_inicio()
  
    def _resolver_si_necesario(self):
        if self.solucion:
            return True
        self.solucion = resolver(self.n, self.fi, self.ci)
        if not self.solucion:
            messagebox.showerror("Sin solución",
                                 f"No hay recorrido desde ({self.fi},{self.ci}).\n"
                                 "Elige otra casilla de inicio.")
            return False
        self.secuencia = sorted(
            (self.solucion[f][c], f, c)
            for f in range(self.n) for c in range(self.n)
        )
        return True
  
    def _activar_click(self):
        self._cancelar_animacion()
        self.pausado = False
        self.esperando_click = True
        self.btn_click.config(text="Haz clic en el tablero...", bg="#C0392B")
        self.btn_animar.config(state="disabled")
        self.btn_paso.config(state="disabled")
        self.lbl.config(text="Selecciona la casilla de inicio")
 
    def _click(self, event):
        if not self.esperando_click:
            return
        col = event.x // self.CELDA
        fila = event.y // self.CELDA
        if 0 <= fila < self.n and 0 <= col < self.n:
            self.fi, self.ci = fila, col
            self.solucion = None
            self.secuencia = []
            self.paso = 0
            self.esperando_click = False
            self.btn_click.config(text="📍 Elegir inicio", bg="#2980B9")
            self._resetear_botones()
            self._dibujar_tablero_base(marcar_inicio=True)
            self.lbl.config(text=f"Inicio en ({self.fi},{self.ci}) · Presiona ▶ o ⏭")
  
    def _animar(self):
        if not self._resolver_si_necesario():
            return
        if self.pausado:
            self.pausado = False
            self.animando = True
            self.btn_stop.config(text="⏸ Pausar", state="normal")
            self.btn_click.config(state="disabled")
            self.btn_animar.config(state="disabled")
            self.btn_paso.config(state="disabled")
            self._tick()
            return
        self.paso = 0
        self.animando = True
        self.pausado = False
        self.btn_stop.config(text="⏸ Pausar", state="normal")
        self.btn_click.config(state="disabled")
        self.btn_animar.config(state="disabled")
        self.btn_paso.config(state="disabled")
        self._tick()
 
    def _tick(self):
        if not self.animando:
            return
        if self.paso >= self.n * self.n:
            self.animando = False
            self.btn_stop.config(state="disabled")
            self._resetear_botones()
            self.lbl.config(text=f"✅ Completado · {self.n*self.n} casillas")
            return
        self.paso += 1
        self._dibujar(self.paso)
        self.lbl.config(text=f"Paso: {self.paso} / {self.n*self.n}")
        self.after_id = self.root.after(300, self._tick)
 
    def _toggle_pausa(self):
        if self.animando:
            self.animando = False
            self.pausado = True
            if self.after_id:
                self.root.after_cancel(self.after_id)
            self.btn_stop.config(text="▶ Continuar")
            self.btn_animar.config(state="normal")
            self.lbl.config(text=f"Pausado en paso {self.paso} / {self.n*self.n}")
        elif self.pausado:
            self.pausado = False
            self.animando = True
            self.btn_stop.config(text="⏸ Pausar")
            self.btn_animar.config(state="disabled")
            self._tick()
 
    def _paso_a_paso(self):
        if not self._resolver_si_necesario():
            return
        if self.animando:
            return
        total = self.n * self.n
        if self.paso < total:
            self.paso += 1
            self._dibujar(self.paso)
            self.lbl.config(text=f"Paso: {self.paso} / {total}")
            if self.paso == total:
                self.lbl.config(text=f"✅ Completado · {total} casillas")
        else:
            messagebox.showinfo("Completado", f"¡{total} casillas recorridas!")
 
    def _cancelar_animacion(self):
        self.animando = False
        if self.after_id:
            self.root.after_cancel(self.after_id)
 
    def _resetear_botones(self):
        self.btn_click.config(state="normal",  text="📍 Elegir inicio", bg="#2980B9")
        self.btn_animar.config(state="normal")
        self.btn_paso.config(state="normal")
        self.btn_stop.config(state="disabled", text="⏸ Pausar")
  
    def _dibujar(self, hasta):
        c = self.CELDA
        n = self.n
        self.canvas.config(width=c * n, height=c * n)
        self.canvas.delete("all")
 
        visibles = {}
        if self.solucion:
            for paso, f, col in self.secuencia:
                if paso <= hasta:
                    visibles[paso] = (f, col)
 
        for f in range(n):
            for col in range(n):
                x0, y0 = col * c, f * c
                x1, y1 = x0 + c, y0 + c
                p = self.solucion[f][col] if self.solucion else -1
 
                if p == -1 or p > hasta:
                    color = self.CLARA if (f + col) % 2 == 0 else self.OSCURA
                elif p == 1:
                    color = self.INICIO
                elif p == hasta:
                    color = self.ACTUAL
                else:
                    color = self.VISITADA
 
                self.canvas.create_rectangle(x0, y0, x1, y1,
                                             fill=color, outline="#111", width=1)
                if p != -1 and p <= hasta:
                    self.canvas.create_text(x0 + c//2, y0 + c//2,
                                            text=str(p), fill="white",
                                            font=("Helvetica", 11, "bold"))
                if p == hasta and hasta > 0:
                    self.canvas.create_text(x0 + c//2, y0 + c//2 - 10,
                                            text="♞", fill="white",
                                            font=("Helvetica", 20))
 
        if hasta >= 2 and self.solucion:
            p_ant = visibles.get(hasta - 1)
            p_act = visibles.get(hasta)
            if p_ant and p_act:
                self.canvas.create_line(
                    p_ant[1]*c + c//2, p_ant[0]*c + c//2,
                    p_act[1]*c + c//2, p_act[0]*c + c//2,
                    fill="white", width=2, arrow=tk.LAST, dash=(4,2)
                )

if __name__ == "__main__":
    root = tk.Tk()
    app = SaltoCaballoApp(root)
    root.mainloop()