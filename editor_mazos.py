# editor_mazos.py
# ─────────────────────────────────────────────────────────────
#  PATRIA O MUERTE — Editor visual de mazos
# ─────────────────────────────────────────────────────────────

import pygame
import sys
import json
import os
import copy
import ventana as V
from carta import Carta
from cartas_data import CARTAS_ORIENTAL, CARTAS_URUGUAYO
from mazos_extra import CARTAS_CHARRUA, CARTAS_POLITICO, CARTAS_CELESTE

# ── Carpeta de mazos guardados ─────────────────────────────
CARPETA_MAZOS = "mazos_guardados"
MIN_CARTAS    = 10
MAX_CARTAS    = 20

# ── Todas las cartas del juego ─────────────────────────────
def get_todas_las_cartas():
    """Devuelve lista de cartas únicas de todos los mazos."""
    todas = []
    vistas = set()
    for pool in [CARTAS_ORIENTAL, CARTAS_URUGUAYO,
                 CARTAS_CHARRUA, CARTAS_POLITICO, CARTAS_CELESTE]:
        for carta in pool:
            if carta.nombre not in vistas:
                vistas.add(carta.nombre)
                todas.append(copy.deepcopy(carta))
    return sorted(todas, key=lambda c: (c.tipo, c.nombre))

# ── Guardar / cargar mazos ─────────────────────────────────

def guardar_mazo(nombre_mazo, cartas):
    os.makedirs(CARPETA_MAZOS, exist_ok=True)
    path = os.path.join(CARPETA_MAZOS, f"{nombre_mazo}.json")
    data = [{"nombre": c.nombre, "tipo": c.tipo, "costo": c.costo,
             "ataque": c.ataque, "defensa": c.defensa,
             "descripcion": c.descripcion, "desc_floop": c.desc_floop}
            for c in cartas]
    with open(path, 'w', encoding='utf-8') as f:
        json.dump({"nombre": nombre_mazo, "cartas": data}, f,
                  ensure_ascii=False, indent=2)

