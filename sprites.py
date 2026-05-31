# sprites.py
# ─────────────────────────────────────────────────────────────
#  PATRIA O MUERTE — Sprites pixel art 16x16 con animación idle
# ─────────────────────────────────────────────────────────────

import pygame
import math

# ── Paleta ─────────────────────────────────────────────────
TRANSP     = (0,0,0,0)
NEGRO      = (10,10,10)
BLANCO     = (240,240,230)
PIEL       = (220,170,110)
PIEL_OSC   = (180,130,80)
ROJO       = (200,40,40)
ROJO_OSC   = (140,20,20)
AZUL       = (40,80,200)
AZUL_CLAR  = (80,140,220)
VERDE      = (40,160,40)
VERDE_OSC  = (20,100,20)
AMARILLO   = (220,190,50)
MARRON     = (120,70,30)
MARRON_OSC = (80,40,10)
GRIS       = (120,120,120)
GRIS_CLAR  = (180,180,180)
NARANJA    = (210,100,20)
CELESTE    = (100,180,230)
DORADO     = (200,160,30)
CREMA      = (230,210,170)
VIOLETA    = (140,60,180)
ROSA       = (220,120,160)
TIERRA     = (160,100,50)
VERDE_OLIVA= (100,120,40)

ESCALA = 4  # cada pixel del arte = 4x4 px reales

def dibujar_pixels(surf, mapa, paleta, ox=0, oy=0, esc=ESCALA):
    for y, fila in enumerate(mapa):
        for x, c in enumerate(fila):
            col = paleta.get(c)
            if col:
                pygame.draw.rect(surf, col, (ox+x*esc, oy+y*esc, esc, esc))

# ════════════════════════════════════════════════════════════
#  SPRITES 16x16
# ════════════════════════════════════════════════════════════

# ── El Gaucho (16x16) ──────────────────────────────────────
GAUCHO = [
    "....SSSSSS......",
    "...SSSSSSSS.....",
    "...SPPPPPPS.....",
    "....PPEEPP......",
    "....PPPPPP......",
    "...MPPPPPM......",
    "..MMMMMMMM......",
    "..MCMMMCMM......",
    "...MMMMMM.......",
    "....BBBB........",
    "...BBBBBB.......",
    "..BB....BB......",
    "..BB....BB......",
    "..ZZ....ZZ......",
    "................",
    "................",
]
GAUCHO_P = {
    'S': MARRON,'P': PIEL,'E': (50,30,10),
    'M': (140,80,30),'C': ROJO,'B': (100,60,20),
    'Z': MARRON_OSC,'.': None
}

# ── Artigas (16x16) ────────────────────────────────────────
ARTIGAS = [
    "....AAAAAA......",
    "...AAAAAAAA.....",
    "...APPPPPPA.....",
    "....PPEEPP......",
    "....PPPPPP......",
    "...UPPPPPU......",
    "..UUUGUUUU......",
    "..UUUGUUU.......",
    "...UUUUUU.......",
    "....BBBB........",
    "...BBBBBB.......",
    "..BB....BB......",
    "..BB....BB......",
    "..ZZ....ZZ......",
    "................",
    "................",
]
ARTIGAS_P = {
    'A': DORADO,'P': PIEL,'E': (50,30,10),
    'U': (20,40,120),'G': DORADO,'B': (10,10,80),
    'Z': NEGRO,'.': None
}

# ── La Payadora (16x16) ────────────────────────────────────
PAYADORA = [
    "....FFFFFF......",
    "...FFFFFFFF.....",
    "...FPPPPPFF.....",
    "....PPEEPP......",
    "....PPPPPP......",
    "...VPPPPVV......",
    "..VVVVVVVV......",
    "..VRVRVRVR......",
    "...VVVVVV.......",
    "...GGGGGG.......",
    "..GGGGGGGG......",
    "..GG....GG......",
    "..GG....GG......",
    "..ZZ....ZZ......",
    "................",
    "................",
]
PAYADORA_P = {
    'F': AMARILLO,'P': PIEL,'E': (60,30,10),
    'V': (180,50,100),'R': ROJO,'G': (200,80,120),
    'Z': MARRON,'.': None
}

