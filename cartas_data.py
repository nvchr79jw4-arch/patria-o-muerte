# cartas_data.py
# ─────────────────────────────────────────────────────────────
#  PATRIA O MUERTE — El juego de cartas
#  Define los dos mazos del juego con temática uruguaya
#
#  MAZO ORIENTAL  →  folklore, gauchos, caudillos, campo
#  MAZO URUGUAYO  →  fútbol, candombe, carnaval, ciudad
# ─────────────────────────────────────────────────────────────

import copy
from carta import Carta

# ════════════════════════════════════════════════════════════
#  MAZO ORIENTAL — La gente del campo y el folklore
# ════════════════════════════════════════════════════════════

CARTAS_ORIENTAL = [

    # ── Criaturas ──────────────────────────────────────────
    Carta("El Gaucho",        "criatura", costo=1, ataque=3, defensa=4,
          descripcion="Jinete indomable de la Banda Oriental",
          desc_floop="Carga directo: +2 ATK este turno"),

    Carta("El Gaucho",        "criatura", costo=1, ataque=3, defensa=4,
          descripcion="Jinete indomable de la Banda Oriental",
          desc_floop="Carga directo: +2 ATK este turno"),

    Carta("Artigas",          "criatura", costo=2, ataque=5, defensa=7,
          descripcion="El Protector de los Pueblos Libres",
          desc_floop="Todas las criaturas aliadas ganan +1 ATK"),

    Carta("La Payadora",      "criatura", costo=1, ataque=2, defensa=3,
          descripcion="Sus versos paralizan al enemigo",
          desc_floop="Paraliza una criatura enemiga (no ataca este turno)"),

    Carta("El Blandengue",    "criatura", costo=2, ataque=4, defensa=5,
          descripcion="Caballería de elite oriental",
          desc_floop=""),

    Carta("El Blandengue",    "criatura", costo=2, ataque=4, defensa=5,
          descripcion="Caballería de elite oriental",
          desc_floop=""),

    Carta("El Matrero",       "criatura", costo=1, ataque=4, defensa=2,
          descripcion="Rápido y esquivo, nadie lo atrapa",
          desc_floop=""),

    Carta("El Matrero",       "criatura", costo=1, ataque=4, defensa=2,
          descripcion="Rápido y esquivo, nadie lo atrapa",
          desc_floop=""),

    Carta("La Curandera",     "criatura", costo=1, ataque=1, defensa=3,
          descripcion="Sana las heridas del ejército",
          desc_floop="Cura 3 DEF a una criatura aliada"),

    # ── Edificios ──────────────────────────────────────────
    Carta("El Rancho",        "edificio", costo=1, defensa=4,
          descripcion="Refugio que protege a los aliados"),

    Carta("La Estancia",      "edificio", costo=2, defensa=6,
          descripcion="Las criaturas aliadas en este carril +1 ATK"),

    # ── Hechizos ───────────────────────────────────────────
    Carta("El Mate",          "hechizo",  costo=0,
          descripcion="Roba 2 cartas. Energía pura oriental"),

    Carta("El Mate",          "hechizo",  costo=0,
          descripcion="Roba 2 cartas. Energía pura oriental"),

    Carta("Lanza Gaucha",     "hechizo",  costo=1,
          descripcion="Inflige 4 de daño a una criatura enemiga"),

    Carta("Lanza Gaucha",     "hechizo",  costo=1,
          descripcion="Inflige 4 de daño a una criatura enemiga"),

    Carta("Grito de Asencio", "hechizo",  costo=2,
          descripcion="Todas las criaturas enemigas reciben 2 de daño"),
]


# ════════════════════════════════════════════════════════════
#  MAZO URUGUAYO — La ciudad, el fútbol y el carnaval
# ════════════════════════════════════════════════════════════

CARTAS_URUGUAYO = [

    # ── Criaturas ──────────────────────────────────────────
    Carta("El Crack",         "criatura", costo=1, ataque=4, defensa=3,
          descripcion="Un 10 que gambetea cualquier cosa",
          desc_floop="Esquiva: no puede ser atacado este turno"),

    Carta("El Crack",         "criatura", costo=1, ataque=4, defensa=3,
          descripcion="Un 10 que gambetea cualquier cosa",
          desc_floop="Esquiva: no puede ser atacado este turno"),

    Carta("El Murguero",      "criatura", costo=1, ataque=2, defensa=4,
          descripcion="Su ritmo desconcierta al rival",
          desc_floop="Roba 1 carta y hace 1 de daño directo"),

    Carta("El Murguero",      "criatura", costo=1, ataque=2, defensa=4,
          descripcion="Su ritmo desconcierta al rival",
          desc_floop="Roba 1 carta y hace 1 de daño directo"),

    Carta("El Tamborilero",   "criatura", costo=2, ataque=3, defensa=5,
          descripcion="Lleva el ritmo del candombe en el carril",
          desc_floop="Todas las criaturas aliadas +1 ATK hasta el fin del turno"),

    Carta("El Hincha",        "criatura", costo=1, ataque=2, defensa=5,
          descripcion="Aguanta todo, nunca se rinde",
          desc_floop=""),

    Carta("El Hincha",        "criatura", costo=1, ataque=2, defensa=5,
          descripcion="Aguanta todo, nunca se rinde",
          desc_floop=""),

    Carta("El Chivito",       "criatura", costo=2, ataque=4, defensa=6,
          descripcion="El sanguche más poderoso del mundo",
          desc_floop="Cura 2 DEF a todas las criaturas aliadas"),

    Carta("La Vedette",       "criatura", costo=2, ataque=3, defensa=4,
          descripcion="Deslumbra y distrae al enemigo",
          desc_floop="Una criatura enemiga pierde 2 ATK permanentemente"),

    # ── Edificios ──────────────────────────────────────────
    Carta("El Estadio",       "edificio", costo=2, defensa=7,
          descripcion="Fortaleza. Las criaturas aliadas +2 ATK en este carril"),

    Carta("La Rambla",        "edificio", costo=1, defensa=4,
          descripcion="Cuando el rival ataca aqui, recibe 1 de daño"),

    # ── Hechizos ───────────────────────────────────────────
    Carta("Gol de Vestuario", "hechizo",  costo=1,
          descripcion="Inflige 5 de daño directo al rival"),

    Carta("Gol de Vestuario", "hechizo",  costo=1,
          descripcion="Inflige 5 de daño directo al rival"),

    Carta("La Murga",         "hechizo",  costo=2,
          descripcion="Destruye un edificio enemigo"),

    Carta("El Asado",         "hechizo",  costo=0,
          descripcion="Roba 2 cartas. El combustible del Uruguay"),

    Carta("El Asado",         "hechizo",  costo=0,
          descripcion="Roba 2 cartas. El combustible del Uruguay"),
]


# ── Funciones para obtener copias frescas de los mazos ──────

def get_mazo_oriental():
    """Devuelve una copia nueva del mazo Oriental (para que cada partida sea independiente)."""
    return [copy.deepcopy(c) for c in CARTAS_ORIENTAL]

def get_mazo_uruguayo():
    """Devuelve una copia nueva del mazo Uruguayo."""
    return [copy.deepcopy(c) for c in CARTAS_URUGUAYO]
