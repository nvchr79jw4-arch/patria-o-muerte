# mazos_extra.py
# ─────────────────────────────────────────────────────────────
#  PATRIA O MUERTE — Mazos adicionales
#  Charrúa, Político y Celeste
# ─────────────────────────────────────────────────────────────

import copy
from carta import Carta

# ════════════════════════════════════════════════════════════
#  MAZO CHARRÚA — Guerreros originarios
#  Estilo: muy agresivo, alto ATK, sacrificio
# ════════════════════════════════════════════════════════════

CARTAS_CHARRUA = [
    # Criaturas
    Carta("Guerrero Charrúa", "criatura", costo=1, ataque=4, defensa=3,
          descripcion="Indomable, nunca se rinde",
          desc_floop="Ataca dos veces este turno"),

    Carta("Guerrero Charrúa", "criatura", costo=1, ataque=4, defensa=3,
          descripcion="Indomable, nunca se rinde",
          desc_floop="Ataca dos veces este turno"),

    Carta("El Cacique",       "criatura", costo=2, ataque=5, defensa=6,
          descripcion="Lider supremo de la tribu",
          desc_floop="Sacrifica 2 HP propios para dar +3 ATK a todas las criaturas"),

    Carta("La Guerrera",      "criatura", costo=1, ataque=3, defensa=4,
          descripcion="Tan feroz como el jaguar",
          desc_floop="Paraliza una criatura enemiga"),

    Carta("La Guerrera",      "criatura", costo=1, ataque=3, defensa=4,
          descripcion="Tan feroz como el jaguar",
          desc_floop="Paraliza una criatura enemiga"),

    Carta("El Chamán",        "criatura", costo=2, ataque=2, defensa=5,
          descripcion="Conecta con los espiritus",
          desc_floop="Roba 2 cartas y cura 3 HP"),

    Carta("Arquero Charrúa",  "criatura", costo=1, ataque=3, defensa=2,
          descripcion="Punteria letal con boleadoras",
          desc_floop="3 daño directo al rival"),

    Carta("Arquero Charrúa",  "criatura", costo=1, ataque=3, defensa=2,
          descripcion="Punteria letal con boleadoras",
          desc_floop="3 daño directo al rival"),

    Carta("El Último Charrúa","criatura", costo=2, ataque=5, defensa=4,
          descripcion="El mas poderoso de todos",
          desc_floop=""),

    # Edificios
    Carta("Toldería",         "edificio", costo=1, defensa=4,
          descripcion="Las criaturas en este carril +1 DEF"),

    Carta("Monte Sagrado",    "edificio", costo=2, defensa=5,
          descripcion="Al inicio de tu turno roba 1 carta"),

    # Hechizos
    Carta("Boleadoras",       "hechizo",  costo=1,
          descripcion="Inmoviliza una criatura enemiga por 1 turno"),

    Carta("Boleadoras",       "hechizo",  costo=1,
          descripcion="Inmoviliza una criatura enemiga por 1 turno"),

    Carta("Grito de Guerra",  "hechizo",  costo=2,
          descripcion="Todas las criaturas aliadas +1 ATK este turno"),

    Carta("Grito de Guerra",  "hechizo",  costo=2,
          descripcion="Todas las criaturas aliadas +1 ATK este turno"),

    Carta("Espiritu Ancestral","hechizo", costo=1,
          descripcion="Revive una criatura destruida con 2 DEF"),
]

# ════════════════════════════════════════════════════════════
#  MAZO POLÍTICO — Historia y caudillos
#  Estilo: control, efectos de largo plazo
# ════════════════════════════════════════════════════════════

CARTAS_POLITICO = [
    # Criaturas
    Carta("José Batlle",      "criatura", costo=2, ataque=3, defensa=6,
          descripcion="El reformador. Cambio todo",
          desc_floop="Niega el ataque de una criatura enemiga este turno"),

    Carta("El Caudillo",      "criatura", costo=1, ataque=4, defensa=3,
          descripcion="Arrastra multitudes",
          desc_floop="Roba 1 carta por cada criatura aliada en campo"),

    Carta("El Caudillo",      "criatura", costo=1, ataque=4, defensa=3,
          descripcion="Arrastra multitudes",
          desc_floop="Roba 1 carta por cada criatura aliada en campo"),

    Carta("El Senador",       "criatura", costo=1, ataque=2, defensa=5,
          descripcion="Palabras que cortan mas que espadas",
          desc_floop="Reduce el costo de tu próxima carta en 1 PA"),

    Carta("El Senador",       "criatura", costo=1, ataque=2, defensa=5,
          descripcion="Palabras que cortan mas que espadas",
          desc_floop="Reduce el costo de tu próxima carta en 1 PA"),

    Carta("La Milica",        "criatura", costo=2, ataque=4, defensa=5,
          descripcion="Orden y disciplina",
          desc_floop=""),

    Carta("La Milica",        "criatura", costo=2, ataque=4, defensa=5,
          descripcion="Orden y disciplina",
          desc_floop=""),

    Carta("El Colorado",      "criatura", costo=1, ataque=3, defensa=3,
          descripcion="Rojo de pasion politica",
          desc_floop="Si hay un Blanco aliado, ambos ganan +2 ATK"),

    Carta("El Blanco",        "criatura", costo=1, ataque=3, defensa=3,
          descripcion="Blanco de convicciones",
          desc_floop="Si hay un Colorado aliado, ambos ganan +2 ATK"),

    # Edificios
    Carta("El Parlamento",    "edificio", costo=2, defensa=6,
          descripcion="Al inicio de tu turno ganas 1 PA extra"),

    Carta("La Intendencia",   "edificio", costo=1, defensa=4,
          descripcion="Tus hechizos cuestan 1 PA menos"),

    # Hechizos
    Carta("Decreto de Ley",   "hechizo",  costo=1,
          descripcion="Niega el FLOOP de todas las criaturas enemigas este turno"),

    Carta("Decreto de Ley",   "hechizo",  costo=1,
          descripcion="Niega el FLOOP de todas las criaturas enemigas este turno"),

    Carta("Campaña Electoral","hechizo",  costo=2,
          descripcion="Roba 3 cartas"),

    Carta("Reforma Agraria",  "hechizo",  costo=1,
          descripcion="Destruye el edificio enemigo con menos DEF"),
]