# ── El Blandengue (16x16) ──────────────────────────────────
BLANDENGUE = [
    "....HHHHHH......",
    "...HHHHHHHH.....",
    "...HPPPPPPH.....",
    "....PPEEPP......",
    "....PPPPPP......",
    "...UPPPPAU......",
    "..UUAUAUAU......",
    "..UUAUAUUU......",
    "...UUUUUU.......",
    "....LLLL........",
    "...LLLLLL.......",
    "..LL....LL......",
    "..LL....LL......",
    "..ZZ....ZZ......",
    "................",
    "................",
]
BLANDENGUE_P = {
    'H': GRIS,'P': PIEL,'E': (50,30,10),
    'U': (30,80,30),'A': DORADO,'L': MARRON,
    'Z': NEGRO,'.': None
}

# ── El Matrero (16x16) ─────────────────────────────────────
MATRERO = [
    "....NNNNNN......",
    "...NNNNNNNN.....",
    "...NPPPPPNN.....",
    "....PPEEPP......",
    "....PPPPPP......",
    "...NPPPPNN......",
    "..NNNNNNNNN.....",
    "..NDNDNDNN......",
    "...NNNNNN.......",
    "....BBBB........",
    "...BBBBBB.......",
    "..BB....BB......",
    "..BB....BB......",
    "..ZZ....ZZ......",
    "................",
    "................",
]
MATRERO_P = {
    'N': (40,40,40),'P': PIEL,'E': (40,20,0),
    'D': ROJO,'B': MARRON_OSC,'Z': NEGRO,'.': None
}

# ── La Curandera (16x16) ───────────────────────────────────
CURANDERA = [
    "....WWWWWW......",
    "...WWWWWWWW.....",
    "...WPPPPPWW.....",
    "....PPEEPP......",
    "....PPPPPP......",
    "...WPPPPWW......",
    "..WWWCWWWW......",
    "..WWCCCWWW......",
    "...WWWWWW.......",
    "....BBBB........",
    "...BBBBBB.......",
    "..BB....BB......",
    "..BB....BB......",
    "..ZZ....ZZ......",
    "................",
    "................",
]
CURANDERA_P = {
    'W': BLANCO,'P': PIEL,'E': (50,30,10),
    'C': ROJO,'B': GRIS_CLAR,'Z': MARRON,'.': None
}

# ── El Crack (16x16) ───────────────────────────────────────
CRACK = [
    "....CCCCCC......",
    "...CCCCCCCC.....",
    "...CPPPPPCC.....",
    "....PPEEPP......",
    "....PPPPPP......",
    "...CPPPPCC......",
    "..CCCCCCCC......",
    "..CWCWCWCC......",
    "...CCCCCC.......",
    "....SSSS........",
    "...SSSSSS.......",
    "..SS....SS......",
    "..SS....SS......",
    "..BB....BB......",
    "................",
    "................",
]
CRACK_P = {
    'C': AZUL,'P': PIEL,'E': (50,30,10),
    'W': BLANCO,'S': BLANCO,'B': NEGRO,'.': None
}

# ── El Murguero (16x16) ────────────────────────────────────
MURGUERO = [
    "....TTTTTT......",
    "...TTTTTTTT.....",
    "...TPPPPPTT.....",
    "....PPEEPP......",
    "....PPPPPP......",
    "...RPPPPOO......",
    "..RROOOROO......",
    "..RRORROOO......",
    "...RROROR.......",
    "....BBBB........",
    "...BBBBBB.......",
    "..BB....BB......",
    "..BB....BB......",
    "..ZZ....ZZ......",
    "................",
    "................",
]
MURGUERO_P = {
    'T': AMARILLO,'P': PIEL,'E': (50,30,10),
    'R': ROJO,'O': NARANJA,'B': (150,40,40),
    'Z': MARRON,'.': None
}

# ── El Tamborilero (16x16) ─────────────────────────────────
TAMBORILERO = [
    "....tttttt......",
    "...tttttttt.....",
    "...tPPPPPtt.....",
    "....PPEEPP......",
    "....PPPPPP......",
    "...DPPPPDt......",
    "..DDDDDDDDD.....",
    "..DMDMDMDM......",
    "...DDDDDDD......",
    "....BBBB........",
    "...BBBBBB.......",
    "..BB....BB......",
    "..BB....BB......",
    "..ZZ....ZZ......",
    "................",
    "................",
]
TAMBORILERO_P = {
    't': MARRON,'P': PIEL,'E': (50,30,10),
    'D': (60,30,10),'M': CREMA,'B': MARRON_OSC,
    'Z': NEGRO,'.': None
}

