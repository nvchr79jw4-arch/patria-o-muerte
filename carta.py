# carta.py
# ─────────────────────────────────────────────────────────────
#  PATRIA O MUERTE — El juego de cartas
#  Define qué ES una carta y cómo se comporta
# ─────────────────────────────────────────────────────────────

class Carta:
    """
    Representa una carta del juego. Puede ser de tres tipos:
      - "criatura"  → tiene ATK y DEF, se coloca en un carril
      - "hechizo"   → efecto inmediato, va al descarte
      - "edificio"  → se coloca en un carril, da ventajas pasivas
    """

    def __init__(self, nombre, tipo, costo, ataque=0, defensa=0,
                 descripcion="", desc_floop=""):
        self.nombre      = nombre       # Nombre de la carta
        self.tipo        = tipo         # "criatura", "hechizo" o "edificio"
        self.costo       = costo        # Puntos de Acción para jugarla (0, 1 o 2)
        self.ataque      = ataque       # Daño que inflige al atacar
        self.defensa     = defensa      # HP de la carta (llega a 0 → destruida)
        self.defensa_max = defensa      # Guarda el valor original para referencias
        self.descripcion = descripcion  # Texto de sabor / efecto
        self.desc_floop  = desc_floop   # Descripción del poder FLOOP (si tiene)
        self.floopada    = False        # ¿Ya usó su FLOOP este turno?

    # ── Consultas ──────────────────────────────────────────────

    def puede_floop(self):
        """True si la carta tiene FLOOP y todavía no lo usó este turno."""
        return self.desc_floop != "" and not self.floopada

    # ── Cambios de estado ──────────────────────────────────────

    def resetear_floop(self):
        """Se llama al inicio de cada turno del dueño para recargar el FLOOP."""
        self.floopada = False

    def recibir_daño(self, cantidad):
        """Reduce la defensa. Devuelve True si la carta muere."""
        self.defensa -= cantidad
        return self.defensa <= 0

    def curar(self, cantidad):
        """Recupera defensa sin superar el máximo original."""
        self.defensa = min(self.defensa + cantidad, self.defensa_max)

    # ── Representación en pantalla ─────────────────────────────

    def __str__(self):
        """Versión corta para listar en la mano o el tablero."""
        if self.tipo == "criatura":
            floop = " ✨" if self.puede_floop() else ""
            return (f"{self.nombre} "
                    f"[ATK:{self.ataque} DEF:{self.defensa}/{self.defensa_max} "
                    f"Costo:{self.costo}PA]{floop}")
        elif self.tipo == "hechizo":
            return f"{self.nombre} [Hechizo | Costo:{self.costo}PA] — {self.descripcion}"
        elif self.tipo == "edificio":
            return (f"{self.nombre} "
                    f"[Edificio | DEF:{self.defensa} | Costo:{self.costo}PA]")
        return self.nombre

    def info_completa(self):
        """Muestra el detalle completo de la carta en pantalla."""
        ancho = 32
        lineas = [
            "  ╔" + "═" * ancho + "╗",
            "  ║" + f" {self.nombre}".center(ancho) + "║",
            "  ║" + "─" * ancho + "║",
            "  ║" + f" Tipo  : {self.tipo}".ljust(ancho) + "║",
            "  ║" + f" Costo : {self.costo} PA".ljust(ancho) + "║",
        ]
        if self.tipo in ("criatura", "edificio"):
            if self.ataque > 0:
                lineas.append("  ║" + f" ATK   : {self.ataque}".ljust(ancho) + "║")
            lineas.append("  ║" + f" DEF   : {self.defensa}/{self.defensa_max}".ljust(ancho) + "║")
        if self.descripcion:
            # Corta la descripción si es muy larga
            desc = self.descripcion[:ancho - 3]
            lineas.append("  ║" + f" {desc}".ljust(ancho) + "║")
        if self.desc_floop:
            floop = self.desc_floop[:ancho - 10]
            lineas.append("  ║" + f" FLOOP : {floop}".ljust(ancho) + "║")
        lineas.append("  ╚" + "═" * ancho + "╝")
        return "\n".join(lineas)
