# ventana.py
# ─────────────────────────────────────────────────────────────
#  PATRIA O MUERTE — El juego de cartas
#  Interfaz gráfica con pygame
# ─────────────────────────────────────────────────────────────

import pygame
import sys

# ── Colores ────────────────────────────────────────────────
NEGRO        = (10,  10,  10)
BLANCO       = (240, 240, 230)
GRIS_OSC     = (40,  40,  40)
GRIS_MED     = (70,  70,  70)
GRIS_CLAR    = (120, 120, 120)
VERDE_OSC    = (20,  60,  20)
VERDE_MED    = (34,  85,  34)
VERDE_CLAR   = (60,  120, 60)
VERDE_CARRIL = (45,  100, 45)
AZUL_OSC     = (10,  30,  80)
AZUL_MED     = (20,  60,  160)
AZUL_CLAR    = (80,  130, 220)
ROJO_OSC     = (100, 10,  10)
ROJO_MED     = (180, 30,  30)
ROJO_CLAR    = (220, 80,  80)
AMARILLO     = (220, 190, 50)
AMARILLO_OSC = (150, 120, 20)
NARANJA      = (200, 100, 30)
CELESTE      = (100, 180, 220)
MORADO       = (100, 50,  150)
MORADO_CLAR  = (150, 80,  200)
DORADO       = (200, 160, 40)
TIERRA       = (100, 70,  30)
CREMA        = (230, 210, 170)

# ── Constantes de layout ───────────────────────────────────
ANCHO        = 1360
ALTO         = 768
FPS          = 60

# Zonas principales
ALTO_HEADER  = 75    # barra de estado arriba
ALTO_LOG     = 80    # log de mensajes abajo
ALTO_MANO    = 110   # zona de mano del jugador (separada del campo)
ALTO_CAMPO   = ALTO - ALTO_HEADER - ALTO_LOG - ALTO_MANO

# Carriles
N_CARRILES   = 4
MARGEN_LAT   = 20
ANCHO_CARRIL = (ANCHO - MARGEN_LAT * 2) // N_CARRILES
ALTO_CARRIL  = (ALTO_CAMPO - 30) // 2

# Cartas
ANCHO_CARTA  = min(ANCHO_CARRIL - 16, 180)
ALTO_CARTA   = 95
RADIO        = 8

# ── Inicialización ─────────────────────────────────────────

pygame.init()
pantalla    = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN)
pygame.display.set_caption("🇺🇾 Patria o Muerte — El juego de cartas")
reloj       = pygame.time.Clock()

# Fuentes
try:
    fuente_grande  = pygame.font.SysFont("segoeui",     22, bold=True)
    fuente_med     = pygame.font.SysFont("segoeui",     16)
    fuente_peq     = pygame.font.SysFont("segoeui",     13)
    fuente_titulo  = pygame.font.SysFont("segoeui",     32, bold=True)
    fuente_num     = pygame.font.SysFont("consolas",    20, bold=True)
except:
    fuente_grande  = pygame.font.Font(None, 24)
    fuente_med     = pygame.font.Font(None, 18)
    fuente_peq     = pygame.font.Font(None, 14)
    fuente_titulo  = pygame.font.Font(None, 36)
    fuente_num     = pygame.font.Font(None, 22)

# ── Helpers de dibujo ──────────────────────────────────────

def rect_redondeado(surf, color, rect, radio=RADIO, borde=0, color_borde=None):
    pygame.draw.rect(surf, color, rect, border_radius=radio)
    if borde and color_borde:
        pygame.draw.rect(surf, color_borde, rect, borde, border_radius=radio)

def texto(surf, txt, fuente, color, x, y, centrado=False):
    sup = fuente.render(str(txt), True, color)
    if centrado:
        x -= sup.get_width() // 2
    surf.blit(sup, (x, y))

def texto_rect(surf, txt, fuente, color, rect, centrado_v=True):
    sup = fuente.render(str(txt), True, color)
    rx = rect.x + (rect.width - sup.get_width()) // 2
    ry = rect.y + (rect.height - sup.get_height()) // (2 if centrado_v else 4)
    surf.blit(sup, (rx, ry))