# ── El Hincha (16x16) ──────────────────────────────────────
HINCHA = [
    "....GGGGGG......",
    "...GGGGGGGG.....",
    "...GPPPPPGG.....",
    "....PPEEPP......",
    "....PPPPPP......",
    "...GPPPPGG......",
    "..GGGGGGGG......",
    "..GWGWGWGG......",
    "...GGGGGG.......",
    "....BBBB........",
    "...BBBBBB.......",
    "..BB....BB......",
    "..BB....BB......",
    "..ZZ....ZZ......",
    "................",
    "................",
]
HINCHA_P = {
    'G': (20,120,20),'P': PIEL,'E': (50,30,10),
    'W': BLANCO,'B': (10,80,10),'Z': MARRON,'.': None
}

# ── El Chivito (16x16) — es un sándwich ────────────────────
CHIVITO = [
    "................",
    "................",
    "..BBBBBBBBBB....",
    ".BBBBBBBBBBBBB..",
    ".BWWWWWWWWWWWB..",
    ".BRRRRRRRRRRBB..",
    ".BVVVVVVVVVVBB..",
    ".BYYYYYYYYYBBB..",
    ".BBBBBBBBBBBBB..",
    "..LLLLLLLLLLL...",
    "..LLLLLLLLLLL...",
    ".LLLLLLLLLLLL...",
    "................",
    "................",
    "................",
    "................",
]
CHIVITO_P = {
    'B': (180,100,30),'W': CREMA,'R': ROJO,
    'V': VERDE,'Y': AMARILLO,'L': (200,160,80),'.': None
}

# ── La Vedette (16x16) ─────────────────────────────────────
VEDETTE = [
    "....FFFFFF......",
    "...FFFFFFFF.....",
    "...FPPPPPFF.....",
    "....PPEEPP......",
    "....PPPPPP......",
    "...RPPPPSS......",
    "..RRSSSSSS......",
    "..RSRSRSSS......",
    "...RRSRRS.......",
    "....BBBB........",
    "...BBBBBB.......",
    "..BB....BB......",
    "..BB....BB......",
    "..ZZ....ZZ......",
    "................",
    "................",
]
VEDETTE_P = {
    'F': AMARILLO,'P': PIEL,'E': (50,30,10),
    'R': ROSA,'S': (255,180,200),'B': (200,80,120),
    'Z': MARRON,'.': None
}

# ── Arquero Dan (16x16) ────────────────────────────────────
ARQUERO = [
    "....hhhhhh......",
    "...hhhhhhhh.....",
    "...hPPPPPhh.....",
    "....PPEEPP......",
    "....PPPPPP......",
    "...VPPPPAh......",
    "..VVVVVAAV......",
    "..VAVAVAAV......",
    "...VVVVVV.......",
    "....BBBB........",
    "...BBBBBB.......",
    "..BB....BB......",
    "..BB....BB......",
    "..ZZ....ZZ......",
    "................",
    "................",
]
ARQUERO_P = {
    'h': VERDE_OSC,'P': PIEL,'E': (50,30,10),
    'V': VERDE,'A': MARRON,'B': VERDE_OSC,
    'Z': MARRON_OSC,'.': None
}

# ── Caballero de Maíz (16x16) ──────────────────────────────
CAB_MAIZ = [
    "....YYYYYY......",
    "...YYYYYYYY.....",
    "...YPPPPPY......",
    "....PPEEPP......",
    "....PPPPPP......",
    "...YPPPPGY......",
    "..YYYYYYYY......",
    "..YGYGYGYY......",
    "...YYYYYY.......",
    "....BBBB........",
    "...BBBBBB.......",
    "..BB....BB......",
    "..BB....BB......",
    "..ZZ....ZZ......",
    "................",
    "................",
]
CAB_MAIZ_P = {
    'Y': AMARILLO,'P': PIEL,'E': (50,30,10),
    'G': VERDE,'B': (160,120,20),'Z': MARRON,'.': None
}

# ── Legión Terricola (16x16) ───────────────────────────────
LEGION = [
    "...HHHHHHHHH....",
    "..HHHHHHHHHHH...",
    "..HPPPPPPPPH....",
    "...PPEEPPEP.....",
    "...PPPPPPPP.....",
    "..GGGGGGGGGG....",
    "..GAGAGAGAGG....",
    "..GAGAGAGAGG....",
    "...GGGGGGGGG....",
    "....BBBBBBBB....",
    "...BBBBBBBBBB...",
    "..BBB......BBB..",
    "..BBB......BBB..",
    "..ZZZ......ZZZ..",
    "................",
    "................",
]
LEGION_P = {
    'H': GRIS,'P': PIEL,'E': (50,30,10),
    'G': (50,100,50),'A': MARRON_OSC,'B': (30,60,30),
    'Z': NEGRO,'.': None
}

