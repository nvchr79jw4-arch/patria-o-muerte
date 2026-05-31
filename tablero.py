# tablero.py
# ─────────────────────────────────────────────────────────────
#  PATRIA O MUERTE — El juego de cartas
#  El tablero tiene 4 carriles. Cada carril puede tener:
#    - Una criatura
#    - Un edificio (debajo de la criatura)
# ─────────────────────────────────────────────────────────────

class Carril:
    """Un solo carril del tablero. Contiene criatura y/o edificio."""

    def __init__(self, numero):
        self.numero   = numero    # 1, 2, 3 o 4
        self.criatura = None      # Una criatura (o None)
        self.edificio = None      # Un edificio (o None)

    def esta_vacio(self):
        return self.criatura is None and self.edificio is None

    def tiene_criatura(self):
        return self.criatura is not None

    def tiene_edificio(self):
        return self.edificio is not None

    def colocar_criatura(self, carta):
        self.criatura = carta

    def colocar_edificio(self, carta):
        self.edificio = carta

    def remover_criatura(self):
        self.criatura = None

    def remover_edificio(self):
        self.edificio = None

    def resetear_floops(self):
        """Recarga el FLOOP de las cartas en este carril."""
        if self.criatura:
            self.criatura.resetear_floop()

    def __str__(self):
        crit  = str(self.criatura) if self.criatura else "(vacío)"
        edif  = f"  🏠 {self.edificio}" if self.edificio else ""
        return f"Carril {self.numero}: {crit}{edif}"


class Tablero:
    """El tablero de un jugador: 4 carriles."""

    def __init__(self):
        self.carriles = [Carril(i + 1) for i in range(4)]

    def get_carril(self, numero):
        """Devuelve el carril por número (1-4)."""
        return self.carriles[numero - 1]

    def resetear_floops(self):
        for c in self.carriles:
            c.resetear_floops()

    def mostrar(self, nombre_jugador):
        print(f"\n  ┌─ Tablero de {nombre_jugador} " + "─" * (30 - len(nombre_jugador)) + "┐")
        for carril in self.carriles:
            print(f"  │  {carril}")
        print("  └" + "─" * 40 + "┘")