def barra_hp(surf, x, y, ancho, hp, hp_max=25, alto=14):
    """Dibuja una barra de vida."""
    fondo = pygame.Rect(x, y, ancho, alto)
    rect_redondeado(surf, GRIS_OSC, fondo, 4)
    if hp > 0:
        pct    = max(0, min(1, hp / hp_max))
        color  = ROJO_MED if pct < 0.3 else (AMARILLO if pct < 0.6 else (80, 200, 80))
        llena  = pygame.Rect(x, y, int(ancho * pct), alto)
        rect_redondeado(surf, color, llena, 4)
    pygame.draw.rect(surf, GRIS_CLAR, fondo, 1, border_radius=4)

# ── Dibujar una carta ──────────────────────────────────────

def dibujar_carta(surf, carta, x, y, seleccionada=False, es_mano=False):
    """Dibuja una carta centrada en (x, y) como esquina superior izquierda."""
    w, h = ANCHO_CARTA, ALTO_CARTA
    r    = pygame.Rect(x, y, w, h)

    # Color de fondo según tipo
    if carta.tipo == "criatura":
        col_fondo  = (30, 55, 30)
        col_borde  = VERDE_CLAR if not seleccionada else AMARILLO
        col_tipo   = (100, 200, 100)
    elif carta.tipo == "hechizo":
        col_fondo  = (30, 30, 70)
        col_borde  = AZUL_CLAR if not seleccionada else AMARILLO
        col_tipo   = (120, 160, 240)
    else:  # edificio
        col_fondo  = (60, 40, 20)
        col_borde  = NARANJA if not seleccionada else AMARILLO
        col_tipo   = (200, 140, 80)

    if seleccionada:
        # Glow efecto
        r_glow = pygame.Rect(x-3, y-3, w+6, h+6)
        rect_redondeado(surf, AMARILLO_OSC, r_glow, RADIO+2)

    rect_redondeado(surf, col_fondo, r, RADIO, 2, col_borde)

    # Nombre
    nombre_corto = carta.nombre[:16] + ("…" if len(carta.nombre) > 16 else "")
    texto(surf, nombre_corto, fuente_peq, BLANCO, x + w//2, y + 7, centrado=True)

    # Línea divisoria
    pygame.draw.line(surf, col_borde, (x+6, y+22), (x+w-6, y+22), 1)

    # Stats según tipo
    if carta.tipo == "criatura":
        # ATK
        texto(surf, "⚔", fuente_peq, ROJO_CLAR, x+8, y+28)
        texto(surf, str(carta.ataque), fuente_grande, ROJO_CLAR, x+24, y+26)
        # DEF
        texto(surf, "🛡", fuente_peq, AZUL_CLAR, x+8, y+52)
        texto(surf, f"{carta.defensa}/{carta.defensa_max}", fuente_med, AZUL_CLAR, x+24, y+50)
        # Barra DEF
        barra_hp(surf, x+6, y+70, w-12, carta.defensa, carta.defensa_max, 8)
        # FLOOP disponible
        if carta.puede_floop():
            texto(surf, "✨FLOOP", fuente_peq, AMARILLO, x + w//2, y+82, centrado=True)

    elif carta.tipo == "hechizo":
        # Descripción corta
        desc = carta.descripcion[:22]
        texto(surf, desc, fuente_peq, CELESTE, x + w//2, y+35, centrado=True)
        texto(surf, "HECHIZO", fuente_peq, col_tipo, x + w//2, y+70, centrado=True)

    elif carta.tipo == "edificio":
        texto(surf, "🏛", fuente_peq, col_tipo, x+8, y+28)
        texto(surf, f"DEF {carta.defensa}", fuente_med, col_tipo, x+24, y+28)
        desc = carta.descripcion[:20]
        texto(surf, desc, fuente_peq, CREMA, x + w//2, y+55, centrado=True)

    # Costo PA (esquina sup derecha)
    r_costo = pygame.Rect(x + w - 22, y + 3, 18, 16)
    rect_redondeado(surf, DORADO, r_costo, 4)
    texto_rect(surf, str(carta.costo), fuente_peq, NEGRO, r_costo)

# ── Dibujar carril ─────────────────────────────────────────

def dibujar_carril(surf, num_carril, carril, x, y, ancho, alto, es_ia=False, seleccionado=False):
    import sprites as SP

    col_borde = AMARILLO if seleccionado else (50, 90, 50)
    r = pygame.Rect(x, y, ancho, alto)
    s = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    s.fill((0, 0, 0, 60) if not seleccionado else (255, 220, 0, 30))
    surf.blit(s, (x, y))
    pygame.draw.rect(surf, col_borde, r, 2, border_radius=6)

    texto(surf, f"{num_carril}", fuente_peq, (80, 140, 80), x + ancho//2, y+4, centrado=True)

    if carril.criatura:
        sp_w, sp_h = 64, 72
        sp = SP.get_sprite(carril.criatura.nombre, sp_w, sp_h, invertido=es_ia, tick=SP.get_tick())
        sx = x + (ancho - sp_w) // 2
        sy = y + 18
        surf.blit(sp, (sx, sy))
        cy_info = sy + sp_h + 4
        bw = ancho - 20
        barra_hp(surf, x+10, cy_info, bw, carril.criatura.defensa, carril.criatura.defensa_max, 6)
        texto(surf, f"atk:{carril.criatura.ataque}", fuente_peq, (220,100,100), x+8,       cy_info+9)
        texto(surf, f"def:{carril.criatura.defensa}", fuente_peq, (100,160,220), x+ancho-55, cy_info+9)
        if carril.criatura.puede_floop():
            texto(surf, "FLOOP!", fuente_peq, AMARILLO, x + ancho//2, cy_info+9, centrado=True)

    if carril.edificio:
        ey = y + alto - 26
        r_edif = pygame.Rect(x+4, ey, ancho-8, 22)
        rect_redondeado(surf, (60, 35, 10), r_edif, 4, 1, NARANJA)
        nombre_corto = carril.edificio.nombre[:16]
        texto(surf, nombre_corto, fuente_peq, CREMA, x + ancho//2, ey+6, centrado=True)

# ── Dibujar tablero completo ───────────────────────────────

def dibujar_tablero(surf, jugador, ia):
    import sprites as SP
    y_ia  = ALTO_HEADER + 10
    y_sep = ALTO_HEADER + ALTO_CARRIL + 20
    y_jug = y_sep + 10

    SP.dibujar_fondo_campo(surf, ANCHO, ALTO, ALTO_HEADER, ALTO_CAMPO)
    SP.actualizar_y_dibujar_animaciones(surf)

    pygame.draw.line(surf, (60, 110, 60), (MARGEN_LAT, y_sep), (ANCHO - MARGEN_LAT, y_sep), 2)
    texto(surf, "── CAMPO DE BATALLA ──", fuente_peq, (80, 140, 80), ANCHO//2, y_sep - 10, centrado=True)

    for i, carril in enumerate(ia.tablero.carriles):
        cx = MARGEN_LAT + i * ANCHO_CARRIL
        dibujar_carril(surf, i+1, carril, cx, y_ia, ANCHO_CARRIL - 8, ALTO_CARRIL - 15, es_ia=True)

    for i, carril in enumerate(jugador.tablero.carriles):
        cx = MARGEN_LAT + i * ANCHO_CARRIL
        dibujar_carril(surf, i+1, carril, cx, y_jug, ANCHO_CARRIL - 8, ALTO_CARRIL - 15, es_ia=False)

# ── Header con HP ──────────────────────────────────────────

def dibujar_header(surf, jugador, ia, turno, prompt):
    rect_redondeado(surf, GRIS_OSC, pygame.Rect(0, 0, ANCHO, ALTO_HEADER), 0)
    pygame.draw.line(surf, VERDE_MED, (0, ALTO_HEADER), (ANCHO, ALTO_HEADER), 2)

    # Título
    texto(surf, "🇺🇾 PATRIA O MUERTE", fuente_grande, DORADO, ANCHO//2, 8, centrado=True)
    texto(surf, f"Turno {turno}  |  Fase: {prompt}", fuente_peq, GRIS_CLAR, ANCHO//2, 32, centrado=True)

    # HP Jugador (izquierda)
    texto(surf, jugador.nombre, fuente_med, BLANCO, 20, 10)
    barra_hp(surf, 20, 32, 200, jugador.hp)
    texto(surf, f"{jugador.hp} HP", fuente_num, (100, 220, 100), 20, 48)
    texto(surf, f"Mano: {len(jugador.mano)}  Mazo: {len(jugador.mazo)}", fuente_peq, GRIS_CLAR, 20, 65)

    # HP IA (derecha)
    texto(surf, ia.nombre, fuente_med, BLANCO, ANCHO - 20, 10)
    sup_ia = fuente_med.render(ia.nombre, True, BLANCO)
    barra_hp(surf, ANCHO - 220, 32, 200, ia.hp)
    texto(surf, f"{ia.hp} HP", fuente_num, ROJO_CLAR, ANCHO - 80, 48)
    texto(surf, f"Mano: {len(ia.mano)}  Mazo: {len(ia.mazo)}", fuente_peq, GRIS_CLAR, ANCHO - 160, 65)

# ── Log de mensajes ────────────────────────────────────────

MAX_LOG = 6
_log    = []

def log_add(msg):
    _log.append(msg)
    if len(_log) > MAX_LOG:
        _log.pop(0)

def dibujar_log(surf):
    y0 = ALTO - ALTO_LOG
    rect_redondeado(surf, (15, 15, 15), pygame.Rect(0, y0, ANCHO, ALTO_LOG), 0)
    pygame.draw.line(surf, VERDE_MED, (0, y0), (ANCHO, y0), 2)
    texto(surf, "LOG DE BATALLA", fuente_peq, GRIS_CLAR, 10, y0 + 4)
    for i, msg in enumerate(_log):
        col = BLANCO if i == len(_log)-1 else GRIS_CLAR
        texto(surf, msg[:120], fuente_peq, col, 10, y0 + 20 + i * 17)

# ── Mano del jugador ───────────────────────────────────────

_carta_hover = -1

def dibujar_mano(surf, jugador, seleccion=-1, pa=2):
    """Dibuja las cartas de la mano del jugador en su zona separada."""
    n     = len(jugador.mano)
    if n == 0:
        return

    y0    = ALTO - ALTO_LOG - ALTO_MANO + (ALTO_MANO - ALTO_CARTA) // 2
    total = n * (ANCHO_CARTA + 8) - 8
    x0    = (ANCHO - total) // 2

    # Fondo de la zona de mano
    y_zona = ALTO - ALTO_LOG - ALTO_MANO
    zona   = pygame.Rect(0, y_zona, ANCHO, ALTO_MANO)
    s_zona = pygame.Surface((ANCHO, ALTO_MANO), pygame.SRCALPHA)
    s_zona.fill((0, 0, 0, 100))
    surf.blit(s_zona, (0, y_zona))
    pygame.draw.line(surf, VERDE_MED, (0, y_zona), (ANCHO, y_zona), 1)
    texto(surf, "TU MANO", fuente_peq, GRIS_CLAR, 10, y_zona + 4)
    texto(surf, f"PA: {pa}/2", fuente_peq, AMARILLO, ANCHO - 60, y_zona + 4)

    for i, carta in enumerate(jugador.mano):
        cx  = x0 + i * (ANCHO_CARTA + 8)
        sel = (i == seleccion)
        if carta.costo > pa:
            s = pygame.Surface((ANCHO_CARTA, ALTO_CARTA), pygame.SRCALPHA)
            s.fill((0, 0, 0, 120))
        dibujar_carta(surf, carta, cx, y0, seleccionada=sel)
        if carta.costo > pa:
            surf.blit(s, (cx, y0))
        texto(surf, str(i+1), fuente_peq, AMARILLO, cx + ANCHO_CARTA//2, y0 - 14, centrado=True)

    return y0

# ── Botones de acción ──────────────────────────────────────

_botones = []

def dibujar_botones(surf, opciones):
    """
    opciones: lista de (label, key, color)
    Devuelve lista de (rect, key)
    """
    global _botones
    _botones = []
    n     = len(opciones)
    bw    = 160
    bh    = 32
    gap   = 12
    total = n * bw + (n-1) * gap
    x0    = (ANCHO - total) // 2
    y0    = ALTO - ALTO_LOG - ALTO_MANO - bh - 8

    for i, (label, key, color) in enumerate(opciones):
        bx = x0 + i * (bw + gap)
        r  = pygame.Rect(bx, y0, bw, bh)
        rect_redondeado(surf, color, r, 6, 1, BLANCO)
        texto_rect(surf, label, fuente_med, BLANCO, r)
        _botones.append((r, key))

    return _botones

# ── Pantalla de selección de carril ───────────────────────

def pedir_carril(surf, jugador, ia, turno, prompt, carriles_validos):
    """
    Muestra el tablero con los carriles válidos resaltados y espera click.
    Devuelve número de carril (1-4) o None si cancela.
    """
    y_jug = ALTO_HEADER + ALTO_CARRIL + 30

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                return None
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx, my = ev.pos
                for i in range(4):
                    cx = MARGEN_LAT + i * ANCHO_CARRIL
                    r  = pygame.Rect(cx, y_jug, ANCHO_CARRIL - 8, ALTO_CARRIL - 15)
                    if r.collidepoint(mx, my) and (i+1) in carriles_validos:
                        return i + 1

        surf.fill(NEGRO)
        dibujar_header(surf, jugador, ia, turno, prompt)
        dibujar_tablero(surf, jugador, ia)
        dibujar_log(surf)

        # Resaltar carriles válidos
        for i in range(4):
            num = i + 1
            cx  = MARGEN_LAT + i * ANCHO_CARRIL
            cy  = y_jug
            r   = pygame.Rect(cx, cy, ANCHO_CARRIL - 8, ALTO_CARRIL - 15)
            if num in carriles_validos:
                s = pygame.Surface((r.width, r.height), pygame.SRCALPHA)
                s.fill((255, 220, 0, 60))
                surf.blit(s, (cx, cy))
                pygame.draw.rect(surf, AMARILLO, r, 3, border_radius=6)
                texto(surf, "CLICK", fuente_peq, AMARILLO, cx + (ANCHO_CARRIL-8)//2, cy + ALTO_CARRIL - 30, centrado=True)

        texto(surf, prompt, fuente_grande, AMARILLO, ANCHO//2, ALTO - ALTO_LOG - 50, centrado=True)
        texto(surf, "[ESC] Cancelar", fuente_peq, GRIS_CLAR, ANCHO//2, ALTO - ALTO_LOG - 28, centrado=True)

        pygame.display.flip()
        reloj.tick(FPS)

# ── Render principal ───────────────────────────────────────

def render(jugador, ia, turno, fase, seleccion_mano=-1, botones=None, pa=2):
    pantalla.fill(NEGRO)
    dibujar_header(pantalla, jugador, ia, turno, fase)
    dibujar_tablero(pantalla, jugador, ia)
    dibujar_log(pantalla)
    y_mano = dibujar_mano(pantalla, jugador, seleccion_mano, pa)
    if botones:
        dibujar_botones(pantalla, botones)
    pygame.display.flip()
    reloj.tick(FPS)
    # Procesar eventos pendientes para evitar lag
    pygame.event.pump()
    return y_mano

# ── Pantalla de fin de juego ───────────────────────────────

def pantalla_fin(ganador, perdedor):
    from efectos import pantalla_fin_epica
    return pantalla_fin_epica(ganador, perdedor)

# ── Pantalla de título ─────────────────────────────────────

def pantalla_titulo_pygame():
    from efectos import FondoAnimado, dibujar_logo, fade_negro
    fondo = FondoAnimado()
    tick  = 0

    while True:
        tick += 1
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN or ev.type == pygame.MOUSEBUTTONDOWN:
                fade_negro(20)
                return

        fondo.update()
        fondo.draw(pantalla)

        # Logo animado
        dibujar_logo(pantalla, tick, y=270)

        # Cartas decorativas
        from carta import Carta
        import sprites as SP
        import math
        cartas_deco = [
            ("El Gaucho",  120, 380),
            ("Artigas",    ANCHO//2 - ANCHO_CARTA//2, 360),
            ("Luis Suárez",ANCHO - 120 - ANCHO_CARTA, 380),
        ]
        for nombre_c, cx, cy in cartas_deco:
            sp = SP.get_sprite(nombre_c, 64, 72, tick=tick)
            pantalla.blit(sp, (cx + ANCHO_CARTA//2 - 32, cy + 10))
            c = Carta(nombre_c, "criatura", 1, 3, 4)
            dibujar_carta(pantalla, c, cx, cy)

        # Cita
        texto(pantalla, '"Los orientales somos o dominamos o morimos"',
              fuente_med, GRIS_CLAR, ANCHO//2, 510, centrado=True)
        texto(pantalla, "— José Artigas", fuente_peq, GRIS_CLAR, ANCHO//2, 532, centrado=True)

        # Instrucción parpadeante
        if tick % 60 < 40:
            texto(pantalla, "▶  Presioná cualquier tecla para jugar  ◀",
                  fuente_grande, AMARILLO, ANCHO//2, 580, centrado=True)

        pygame.display.flip()
        reloj.tick(FPS)