# ── Caminante de Maíz (16x16) ──────────────────────────────
CAM_MAIZ = [
    "....yyyyyy......",
    "...yyyyyyyy.....",
    "...yPPPPPyy.....",
    "....PPEEPP......",
    "....PPPPPP......",
    "...yPPPPyy......",
    "..yyyyyyyyY.....",
    "..yGyGyGyyy.....",
    "...yyyyyyy......",
    "....yyyy........",
    "...yyyyyy.......",
    "...yy..yy.......",
    "...yy..yy.......",
    "...ZZ..ZZ.......",
    "................",
    "................",
]
CAM_MAIZ_P = {
    'y': (180,160,20),'P': PIEL,'E': (50,30,10),
    'Y': (220,200,50),'G': VERDE,'Z': MARRON,'.': None
}

# ── Guardián del Silo (16x16) ──────────────────────────────
GUARDIAN = [
    "....hhhhhh......",
    "...hhhhhhhh.....",
    "...hPPPPPhh.....",
    "....PPEEPP......",
    "....PPPPPP......",
    "...BPPPPAh......",
    "..BBBBBABB......",
    "..BABABABBB.....",
    "...BBBBBBB......",
    "....LLLL........",
    "...LLLLLL.......",
    "..LL....LL......",
    "..LL....LL......",
    "..ZZ....ZZ......",
    "................",
    "................",
]
GUARDIAN_P = {
    'h': MARRON,'P': PIEL,'E': (50,30,10),
    'B': (100,60,20),'A': DORADO,'L': (120,70,25),
    'Z': MARRON_OSC,'.': None
}

# ── Caballero Azul ─────────────────────────────────────────
CAB_AZUL = [
    "....AAAAAA......",
    "...AAAAAAAA.....",
    "...APPPPPAA.....",
    "....PPEEPP......",
    "....PPPPPP......",
    "...UPPPPAU......",
    "..UUUUUUUU......",
    "..UAUAUAUU......",
    "...UUUUUU.......",
    "....BBBB........",
    "...BBBBBB.......",
    "..BB....BB......",
    "..BB....BB......",
    "..ZZ....ZZ......",
    "................",
    "................",
]
CAB_AZUL_P = {
    'A': AZUL_CLAR,'P': PIEL,'E': (50,30,10),
    'U': AZUL,'B': (10,10,120),'Z': NEGRO,'.': None
}


# ── Guerrero Charrúa ───────────────────────────────────────
CHARRUA = [
    "....CCCCCC......",
    "...CCCCCCCC.....",
    "...CPPPPPCC.....",
    "....PPEEPP......",
    "....PPPPPP......",
    "...RPPPPCC......",
    "..RRRCCRCC......",
    "..RRCRCRRR......",
    "...RRRRRR.......",
    "....BBBB........",
    "...BBBBBB.......",
    "..BB....BB......",
    "..BB....BB......",
    "..ZZ....ZZ......",
    "................",
    "................",
]
CHARRUA_P = {
    'C': (80,50,20),'P': PIEL,'E': (40,20,0),
    'R': ROJO,'B': MARRON_OSC,'Z': NEGRO,'.': None
}

# ── El Cacique ─────────────────────────────────────────────
CACIQUE = [
    "...PPPPPPPP.....",
    "..PPPPPPPPPP....",
    "..PPPPPPPPP.....",
    "....PPEEPP......",
    "....PPPPPP......",
    "...DPPPPDD......",
    "..DDDDDDDDD.....",
    "..DADADADDR.....",
    "...DDDDDDR......",
    "....BBBB........",
    "...BBBBBB.......",
    "..BB....BB......",
    "..BB....BB......",
    "..ZZ....ZZ......",
    "................",
    "................",
]
CACIQUE_P = {
    'P': AMARILLO,'E': (50,30,10),
    'D': (100,60,20),'A': ROJO,'R': NARANJA,
    'B': MARRON_OSC,'Z': NEGRO,'.': None
}