# ════════════════════════════════════════════════════════════
#  MAZO CELESTE — La selección uruguaya
#  Estilo: combinaciones, trabajo en equipo
# ════════════════════════════════════════════════════════════

CARTAS_CELESTE = [
    # Criaturas
    Carta("Luis Suárez",      "criatura", costo=2, ataque=5, defensa=5,
          descripcion="El pistolero. Gol cuando mas duele",
          desc_floop="5 daño directo al rival — ¡GOOOL!"),

    Carta("Diego Forlán",     "criatura", costo=2, ataque=5, defensa=5,
          descripcion="El mejor del mundo 2010",
          desc_floop="Todas las criaturas aliadas +2 ATK"),

    Carta("Edinson Cavani",   "criatura", costo=2, ataque=5, defensa=6,
          descripcion="El Matador de Salto",
          desc_floop="Cura 3 DEF a una criatura aliada"),

    Carta("El 9",             "criatura", costo=1, ataque=4, defensa=3,
          descripcion="Goleador nato",
          desc_floop=""),

    Carta("El 9",             "criatura", costo=1, ataque=4, defensa=3,
          descripcion="Goleador nato",
          desc_floop=""),

    Carta("El Arquero",       "criatura", costo=1, ataque=1, defensa=6,
          descripcion="El muro del arco celeste",
          desc_floop="Niega el próximo ataque directo al rival"),

    Carta("El Arquero",       "criatura", costo=1, ataque=1, defensa=6,
          descripcion="El muro del arco celeste",
          desc_floop="Niega el próximo ataque directo al rival"),

    Carta("El Volante",       "criatura", costo=1, ataque=3, defensa=4,
          descripcion="Motor del equipo",
          desc_floop="Roba 1 carta"),

    Carta("El Volante",       "criatura", costo=1, ataque=3, defensa=4,
          descripcion="Motor del equipo",
          desc_floop="Roba 1 carta"),

    # Edificios
    Carta("El Centenario",    "edificio", costo=2, defensa=7,
          descripcion="El estadio mas glorioso. +2 ATK a criaturas aliadas"),

    Carta("La Celeste Olímpica","edificio",costo=1, defensa=4,
          descripcion="Espiritu del 50. Criaturas aliadas no mueren con 1 DEF"),

    # Hechizos
    Carta("El Maracanazo",    "hechizo",  costo=2,
          descripcion="El golpe historico. 4 daño directo al rival"),

    Carta("Contraataque",     "hechizo",  costo=1,
          descripcion="Devuelve el ultimo daño recibido al rival"),

    Carta("Contraataque",     "hechizo",  costo=1,
          descripcion="Devuelve el ultimo daño recibido al rival"),

    Carta("La Garra Charrúa", "hechizo",  costo=1,
          descripcion="Una criatura aliada no muere este turno, queda con 1 DEF"),

    Carta("La Garra Charrúa", "hechizo",  costo=1,
          descripcion="Una criatura aliada no muere este turno, queda con 1 DEF"),
]

# ── Funciones para obtener mazos ───────────────────────────

def get_mazo_charrua():
    return [copy.deepcopy(c) for c in CARTAS_CHARRUA]

def get_mazo_politico():
    return [copy.deepcopy(c) for c in CARTAS_POLITICO]

def get_mazo_celeste():
    return [copy.deepcopy(c) for c in CARTAS_CELESTE]

# ── Lista de todos los mazos disponibles ───────────────────

TODOS_LOS_MAZOS = {
    "Oriental":  ("Gauchos, caudillos y el campo",   "cartas_data",    "get_mazo_oriental"),
    "Uruguayo":  ("Fútbol, candombe y la ciudad",     "cartas_data",    "get_mazo_uruguayo"),
    "Charrúa":   ("Guerreros originarios",            "mazos_extra",    "get_mazo_charrua"),
    "Político":  ("Caudillos e historia oriental",    "mazos_extra",    "get_mazo_politico"),
    "Celeste":   ("La selección uruguaya",            "mazos_extra",    "get_mazo_celeste"),
}