def cargar_mazo(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    cartas = [Carta(c["nombre"], c["tipo"], c["costo"],
                    c.get("ataque",0), c.get("defensa",0),
                    c.get("descripcion",""), c.get("desc_floop",""))
              for c in data["cartas"]]
    return data["nombre"], cartas

def listar_mazos_guardados():
    os.makedirs(CARPETA_MAZOS, exist_ok=True)
    return [f for f in os.listdir(CARPETA_MAZOS) if f.endswith('.json')]

# ── Editor principal ───────────────────────────────────────

def abrir_editor():
    """
    Abre el editor visual de mazos.
    Devuelve (nombre, cartas) si guarda, o None si cancela.
    """
    todas         = get_todas_las_cartas()
    mazo_actual   = []   # cartas en el mazo que está armando
    nombre_mazo   = ""
    scroll_pool   = 0    # scroll del pool de cartas
    scroll_mazo   = 0    # scroll del mazo actual
    carta_hover   = -1
    mazo_hover    = -1
    mensaje       = ""
    msg_timer     = 0
    escribiendo_nombre = False

    # Layout
    W, H       = V.ANCHO, V.ALTO
    PANEL_IZQ  = 0
    ANCHO_IZQ  = int(W * 0.55)   # pool de cartas
    PANEL_DER  = ANCHO_IZQ + 10
    ANCHO_DER  = W - PANEL_DER   # mazo actual
    Y_HEADER   = 60
    Y_CONTENT  = Y_HEADER + 10
    ALTO_CONT  = H - Y_CONTENT - 100

    # Tamaño de filas
    FILA_H     = 38
    COLS_POOL  = 1

    def set_msg(txt, ok=True):
        nonlocal mensaje, msg_timer
        mensaje   = txt
        msg_timer = 120

    while True:
        mx, my = pygame.mouse.get_pos()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return None
                if ev.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()

                if escribiendo_nombre:
                    if ev.key == pygame.K_BACKSPACE:
                        nombre_mazo = nombre_mazo[:-1]
                    elif ev.key == pygame.K_RETURN:
                        escribiendo_nombre = False
                    elif ev.unicode.isprintable() and len(nombre_mazo) < 20:
                        nombre_mazo += ev.unicode

                # Scroll
                if ev.key == pygame.K_UP:
                    scroll_pool = max(0, scroll_pool - 1)
                if ev.key == pygame.K_DOWN:
                    scroll_pool = min(max(0, len(todas) - 12), scroll_pool + 1)

            if ev.type == pygame.MOUSEWHEEL:
                if mx < PANEL_DER:
                    scroll_pool = max(0, min(len(todas)-1, scroll_pool - ev.y))
                else:
                    scroll_mazo = max(0, min(len(mazo_actual)-1, scroll_mazo - ev.y))

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                # Click en nombre
                r_nombre = pygame.Rect(PANEL_DER, H - 85, ANCHO_DER - 10, 32)
                if r_nombre.collidepoint(mx, my):
                    escribiendo_nombre = True
                    continue
                else:
                    escribiendo_nombre = False

                # Click en pool (izquierda) → agregar al mazo
                if mx < PANEL_DER - 5:
                    y_rel = my - Y_CONTENT
                    if 0 <= y_rel < ALTO_CONT:
                        idx = scroll_pool + y_rel // FILA_H
                        if 0 <= idx < len(todas):
                            carta = todas[idx]
                            # Máximo 3 copias de la misma carta
                            copias = sum(1 for c in mazo_actual if c.nombre == carta.nombre)
                            if len(mazo_actual) >= MAX_CARTAS:
                                set_msg(f"Máximo {MAX_CARTAS} cartas por mazo", ok=False)
                            elif copias >= 3:
                                set_msg(f"Máximo 3 copias de '{carta.nombre}'", ok=False)
                            else:
                                mazo_actual.append(copy.deepcopy(carta))
                                set_msg(f"'{carta.nombre}' agregada ({len(mazo_actual)}/{MAX_CARTAS})")

                # Click en mazo (derecha) → quitar carta
                elif mx > PANEL_DER:
                    y_rel = my - Y_CONTENT
                    if 0 <= y_rel < ALTO_CONT - 100:
                        idx = scroll_mazo + y_rel // FILA_H
                        if 0 <= idx < len(mazo_actual):
                            quitada = mazo_actual.pop(idx)
                            set_msg(f"'{quitada.nombre}' quitada")

                # Botón guardar
                r_guardar = pygame.Rect(PANEL_DER, H - 45, ANCHO_DER - 10, 36)
                if r_guardar.collidepoint(mx, my):
                    if len(mazo_actual) < MIN_CARTAS:
                        set_msg(f"Necesitás al menos {MIN_CARTAS} cartas", ok=False)
                    elif not nombre_mazo.strip():
                        set_msg("Poné un nombre al mazo", ok=False)
                        escribiendo_nombre = True
                    else:
                        guardar_mazo(nombre_mazo.strip(), mazo_actual)
                        set_msg(f"¡Mazo '{nombre_mazo}' guardado!")
                        return nombre_mazo.strip(), mazo_actual

                # Botón limpiar
                r_limpiar = pygame.Rect(PANEL_DER, H - 88, ANCHO_DER//2 - 15, 32)
                if r_limpiar.collidepoint(mx, my):
                    mazo_actual = []
                    set_msg("Mazo limpiado")

        # ── Render ─────────────────────────────────────────
        V.pantalla.fill(V.NEGRO)

        # Fondo
        for y in range(H):
            t = y/H
            pygame.draw.line(V.pantalla, (int(8+10*t),int(15+25*t),int(8+10*t)),(0,y),(W,y))

        # Header
        V.rect_redondeado(V.pantalla, (15,25,15),
                          pygame.Rect(0,0,W,Y_HEADER), 0, 1, V.VERDE_MED)
        V.texto(V.pantalla, "🛠  EDITOR DE MAZOS", V.fuente_titulo,
                V.DORADO, W//2, 12, centrado=True)
        V.texto(V.pantalla, "Click izquierda: agregar  |  Click derecha (en tu mazo): quitar  |  ESC: salir",
                V.fuente_peq, V.GRIS_CLAR, W//2, 42, centrado=True)

        # ── Panel izquierdo: pool de cartas ────────────────
        V.rect_redondeado(V.pantalla, (12,22,12),
                          pygame.Rect(PANEL_IZQ, Y_CONTENT-5, ANCHO_IZQ-5, ALTO_CONT+10),
                          6, 1, (40,80,40))

        V.texto(V.pantalla, f"CARTAS DISPONIBLES ({len(todas)})",
                V.fuente_med, V.VERDE_CLAR, PANEL_IZQ+10, Y_CONTENT+2)

        # Hover en pool
        if mx < PANEL_DER - 5:
            y_rel = my - Y_CONTENT
            if 0 <= y_rel < ALTO_CONT:
                carta_hover = scroll_pool + y_rel // FILA_H
            else:
                carta_hover = -1
        else:
            carta_hover = -1

        # Filas del pool
        visible = ALTO_CONT // FILA_H
        for i in range(visible):
            idx = scroll_pool + i
            if idx >= len(todas):
                break
            carta = todas[idx]
            fy    = Y_CONTENT + 22 + i * FILA_H
            sel   = (idx == carta_hover)

            # Fondo fila
            col_fila = (30,55,30) if sel else (18,32,18)
            V.rect_redondeado(V.pantalla, col_fila,
                              pygame.Rect(PANEL_IZQ+4, fy, ANCHO_IZQ-18, FILA_H-2), 4)

            # Indicador de tipo
            col_tipo = {
                "criatura": V.VERDE_CLAR,
                "hechizo":  V.AZUL_CLAR,
                "edificio": V.NARANJA,
            }.get(carta.tipo, V.BLANCO)
            pygame.draw.rect(V.pantalla, col_tipo,
                             (PANEL_IZQ+6, fy+8, 4, FILA_H-18), border_radius=2)

            # Nombre
            V.texto(V.pantalla, carta.nombre, V.fuente_med,
                    V.BLANCO if sel else V.CREMA, PANEL_IZQ+16, fy+5)

            # Stats
            if carta.tipo == "criatura":
                stats = f"ATK:{carta.ataque} DEF:{carta.defensa}"
            elif carta.tipo == "edificio":
                stats = f"DEF:{carta.defensa}"
            else:
                stats = carta.descripcion[:28]
            V.texto(V.pantalla, stats, V.fuente_peq,
                    V.GRIS_CLAR, PANEL_IZQ+16, fy+20)

            # Costo
            r_costo = pygame.Rect(ANCHO_IZQ - 40, fy+8, 22, 18)
            V.rect_redondeado(V.pantalla, V.AMARILLO_OSC, r_costo, 4)
            V.texto_rect(V.pantalla, str(carta.costo), V.fuente_peq, V.NEGRO, r_costo)

            # Copias ya en mazo
            copias = sum(1 for c in mazo_actual if c.nombre == carta.nombre)
            if copias > 0:
                V.texto(V.pantalla, f"x{copias}", V.fuente_peq,
                        V.AMARILLO, ANCHO_IZQ - 62, fy+10)

            # FLOOP indicator
            if carta.desc_floop:
                V.texto(V.pantalla, "✨", V.fuente_peq,
                        V.AMARILLO, ANCHO_IZQ - 85, fy+10)

        # Scrollbar pool
        if len(todas) > visible:
            sb_h   = int(ALTO_CONT * visible / len(todas))
            sb_y   = Y_CONTENT + int(ALTO_CONT * scroll_pool / len(todas))
            pygame.draw.rect(V.pantalla, V.GRIS_MED,
                             (ANCHO_IZQ - 8, Y_CONTENT, 6, ALTO_CONT), border_radius=3)
            pygame.draw.rect(V.pantalla, V.VERDE_CLAR,
                             (ANCHO_IZQ - 8, sb_y, 6, sb_h), border_radius=3)

        # ── Panel derecho: mazo actual ──────────────────────
        V.rect_redondeado(V.pantalla, (12,15,25),
                          pygame.Rect(PANEL_DER, Y_CONTENT-5, ANCHO_DER, ALTO_CONT+10),
                          6, 1, V.AZUL_MED)

        # Contador
        color_count = V.VERDE_CLAR if len(mazo_actual) >= MIN_CARTAS else V.ROJO_CLAR
        V.texto(V.pantalla, f"TU MAZO: {len(mazo_actual)}/{MAX_CARTAS}",
                V.fuente_med, color_count, PANEL_DER+8, Y_CONTENT+2)

        # Hover en mazo
        if mx > PANEL_DER:
            y_rel = my - Y_CONTENT
            if 22 <= y_rel < ALTO_CONT - 100:
                mazo_hover = scroll_mazo + (y_rel - 22) // FILA_H
            else:
                mazo_hover = -1
        else:
            mazo_hover = -1

        # Filas del mazo
        visible_mazo = (ALTO_CONT - 120) // FILA_H
        for i in range(visible_mazo):
            idx = scroll_mazo + i
            if idx >= len(mazo_actual):
                break
            carta = mazo_actual[idx]
            fy    = Y_CONTENT + 22 + i * FILA_H
            sel   = (idx == mazo_hover)

            col_fila = (60,20,20) if sel else (20,25,45)
            V.rect_redondeado(V.pantalla, col_fila,
                              pygame.Rect(PANEL_DER+4, fy, ANCHO_DER-14, FILA_H-2), 4)

            col_tipo = {
                "criatura": V.VERDE_CLAR,
                "hechizo":  V.AZUL_CLAR,
                "edificio": V.NARANJA,
            }.get(carta.tipo, V.BLANCO)
            pygame.draw.rect(V.pantalla, col_tipo,
                             (PANEL_DER+6, fy+8, 4, FILA_H-18), border_radius=2)

            V.texto(V.pantalla, carta.nombre, V.fuente_med,
                    V.ROJO_CLAR if sel else V.BLANCO, PANEL_DER+16, fy+5)

            if carta.tipo == "criatura":
                stats = f"ATK:{carta.ataque} DEF:{carta.defensa}"
            elif carta.tipo == "edificio":
                stats = f"DEF:{carta.defensa}"
            else:
                stats = carta.tipo
            V.texto(V.pantalla, stats, V.fuente_peq,
                    V.GRIS_CLAR, PANEL_DER+16, fy+20)

            if sel:
                V.texto(V.pantalla, "✕ click para quitar",
                        V.fuente_peq, V.ROJO_CLAR, PANEL_DER+ANCHO_DER-120, fy+10)

        # Botones panel derecho
        y_btn = H - 130

        # Resumen del mazo
        tipos = {"criatura":0,"hechizo":0,"edificio":0}
        for c in mazo_actual:
            tipos[c.tipo] = tipos.get(c.tipo,0) + 1
        V.texto(V.pantalla,
                f"Criaturas: {tipos['criatura']}  Hechizos: {tipos['hechizo']}  Edificios: {tipos['edificio']}",
                V.fuente_peq, V.GRIS_CLAR, PANEL_DER+8, y_btn)

        # Campo nombre
        V.texto(V.pantalla, "Nombre del mazo:", V.fuente_peq,
                V.GRIS_CLAR, PANEL_DER+8, y_btn+18)
        r_nombre = pygame.Rect(PANEL_DER, y_btn+32, ANCHO_DER-10, 32)
        col_input = V.AMARILLO if escribiendo_nombre else V.GRIS_MED
        V.rect_redondeado(V.pantalla, (20,25,45), r_nombre, 6, 2, col_input)
        import time
        cursor = "|" if escribiendo_nombre and int(time.time()*2)%2==0 else ""
        V.texto_rect(V.pantalla, nombre_mazo + cursor, V.fuente_med, V.BLANCO, r_nombre)

        # Botón limpiar
        r_limpiar = pygame.Rect(PANEL_DER, y_btn+70, ANCHO_DER//2-5, 30)
        V.rect_redondeado(V.pantalla, V.ROJO_OSC, r_limpiar, 6, 1, V.ROJO_CLAR)
        V.texto_rect(V.pantalla, "🗑 Limpiar", V.fuente_peq, V.BLANCO, r_limpiar)

        # Botón guardar
        r_guardar = pygame.Rect(PANEL_DER, y_btn+106, ANCHO_DER-10, 36)
        col_guard = V.VERDE_MED if len(mazo_actual) >= MIN_CARTAS and nombre_mazo else V.GRIS_OSC
        V.rect_redondeado(V.pantalla, col_guard, r_guardar, 8, 2, V.VERDE_CLAR)
        V.texto_rect(V.pantalla, "💾 GUARDAR MAZO", V.fuente_grande, V.BLANCO, r_guardar)

        # Mensaje de estado
        if msg_timer > 0:
            alpha = min(255, msg_timer * 4)
            col_msg = (100,220,100) if "guardado" in mensaje or "agregada" in mensaje else (220,100,100)
            V.texto(V.pantalla, mensaje, V.fuente_med, col_msg, W//2, H-15, centrado=True)
            msg_timer -= 1

        pygame.display.flip()
        V.reloj.tick(V.FPS)

# ── Pantalla de mazos guardados ────────────────────────────

def pantalla_mis_mazos():
    """
    Muestra los mazos guardados para elegir uno.
    Devuelve (nombre, cartas) o None.
    """
    mazos = listar_mazos_guardados()
    seleccion = 0

    while True:
        mazos = listar_mazos_guardados()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return None
                if ev.key == pygame.K_UP:
                    seleccion = max(0, seleccion-1)
                if ev.key == pygame.K_DOWN:
                    seleccion = min(len(mazos)-1, seleccion+1)
                if ev.key == pygame.K_RETURN and mazos:
                    path = os.path.join(CARPETA_MAZOS, mazos[seleccion])
                    return cargar_mazo(path)
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = ev.pos
                # Click en mazo
                for i, archivo in enumerate(mazos):
                    r = pygame.Rect(V.ANCHO//2-250, 150 + i*55, 500, 48)
                    if r.collidepoint(mx, my):
                        seleccion = i
                # Doble click o botón usar
                r_usar = pygame.Rect(V.ANCHO//2-100, V.ALTO-80, 200, 45)
                if r_usar.collidepoint(mx, my) and mazos:
                    path = os.path.join(CARPETA_MAZOS, mazos[seleccion])
                    return cargar_mazo(path)
                r_nuevo = pygame.Rect(V.ANCHO//2-220, V.ALTO-80, 110, 45)
                if r_nuevo.collidepoint(mx, my):
                    resultado = abrir_editor()
                    if resultado:
                        return resultado
                r_cancel = pygame.Rect(V.ANCHO//2+110, V.ALTO-80, 110, 45)
                if r_cancel.collidepoint(mx, my):
                    return None

        V.pantalla.fill(V.NEGRO)
        for y in range(V.ALTO):
            t = y/V.ALTO
            pygame.draw.line(V.pantalla,(int(8+10*t),int(15+25*t),int(8+10*t)),(0,y),(V.ANCHO,y))

        V.texto(V.pantalla, "📁  MIS MAZOS", V.fuente_titulo,
                V.DORADO, V.ANCHO//2, 40, centrado=True)
        pygame.draw.line(V.pantalla, V.VERDE_MED, (100,90),(V.ANCHO-100,90), 1)

        if not mazos:
            V.texto(V.pantalla, "No tenés mazos guardados todavía.",
                    V.fuente_grande, V.GRIS_CLAR, V.ANCHO//2, 200, centrado=True)
            V.texto(V.pantalla, "Creá uno con el editor →",
                    V.fuente_med, V.GRIS_CLAR, V.ANCHO//2, 240, centrado=True)
        else:
            for i, archivo in enumerate(mazos):
                nombre = archivo.replace('.json','')
                r      = pygame.Rect(V.ANCHO//2-250, 110 + i*55, 500, 48)
                sel    = (i == seleccion)
                col    = V.VERDE_MED if sel else (20,35,20)
                borde  = V.AMARILLO  if sel else V.GRIS_MED
                V.rect_redondeado(V.pantalla, col, r, 8, 2, borde)

                # Leer info del mazo
                try:
                    path = os.path.join(CARPETA_MAZOS, archivo)
                    with open(path, encoding='utf-8') as f:
                        data = json.load(f)
                    n_cartas = len(data['cartas'])
                    V.texto(V.pantalla, nombre, V.fuente_grande,
                            V.BLANCO, V.ANCHO//2-230, 122+i*55)
                    V.texto(V.pantalla, f"{n_cartas} cartas",
                            V.fuente_peq, V.GRIS_CLAR, V.ANCHO//2+150, 130+i*55)
                except:
                    V.texto(V.pantalla, nombre, V.fuente_grande,
                            V.BLANCO, V.ANCHO//2-230, 122+i*55)

        # Botones
        r_nuevo = pygame.Rect(V.ANCHO//2-220, V.ALTO-80, 110, 45)
        V.rect_redondeado(V.pantalla, V.AZUL_MED, r_nuevo, 8, 2, V.AZUL_CLAR)
        V.texto_rect(V.pantalla, "✏ Nuevo", V.fuente_med, V.BLANCO, r_nuevo)

        if mazos:
            r_usar = pygame.Rect(V.ANCHO//2-100, V.ALTO-80, 200, 45)
            V.rect_redondeado(V.pantalla, V.VERDE_MED, r_usar, 8, 2, V.VERDE_CLAR)
            V.texto_rect(V.pantalla, "▶ Usar este mazo", V.fuente_med, V.BLANCO, r_usar)

        r_cancel = pygame.Rect(V.ANCHO//2+110, V.ALTO-80, 110, 45)
        V.rect_redondeado(V.pantalla, V.GRIS_OSC, r_cancel, 8, 2, V.GRIS_MED)
        V.texto_rect(V.pantalla, "✕ Volver", V.fuente_med, V.BLANCO, r_cancel)

        pygame.display.flip()
        V.reloj.tick(V.FPS)