# ── Luis Suárez ────────────────────────────────────────────
SUAREZ = [
    "....CCCCCC......",
    "...CCCCCCCC.....",
    "...CPPPPPCC.....",
    "....PPEEPP......",
    "....PPPPPP......",
    "...CPPPPCC......",
    "..CCCCCCCC......",
    "..CWCWCWCC......",
    "...CCCCCC.......",
    "....SSSS........",
    "...SSSSSS.......",
    "..SS....SS......",
    "..SS....SS......",
    "..BB....BB......",
    "................",
    "................",
]
SUAREZ_P = {
    'C': CELESTE,'P': PIEL,'E': (50,30,10),
    'W': BLANCO,'S': BLANCO,'B': NEGRO,'.': None
}

# ── José Batlle ────────────────────────────────────────────
BATLLE = [
    "....GGGGGG......",
    "...GGGGGGGG.....",
    "...GPPPPPGG.....",
    "....PPEEPP......",
    "....PPPPPP......",
    "...NPPPPGG......",
    "..NNNNNNNN......",
    "..NGNGNGNN......",
    "...NNNNNN.......",
    "....BBBB........",
    "...BBBBBB.......",
    "..BB....BB......",
    "..BB....BB......",
    "..ZZ....ZZ......",
    "................",
    "................",
]
BATLLE_P = {
    'G': GRIS_CLAR,'P': PIEL,'E': (50,30,10),
    'N': (50,50,50),'B': GRIS,'Z': NEGRO,'.': None
}

# ── Mapa de sprites ────────────────────────────────────────
SPRITES = {
    "El Gaucho":         (GAUCHO,       GAUCHO_P),
    "Artigas":           (ARTIGAS,      ARTIGAS_P),
    "La Payadora":       (PAYADORA,     PAYADORA_P),
    "El Blandengue":     (BLANDENGUE,   BLANDENGUE_P),
    "El Matrero":        (MATRERO,      MATRERO_P),
    "La Curandera":      (CURANDERA,    CURANDERA_P),
    "El Crack":          (CRACK,        CRACK_P),
    "El Murguero":       (MURGUERO,     MURGUERO_P),
    "El Tamborilero":    (TAMBORILERO,  TAMBORILERO_P),
    "El Hincha":         (HINCHA,       HINCHA_P),
    "El Chivito":        (CHIVITO,      CHIVITO_P),
    "La Vedette":        (VEDETTE,      VEDETTE_P),
    "Arquero Dan":       (ARQUERO,      ARQUERO_P),
    "Caballero de Maíz": (CAB_MAIZ,     CAB_MAIZ_P),
    "Legión Terricola":  (LEGION,       LEGION_P),
    "Caminante de Maíz": (CAM_MAIZ,     CAM_MAIZ_P),
    "Guardián del Silo": (GUARDIAN,     GUARDIAN_P),
    "Caballero Azul":    (CAB_AZUL,     CAB_AZUL_P),
    "Segador de Campo":  (MATRERO,      GAUCHO_P),
    "Perro Molón":       (HINCHA,       CRACK_P),
    "Erudito Antiguo":   (CURANDERA,    ARTIGAS_P),
    "Guerrero Charrúa":  (CHARRUA,      CHARRUA_P),
    "El Cacique":        (CACIQUE,      CACIQUE_P),
    "La Guerrera":       (CHARRUA,      PAYADORA_P),
    "El Chamán":         (CURANDERA,    CACIQUE_P),
    "Arquero Charrúa":   (ARQUERO,      CHARRUA_P),
    "El Último Charrúa": (CACIQUE,      CHARRUA_P),
    "José Batlle":       (BATLLE,       BATLLE_P),
    "El Caudillo":       (ARTIGAS,      BATLLE_P),
    "El Senador":        (BATLLE,       ARTIGAS_P),
    "La Milica":         (BLANDENGUE,   BATLLE_P),
    "El Colorado":       (HINCHA,       MURGUERO_P),
    "El Blanco":         (HINCHA,       BLANCO_P if "BLANCO_P" in dir() else CURANDERA_P),
    "Luis Suárez":       (SUAREZ,       SUAREZ_P),
    "Diego Forlán":      (SUAREZ,       CRACK_P),
    "Edinson Cavani":    (SUAREZ,       MURGUERO_P),
    "El 9":              (CRACK,        SUAREZ_P),
    "El Arquero":        (GUARDIAN,     SUAREZ_P),
    "El Volante":        (HINCHA,       SUAREZ_P),
}

