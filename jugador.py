# jugador.py
# ─────────────────────────────────────────────────────────────
#  PATRIA O MUERTE — El juego de cartas
#  Representa a un jugador (humano o IA heredan de esta clase)
# ─────────────────────────────────────────────────────────────

import random
from tablero import Tablero

class Jugador:
    """Clase base para jugador humano e IA."""

    def __init__(self, nombre, mazo):
        self.nombre          = nombre
        self.hp              = 25          # Puntos de vida iniciales
        self.mazo            = mazo        # Lista de cartas
        self.mano            = []          # Cartas en mano
        self.descarte        = []          # Cartas usadas
        self.tablero         = Tablero()   # Sus 4 carriles
        self.puntos_accion   = 2           # PA disponibles por turno
        self.paralizado      = {}          # {numero_carril: True} si está paralizado

        random.shuffle(self.mazo)
        self.robar(5)                      # Mano inicial de 5 cartas

    # ── Robar cartas ───────────────────────────────────────────

    def robar(self, cantidad=1):
        """Roba N cartas del mazo a la mano."""
        for _ in range(cantidad):
            if self.mazo:
                self.mano.append(self.mazo.pop())
            else:
                print(f"  ⚠️  {self.nombre} no tiene más cartas en el mazo.")
                break

    # ── Estado del jugador ────────────────────────────────────

    def esta_vivo(self):
        return self.hp > 0

    def recibir_daño(self, cantidad):
        self.hp = max(0, self.hp - cantidad)

    def curar(self, cantidad):
        self.hp = min(30, self.hp + cantidad)  # máximo 30 HP

    # ── Mostrar información ───────────────────────────────────

    def mostrar_estado(self):
        print(f"\n  ❤️  {self.nombre}: {self.hp} HP  |  "
              f"Cartas en mano: {len(self.mano)}  |  "
              f"Mazo: {len(self.mazo)}")

    def mostrar_mano(self):
        if not self.mano:
            print(f"  {self.nombre} no tiene cartas en la mano.")
            return
        print(f"\n  🃏 Mano de {self.nombre}:")
        for i, carta in enumerate(self.mano):
            print(f"     {i + 1}. {carta}")

    # ── Inicio de turno ───────────────────────────────────────

    def iniciar_turno(self):
        """Recarga PA, resetea FLOOPs y roba 1 carta."""
        self.puntos_accion = 2
        self.tablero.resetear_floops()
        self.robar(1)
        # Resetear parálisis
        self.paralizado = {}