# ── Cache y generación ─────────────────────────────────────
_cache = {}

def get_sprite_base(nombre):
    """Genera la surface base del sprite sin animación."""
    key = nombre
    if key in _cache:
        return _cache[key]

    ancho, alto = 16 * ESCALA, 16 * ESCALA
    surf = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    surf.fill((0,0,0,0))

    if nombre in SPRITES:
        mapa, paleta = SPRITES[nombre]
        dibujar_pixels(surf, mapa, paleta, 0, 0, ESCALA)
    else:
        # Sprite genérico
        pygame.draw.circle(surf, GRIS, (ancho//2, alto//2-10), 10)
        pygame.draw.rect(surf, GRIS, (ancho//2-8, alto//2, 16, 20))

    _cache[key] = surf
    return surf


def get_sprite(nombre, ancho_dest, alto_dest, invertido=False, tick=0):
    """
    Devuelve sprite animado (idle) escalado al tamaño pedido.
    tick: frame actual del juego para la animación.
    """
    base = get_sprite_base(nombre)

    # Animación idle: movimiento suave de arriba/abajo
    offset_y = int(math.sin(tick * 0.08) * 2)

    # Surface de destino
    surf = pygame.Surface((ancho_dest, alto_dest), pygame.SRCALPHA)
    surf.fill((0,0,0,0))

    # Escalar base al tamaño destino
    escala_surf = pygame.transform.scale(base, (ancho_dest, alto_dest - 4))

    if invertido:
        escala_surf = pygame.transform.flip(escala_surf, True, False)

    surf.blit(escala_surf, (0, offset_y))
    return surf


# ── Tick global ────────────────────────────────────────────
_tick = 0

def avanzar_tick():
    global _tick
    _tick += 1

def get_tick():
    return _tick


# ════════════════════════════════════════════════════════════
#  ANIMACIONES
# ════════════════════════════════════════════════════════════

class Animacion:
    def __init__(self, tipo, x, y, color=(220,80,80)):
        self.tipo     = tipo
        self.x        = x
        self.y        = y
        self.color    = color
        self.frame    = 0
        self.duracion = {"ataque":20,"daño":15,"magia":25,"muerte":30}.get(tipo, 20)
        self.activa   = True

    def avanzar(self):
        self.frame += 1
        if self.frame >= self.duracion:
            self.activa = False

    def dibujar(self, surf):
        t = self.frame / self.duracion
        if   self.tipo == "ataque": self._ataque(surf, t)
        elif self.tipo == "daño":   self._daño(surf, t)
        elif self.tipo == "magia":  self._magia(surf, t)
        elif self.tipo == "muerte": self._muerte(surf, t)

    def _ataque(self, surf, t):
        for i in range(6):
            alpha  = int(255 * (1-t) * ((6-i)/6))
            offset = int(i * 7 * t)
            p1 = (self.x - 20 + offset, self.y - 20 + offset)
            p2 = (self.x + 20 + offset, self.y + 20 + offset)
            s  = pygame.Surface((surf.get_width(), surf.get_height()), pygame.SRCALPHA)
            pygame.draw.line(s, (*self.color, alpha), p1, p2, 4)
            p3 = (self.x - 20 + offset, self.y + 20 + offset)
            p4 = (self.x + 20 + offset, self.y - 20 + offset)
            pygame.draw.line(s, (*self.color, alpha//2), p3, p4, 2)
            surf.blit(s, (0,0))

    def _daño(self, surf, t):
        alpha = int(220 * (1-t))
        radio = int(25 + 15*t)
        s = pygame.Surface((radio*2, radio*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (255,50,50,alpha), (radio,radio), radio)
        surf.blit(s, (self.x-radio, self.y-radio))
        # Número de daño flotando
        try:
            fuente = pygame.font.SysFont("consolas", 20, bold=True)
            num_y  = int(self.y - 30 * t)
            txt    = fuente.render("!", True, (255,255,100))
            surf.blit(txt, (self.x, num_y))
        except:
            pass

    def _magia(self, surf, t):
        for i in range(8):
            angulo = (i/8)*math.pi*2 + t*math.pi*4
            radio  = int(25 * math.sin(t * math.pi))
            px = int(self.x + radio * math.cos(angulo))
            py = int(self.y + radio * math.sin(angulo))
            alpha = int(255*(1-t))
            s = pygame.Surface((10,10), pygame.SRCALPHA)
            pygame.draw.circle(s, (220,190,50,alpha), (5,5), 5)
            surf.blit(s, (px-5, py-5))

    def _muerte(self, surf, t):
        import random; random.seed(99)
        for _ in range(16):
            angulo = random.uniform(0, math.pi*2)
            dist   = int(50*t)
            px = int(self.x + dist*math.cos(angulo))
            py = int(self.y + dist*math.sin(angulo))
            alpha = int(255*(1-t))
            sz = max(2, int(8*(1-t)))
            s = pygame.Surface((sz*2,sz*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (220,80,20,alpha), (sz,sz), sz)
            surf.blit(s, (px-sz, py-sz))

_animaciones = []

def agregar_animacion(tipo, x, y, color=(220,80,80)):
    _animaciones.append(Animacion(tipo, x, y, color))

def actualizar_y_dibujar_animaciones(surf):
    global _animaciones
    avanzar_tick()
    for a in _animaciones:
        a.dibujar(surf)
        a.avanzar()
    _animaciones = [a for a in _animaciones if a.activa]

def hay_animaciones():
    return len(_animaciones) > 0


# ════════════════════════════════════════════════════════════
#  FONDO DECORADO
# ════════════════════════════════════════════════════════════

def dibujar_fondo_campo(surf, ancho, alto, y_inicio, alto_campo):
    # Degradado verde
    for y in range(y_inicio, y_inicio + alto_campo):
        t   = (y - y_inicio) / alto_campo
        col = (int(15+15*t), int(55+25*t), int(15+15*t))
        pygame.draw.line(surf, col, (0,y), (ancho,y))

    # Líneas de cancha
    cy = y_inicio + alto_campo // 2
    pygame.draw.line(surf, (50,110,50), (0,cy), (ancho,cy), 2)
    pygame.draw.circle(surf, (50,110,50), (ancho//2, cy), 70, 1)
    pygame.draw.circle(surf, (50,110,50), (ancho//2, cy), 5)

    # Arcos
    pygame.draw.rect(surf, (50,110,50), (ancho//2-60, y_inicio, 120, 30), 1)
    pygame.draw.rect(surf, (50,110,50), (ancho//2-60, y_inicio+alto_campo-30, 120, 30), 1)

    # Líneas de carriles
    from ventana import MARGEN_LAT, ANCHO_CARRIL, N_CARRILES
    for i in range(1, N_CARRILES):
        x = MARGEN_LAT + i * ANCHO_CARRIL
        pygame.draw.line(surf, (40,90,40), (x,y_inicio), (x,y_inicio+alto_campo), 1)

    # Matecito decorativo
    _dibujar_mate(surf, 15, y_inicio + alto_campo - 55)
    _dibujar_mate(surf, ancho - 45, y_inicio + alto_campo - 55)

    # Sol de Artigas
    _dibujar_sol_artigas(surf, ancho//2, y_inicio + 22)


def _dibujar_mate(surf, x, y):
    # Termo
    pygame.draw.rect(surf, (50,50,50),   (x, y, 10, 28))
    pygame.draw.rect(surf, (90,90,90),   (x+1,y+1, 8, 4))
    pygame.draw.rect(surf, (70,70,70),   (x+1,y+24,8, 4))
    # Mate
    pygame.draw.ellipse(surf, MARRON,     (x+12,y+8, 20,18))
    pygame.draw.ellipse(surf, MARRON_OSC, (x+13,y+9, 18,16))
    pygame.draw.ellipse(surf, (60,30,5),  (x+14,y+10,16,8))
    # Bombilla
    pygame.draw.line(surf, GRIS, (x+22,y+12),(x+28,y+3), 2)
    pygame.draw.circle(surf, GRIS_CLAR, (x+28,y+3), 2)


def _dibujar_sol_artigas(surf, cx, cy):
    r = 12
    pygame.draw.circle(surf, (160,130,20), (cx,cy), r)
    pygame.draw.circle(surf, (140,110,10), (cx,cy), r, 1)
    for i in range(16):
        ang = (i/16)*math.pi*2
        x1  = int(cx + (r+2)*math.cos(ang))
        y1  = int(cy + (r+2)*math.sin(ang))
        x2  = int(cx + (r+8 if i%2==0 else r+5)*math.cos(ang))
        y2  = int(cy + (r+8 if i%2==0 else r+5)*math.sin(ang))
        pygame.draw.line(surf, (140,110,10), (x1,y1),(x2,y2), 1)
