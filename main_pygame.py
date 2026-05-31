# main_pygame.py
# ─────────────────────────────────────────────────────────────
#  PATRIA O MUERTE — El juego de cartas
#  → py -3.12 main_pygame.py
# ─────────────────────────────────────────────────────────────

import pygame
import sys
import time
import random

from jugador      import Jugador
from ia           import IA
from cartas_data  import get_mazo_oriental, get_mazo_uruguayo
from mazos_extra  import get_mazo_charrua, get_mazo_politico, get_mazo_celeste
from carta        import Carta
from reglas       import mostrar_reglas
from editor_mazos  import abrir_editor, pantalla_mis_mazos
from multijugador  import pantalla_config_2j, jugar_2j
from online        import pantalla_online
import ventana    as V
from efectos      import fade_negro, fade_in, emitir_particulas, agregar_notificacion, actualizar_notificaciones, actualizar_particulas

# ── Pantalla de selección ──────────────────────────────────

def pantalla_seleccion():
    nombre   = ""
    mazo_idx = 0
    mazos = [
        ("🌿 Oriental",  "Gauchos y caudillos",    V.VERDE_MED),
        ("🎭 Uruguayo",  "Fútbol y carnaval",       (80,40,120)),
        ("🏹 Charrúa",   "Guerreros originarios",   (120,60,20)),
        ("🏛 Político",  "Historia oriental",       (60,60,100)),
        ("🩵 Celeste",   "La selección uruguaya",   (20,80,160)),
    ]
    n_mazos = len(mazos)

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                if ev.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                elif ev.key == pygame.K_RETURN and len(nombre) >= 1:
                    return nombre, mazo_idx
                elif ev.key == pygame.K_RIGHT:
                    mazo_idx = (mazo_idx + 1) % n_mazos
                elif ev.key == pygame.K_LEFT:
                    mazo_idx = (mazo_idx - 1) % n_mazos
                elif ev.unicode.isprintable() and len(nombre) < 16:
                    nombre += ev.unicode
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = ev.pos
                bw = 200; gap = 12
                total = n_mazos * bw + (n_mazos-1) * gap
                x0 = (V.ANCHO - total) // 2
                for i in range(n_mazos):
                    bx = x0 + i*(bw+gap)
                    r  = pygame.Rect(bx, 345, bw, 90)
                    if r.collidepoint(mx, my):
                        mazo_idx = i
                bw_btn = 155; gap_btn = 8
                x_btns = V.ANCHO//2 - (5*bw_btn + 4*gap_btn)//2
                r_jugar  = pygame.Rect(x_btns + 0*(bw_btn+gap_btn), 470, bw_btn, 50)
                r_2j     = pygame.Rect(x_btns + 1*(bw_btn+gap_btn), 470, bw_btn, 50)
                r_online = pygame.Rect(x_btns + 2*(bw_btn+gap_btn), 470, bw_btn, 50)
                r_reglas = pygame.Rect(x_btns + 3*(bw_btn+gap_btn), 470, bw_btn, 50)
                r_editor = pygame.Rect(x_btns + 4*(bw_btn+gap_btn), 470, bw_btn, 50)
                if r_jugar.collidepoint(mx, my) and len(nombre) >= 1:
                    return nombre, mazo_idx
                if r_2j.collidepoint(mx, my):
                    return "__2J__", 0
                if r_online.collidepoint(mx, my):
                    return "__ONLINE__", mazo_idx
                if r_reglas.collidepoint(mx, my):
                    mostrar_reglas()
                if r_editor.collidepoint(mx, my):
                    resultado = pantalla_mis_mazos()
                    if resultado:
                        nombre_final = nombre if nombre else "Jugador"
                        return nombre_final, resultado

        V.pantalla.fill(V.NEGRO)
        for y in range(V.ALTO):
            t = y/V.ALTO
            pygame.draw.line(V.pantalla, (int(10+15*t),int(20+40*t),int(10+15*t)),(0,y),(V.ANCHO,y))

        V.texto(V.pantalla, "🇺🇾  PATRIA O MUERTE  🇺🇾", V.fuente_titulo, V.DORADO, V.ANCHO//2, 35, centrado=True)
        V.texto(V.pantalla, "El juego de cartas", V.fuente_grande, V.CREMA, V.ANCHO//2, 85, centrado=True)
        pygame.draw.line(V.pantalla, V.VERDE_MED, (100,115),(V.ANCHO-100,115), 1)

        V.texto(V.pantalla, "Tu nombre:", V.fuente_grande, V.BLANCO, V.ANCHO//2, 140, centrado=True)
        r_input = pygame.Rect(V.ANCHO//2 - 160, 168, 320, 42)
        V.rect_redondeado(V.pantalla, (20,35,20), r_input, 8, 2, V.AMARILLO)
        cursor = "|" if int(time.time() * 2) % 2 == 0 else ""
        V.texto_rect(V.pantalla, nombre + cursor, V.fuente_grande, V.BLANCO, r_input)

        V.texto(V.pantalla, "Elegí tu mazo:", V.fuente_grande, V.BLANCO, V.ANCHO//2, 300, centrado=True)
        V.texto(V.pantalla, "← → para navegar", V.fuente_peq, V.GRIS_CLAR, V.ANCHO//2, 325, centrado=True)

        bw = 200; gap = 12
        total = n_mazos * bw + (n_mazos-1) * gap
        x0 = (V.ANCHO - total) // 2
        for i, (nombre_mazo, desc, col) in enumerate(mazos):
            bx  = x0 + i*(bw+gap)
            r   = pygame.Rect(bx, 345, bw, 90)
            sel = (i == mazo_idx)
            if sel:
                sr = pygame.Rect(bx-2, 343, bw+4, 94)
                V.rect_redondeado(V.pantalla, V.AMARILLO_OSC, sr, 10)
            V.rect_redondeado(V.pantalla, col if sel else V.GRIS_OSC, r, 8, 2, V.AMARILLO if sel else V.GRIS_MED)
            V.texto(V.pantalla, nombre_mazo, V.fuente_med,  V.BLANCO,    bx+bw//2, 360, centrado=True)
            V.texto(V.pantalla, desc,        V.fuente_peq,  V.GRIS_CLAR, bx+bw//2, 385, centrado=True)
            if sel:
                V.texto(V.pantalla, "✓ SELECCIONADO", V.fuente_peq, V.AMARILLO, bx+bw//2, 408, centrado=True)

        for i in range(n_mazos):
            pygame.draw.circle(V.pantalla, V.AMARILLO if i==mazo_idx else V.GRIS_MED,
                               (V.ANCHO//2-(n_mazos//2-i)*20, 450), 5)

        bw_btn = 155; gap_btn = 8
        x_btns = V.ANCHO//2 - (5*bw_btn + 4*gap_btn)//2
        r_jugar  = pygame.Rect(x_btns + 0*(bw_btn+gap_btn), 470, bw_btn, 50)
        r_2j     = pygame.Rect(x_btns + 1*(bw_btn+gap_btn), 470, bw_btn, 50)
        r_online = pygame.Rect(x_btns + 2*(bw_btn+gap_btn), 470, bw_btn, 50)
        r_reglas = pygame.Rect(x_btns + 3*(bw_btn+gap_btn), 470, bw_btn, 50)
        r_editor = pygame.Rect(x_btns + 4*(bw_btn+gap_btn), 470, bw_btn, 50)
        col_btn  = V.VERDE_MED if len(nombre) >= 1 else V.GRIS_OSC
        V.rect_redondeado(V.pantalla, col_btn,       r_jugar,  8, 2, V.AMARILLO)
        V.rect_redondeado(V.pantalla, (60,20,120),   r_2j,     8, 2, V.MORADO_CLAR)
        V.rect_redondeado(V.pantalla, (20,80,120),   r_online, 8, 2, V.CELESTE)
        V.rect_redondeado(V.pantalla, V.AZUL_MED,    r_reglas, 8, 2, V.AZUL_CLAR)
        V.rect_redondeado(V.pantalla, (100,60,20),   r_editor, 8, 2, V.NARANJA)
        V.texto_rect(V.pantalla, "⚔ vs IA",       V.fuente_med, V.BLANCO, r_jugar)
        V.texto_rect(V.pantalla, "👥 2 Local",     V.fuente_med, V.BLANCO, r_2j)
        V.texto_rect(V.pantalla, "🌐 Online",      V.fuente_med, V.BLANCO, r_online)
        V.texto_rect(V.pantalla, "📖 Reglas",      V.fuente_med, V.BLANCO, r_reglas)
        V.texto_rect(V.pantalla, "🛠 Mis Mazos",   V.fuente_med, V.BLANCO, r_editor)

        if len(nombre) == 0:
            V.texto(V.pantalla, "Escribí tu nombre para continuar", V.fuente_peq, V.GRIS_CLAR, V.ANCHO//2, 535, centrado=True)

        pygame.display.flip()
        V.reloj.tick(V.FPS)

# ── Turno del jugador ──────────────────────────────────────

def turno_jugador(jugador, ia, turno):
    jugador.iniciar_turno()
    fade_negro(12)
    V.log_add(f"── Turno {turno}: tu turno, {jugador.nombre} ──")
    fase      = "Jugar cartas"
    seleccion = -1

    while True:
        botones = [
            ("Jugar carta",    "jugar", V.VERDE_MED),
            ("FLOOP",          "floop", V.MORADO),
            ("Terminar turno", "fin",   V.ROJO_OSC),
        ]
        y_mano = V.render(jugador, ia, turno, fase, seleccion, botones, jugador.puntos_accion)
        accion = esperar_accion(jugador, y_mano)

        if accion == "fin":
            break
        elif accion == "floop":
            hacer_floop_jugador(jugador, ia, turno)
        elif isinstance(accion, int) and accion >= 0:
            seleccion = accion
            V.log_add(f"Seleccionada: {jugador.mano[accion].nombre} — apretá 'Jugar carta'")
        elif accion == "jugar":
            if seleccion >= 0 and seleccion < len(jugador.mano):
                carta = jugador.mano[seleccion]
                if carta.costo > jugador.puntos_accion:
                    V.log_add(f"No tenés PA suficientes (costo {carta.costo}, tenés {jugador.puntos_accion})")
                    seleccion = -1
                else:
                    if jugar_carta(jugador, ia, turno, carta, seleccion):
                        seleccion = -1
            else:
                V.log_add("Primero seleccioná una carta de tu mano")

        if jugador.puntos_accion <= 0:
            V.log_add("Sin PA. Pasando a batalla...")
            break

    V.log_add(f"⚔️  {jugador.nombre} ataca...")
    V.render(jugador, ia, turno, "Batalla", pa=jugador.puntos_accion)
    pygame.time.wait(800)
    fase_batalla(jugador, ia)

def esperar_accion(jugador, y_mano):
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx, my = ev.pos
                for r, key in V._botones:
                    if r.collidepoint(mx, my):
                        return key
                if y_mano and y_mano <= my <= y_mano + V.ALTO_CARTA:
                    n     = len(jugador.mano)
                    total = n * (V.ANCHO_CARTA + 8) - 8
                    x0    = (V.ANCHO - total) // 2
                    for i in range(n):
                        cx = x0 + i * (V.ANCHO_CARTA + 8)
                        r  = pygame.Rect(cx, y_mano, V.ANCHO_CARTA, V.ALTO_CARTA)
                        if r.collidepoint(mx, my):
                            return i
        V.reloj.tick(V.FPS)

def jugar_carta(jugador, ia, turno, carta, idx_mano):
    if carta.tipo == "criatura":
        vacios = [i+1 for i, c in enumerate(jugador.tablero.carriles) if not c.tiene_criatura()]
        if not vacios:
            V.log_add("No hay carriles libres para criaturas")
            return False
        num = V.pedir_carril(V.pantalla, jugador, ia, turno, "Elegí un carril", vacios)
        if num is None:
            return False
        jugador.tablero.get_carril(num).colocar_criatura(carta)
        jugador.mano.pop(idx_mano)
        jugador.puntos_accion -= carta.costo
        V.log_add(f"Colocaste '{carta.nombre}' en carril {num}")
        return True

    elif carta.tipo == "edificio":
        vacios = [i+1 for i, c in enumerate(jugador.tablero.carriles) if not c.tiene_edificio()]
        if not vacios:
            V.log_add("No hay carriles libres para edificios")
            return False
        num = V.pedir_carril(V.pantalla, jugador, ia, turno, "Elegí carril para el edificio", vacios)
        if num is None:
            return False
        jugador.tablero.get_carril(num).colocar_edificio(carta)
        jugador.mano.pop(idx_mano)
        jugador.puntos_accion -= carta.costo
        V.log_add(f"Construiste '{carta.nombre}' en carril {num}")
        return True

    elif carta.tipo == "hechizo":
        resultado = aplicar_hechizo_pygame(jugador, ia, turno, carta)
        if resultado is not None:
            jugador.mano.pop(idx_mano)
            jugador.descarte.append(carta)
            jugador.puntos_accion -= carta.costo
            V.log_add(f"Hechizo '{carta.nombre}': {resultado}")
            return True
        return False

def aplicar_hechizo_pygame(jugador, ia, turno, carta):
    nombre = carta.nombre

    if nombre in ("El Mate", "El Asado"):
        jugador.robar(2)
        return "robaste 2 cartas"

    elif nombre == "Gol de Vestuario":
        ia.recibir_daño(3)
        return f"¡Gol de Vestuario! 3 daño directo a {ia.nombre}"

    elif nombre == "Grito de Asencio":
        destruidas = []
        for c in ia.tablero.carriles:
            if c.criatura:
                if c.criatura.recibir_daño(2):
                    destruidas.append(c.criatura.nombre)
                    c.remover_criatura()
        msg = "2 daño a todas las criaturas enemigas"
        if destruidas:
            msg += f" | destruidas: {', '.join(destruidas)}"
        return msg

    elif nombre == "Lanza Gaucha":
        con_criatura = [i+1 for i, c in enumerate(ia.tablero.carriles) if c.criatura]
        if con_criatura:
            num = V.pedir_carril(V.pantalla, jugador, ia, turno,
                                 "Lanza Gaucha: elegí carril enemigo", con_criatura)
            if num is None:
                return None
            c   = ia.tablero.get_carril(num)
            obj = c.criatura.nombre
            if c.criatura.recibir_daño(4):
                c.remover_criatura()
                return f"4 daño a '{obj}' — ¡destruida!"
            return f"4 daño a '{obj}' (quedan {c.criatura.defensa} DEF)"
        ia.recibir_daño(4)
        return f"4 daño directo a {ia.nombre}"

    elif nombre == "Campo de Pesadillas":
        con_criatura = [i+1 for i, c in enumerate(ia.tablero.carriles) if c.criatura]
        if not con_criatura:
            V.log_add("El rival no tiene criaturas")
            return None
        num = V.pedir_carril(V.pantalla, jugador, ia, turno,
                             "Campo de Pesadillas: elegí carril", con_criatura)
        if num is None:
            return None
        c = ia.tablero.get_carril(num)
        c.criatura.ataque = max(0, c.criatura.ataque - 2)
        return f"'{c.criatura.nombre}' pierde 2 ATK (ahora {c.criatura.ataque})"

    elif nombre == "La Murga":
        con_edificio = [i+1 for i, c in enumerate(ia.tablero.carriles) if c.edificio]
        if not con_edificio:
            V.log_add("El rival no tiene edificios")
            return None
        num = V.pedir_carril(V.pantalla, jugador, ia, turno,
                             "La Murga: elegí edificio a destruir", con_edificio)
        if num is None:
            return None
        c           = ia.tablero.get_carril(num)
        nombre_edif = c.edificio.nombre
        c.remover_edificio()
        return f"destruiste '{nombre_edif}'"

    elif nombre == "Reclamar Terreno":
        criaturas = [c for c in jugador.descarte if c.tipo == "criatura"]
        if not criaturas:
            V.log_add("No tenés criaturas en el descarte")
            return None
        recuperada          = criaturas[-1]
        jugador.descarte.remove(recuperada)
        recuperada.defensa  = recuperada.defensa_max
        recuperada.floopada = False
        jugador.mano.append(recuperada)
        return f"'{recuperada.nombre}' vuelve a tu mano"

    elif nombre == "Boleadoras":
        con_criatura = [i+1 for i, c in enumerate(ia.tablero.carriles) if c.criatura]
        if not con_criatura:
            V.log_add("El rival no tiene criaturas")
            return None
        num = V.pedir_carril(V.pantalla, jugador, ia, turno,
                             "Boleadoras: ¿qué criatura inmovilizás?", con_criatura)
        if num is None:
            return None
        ia.paralizado[num] = True
        return f"criatura en carril {num} inmovilizada"

    elif nombre == "Grito de Guerra":
        for c in jugador.tablero.carriles:
            if c.criatura:
                c.criatura.ataque += 1
        return "todas las criaturas aliadas +1 ATK este turno"

    elif nombre == "Espiritu Ancestral":
        criaturas = [c for c in jugador.descarte if c.tipo == "criatura"]
        if not criaturas:
            V.log_add("No tenés criaturas en el descarte")
            return None
        recuperada          = criaturas[-1]
        jugador.descarte.remove(recuperada)
        recuperada.defensa  = 2
        recuperada.floopada = False
        jugador.mano.append(recuperada)
        return f"'{recuperada.nombre}' revive con 2 DEF"

    elif nombre == "Decreto de Ley":
        for c in ia.tablero.carriles:
            if c.criatura:
                c.criatura.floopada = True
        return "ninguna criatura enemiga puede usar FLOOP este turno"

    elif nombre == "Campaña Electoral":
        jugador.robar(2)
        return "robaste 2 cartas"

    elif nombre == "Reforma Agraria":
        con_edificio = [c for c in ia.tablero.carriles if c.edificio]
        if not con_edificio:
            V.log_add("El rival no tiene edificios")
            return None
        objetivo = min(con_edificio, key=lambda c: c.edificio.defensa)
        nombre_edif = objetivo.edificio.nombre
        objetivo.remover_edificio()
        return f"destruiste '{nombre_edif}'"

    elif nombre == "El Maracanazo":
        ia.recibir_daño(4)
        return f"¡MARACANAZO! 4 daño directo a {ia.nombre}"

    elif nombre == "Contraataque":
        ia.recibir_daño(3)
        return "contraataque: 3 daño al rival"

    elif nombre == "La Garra Charrúa":
        con_criatura = [i+1 for i, c in enumerate(jugador.tablero.carriles) if c.criatura]
        if not con_criatura:
            V.log_add("No tenés criaturas")
            return None
        num = V.pedir_carril(V.pantalla, jugador, ia, turno,
                             "La Garra: ¿qué criatura protegés?", con_criatura)
        if num is None:
            return None
        c = jugador.tablero.get_carril(num)
        c.criatura._garra = True
        return f"'{c.criatura.nombre}' no morirá este turno"

    V.log_add(f"Hechizo '{nombre}' no reconocido")
    return None

def hacer_floop_jugador(jugador, ia, turno):
    floopables = [i+1 for i, c in enumerate(jugador.tablero.carriles)
                  if c.criatura and c.criatura.puede_floop()]
    if not floopables:
        V.log_add("No tenés criaturas con FLOOP disponible")
        return
    num = V.pedir_carril(V.pantalla, jugador, ia, turno, "¿Qué criatura floopás?", floopables)
    if num is None:
        return
    carril   = jugador.tablero.get_carril(num)
    criatura = carril.criatura
    nombre   = criatura.nombre
    resultado = None

    if nombre == "El Gaucho":
        criatura.ataque += 2
        resultado = f"+2 ATK este turno (ahora {criatura.ataque})"
    elif nombre == "Artigas":
        for c in jugador.tablero.carriles:
            if c.criatura: c.criatura.ataque += 1
        resultado = "todas las criaturas aliadas +1 ATK"
    elif nombre == "La Payadora":
        con_criatura = [i+1 for i, c in enumerate(ia.tablero.carriles) if c.criatura]
        if not con_criatura:
            V.log_add("No hay criaturas enemigas"); return
        num2 = V.pedir_carril(V.pantalla, jugador, ia, turno,
                               "La Payadora: ¿qué criatura paralizás?", con_criatura)
        if num2 is None: return
        ia.paralizado[num2] = True
        resultado = f"criatura en carril {num2} paralizada"
    elif nombre == "La Curandera":
        aliadas = [c.criatura for c in jugador.tablero.carriles if c.criatura]
        if aliadas:
            obj = min(aliadas, key=lambda c: c.defensa)
            obj.curar(3)
            resultado = f"cura 3 DEF a '{obj.nombre}'"
    elif nombre == "Caballero Azul":
        aliadas = [c.criatura for c in jugador.tablero.carriles if c.criatura]
        if aliadas:
            obj = min(aliadas, key=lambda c: c.defensa)
            obj.curar(2)
            resultado = f"cura 2 DEF a '{obj.nombre}'"
    elif nombre == "El Crack":
        carril._esquivando = True
        resultado = "esquiva activada"
    elif nombre == "El Murguero":
        jugador.robar(1); ia.recibir_daño(1)
        resultado = f"robaste 1 carta y {ia.nombre} recibe 1 daño"
    elif nombre == "El Tamborilero":
        for c in jugador.tablero.carriles:
            if c.criatura: c.criatura.ataque += 1
        resultado = "todas las criaturas aliadas +1 ATK"
    elif nombre == "El Chivito":
        for c in jugador.tablero.carriles:
            if c.criatura: c.criatura.curar(2)
        resultado = "cura 2 DEF a todas las criaturas aliadas"
    elif nombre == "La Vedette":
        con_criatura = [i+1 for i, c in enumerate(ia.tablero.carriles) if c.criatura]
        if not con_criatura:
            V.log_add("No hay criaturas enemigas"); return
        num2 = V.pedir_carril(V.pantalla, jugador, ia, turno,
                               "La Vedette: ¿a qué criatura?", con_criatura)
        if num2 is None: return
        c = ia.tablero.get_carril(num2)
        c.criatura.ataque = max(0, c.criatura.ataque - 2)
        resultado = f"'{c.criatura.nombre}' -2 ATK"
    elif nombre == "Arquero Dan":
        ia.recibir_daño(2)
        resultado = f"2 daño directo a {ia.nombre}"
    elif nombre == "Legión Terricola":
        destruidas = []
        for c in ia.tablero.carriles:
            if c.criatura:
                if c.criatura.recibir_daño(criatura.ataque):
                    destruidas.append(c.criatura.nombre); c.remover_criatura()
        resultado = "ataca todas las criaturas enemigas"
        if destruidas: resultado += f" | destruidas: {', '.join(destruidas)}"
    elif nombre == "Guardián del Silo":
        resultado = f"mano de {ia.nombre}: {len(ia.mano)} cartas"
    elif nombre == "Caminante de Maíz":
        criatura.curar(2)
        resultado = f"regenera 2 DEF (ahora {criatura.defensa})"
    elif nombre == "Guerrero Charrúa":
        criatura.ataque += 2
        resultado = f"+2 ATK este turno (ahora {criatura.ataque})"
    elif nombre == "El Cacique":
        jugador.recibir_daño(4)
        for c in jugador.tablero.carriles:
            if c.criatura: c.criatura.ataque += 2
        resultado = "sacrificás 4 HP, todas las criaturas +2 ATK"
    elif nombre == "La Guerrera":
        con_criatura = [i+1 for i, c in enumerate(ia.tablero.carriles) if c.criatura]
        if con_criatura:
            num2 = V.pedir_carril(V.pantalla, jugador, ia, turno,
                                   "La Guerrera: ¿qué criatura paralizás?", con_criatura)
            if num2: ia.paralizado[num2] = True; resultado = "criatura paralizada"
    elif nombre == "El Chamán":
        jugador.robar(2); jugador.curar(3)
        resultado = "robaste 2 cartas y curaste 3 HP"
    elif nombre == "Arquero Charrúa":
        ia.recibir_daño(3)
        resultado = f"3 daño directo a {ia.nombre}"
    elif nombre == "Luis Suárez":
        ia.recibir_daño(3)
        resultado = f"¡GOOOL! 3 daño directo a {ia.nombre}"
    elif nombre == "Diego Forlán":
        for c in jugador.tablero.carriles:
            if c.criatura: c.criatura.ataque += 1
        resultado = "todas las criaturas aliadas +1 ATK"
    elif nombre == "Edinson Cavani":
        aliadas = [c.criatura for c in jugador.tablero.carriles if c.criatura]
        if aliadas:
            obj = min(aliadas, key=lambda c: c.defensa)
            obj.curar(3); resultado = f"cura 3 DEF a '{obj.nombre}'"
    elif nombre == "El Volante":
        jugador.robar(1); resultado = "robaste 1 carta"
    elif nombre == "El Caudillo":
        n = sum(1 for c in jugador.tablero.carriles if c.criatura)
        jugador.robar(n); resultado = f"robaste {n} cartas"
    elif nombre == "El Senador":
        jugador.puntos_accion += 1; resultado = "ganaste 1 PA extra"
    else:
        resultado = "habilidad activada"

    if resultado:
        criatura.floopada = True
        V.log_add(f"✨ FLOOP '{criatura.nombre}': {resultado}")

# ── Fase de batalla ─────────────────────────────────────────

def fase_batalla(atacante, defensor):
    for i, carril_atk in enumerate(atacante.tablero.carriles):
        if not carril_atk.criatura:
            continue
        criatura_atk = carril_atk.criatura
        num          = i + 1
        carril_def   = defensor.tablero.get_carril(num)

        if num in atacante.paralizado:
            V.log_add(f"Carril {num}: '{criatura_atk.nombre}' paralizada, no ataca")
            continue

        esquivando = getattr(carril_def, '_esquivando', False)
        if esquivando:
            V.log_add(f"Carril {num}: '{carril_def.criatura.nombre}' esquiva!")
            carril_def._esquivando = False
            continue

        if carril_def.criatura:
            cdef      = carril_def.criatura
            muere_def = cdef.recibir_daño(criatura_atk.ataque)
            muere_atk = criatura_atk.recibir_daño(cdef.ataque)
            V.log_add(f"Carril {num}: '{criatura_atk.nombre}' vs '{cdef.nombre}'")
            # La Garra Charrúa
            if muere_def and not getattr(cdef, '_garra', False):
                V.log_add(f"  💀 '{cdef.nombre}' destruida!")
                carril_def.remover_criatura()
                agregar_notificacion("💀 ¡Destruida!", (220,80,30),
                                     V.ALTO_HEADER + V.ALTO_CARRIL + 40)
                emitir_particulas(cx_anim, V.ALTO_HEADER + V.ALTO_CARRIL,
                                  (220,80,20), 20, "explosion")
            elif muere_def:
                cdef.defensa = 1; cdef._garra = False
                V.log_add(f"  🛡 '{cdef.nombre}' sobrevive por La Garra!")
            if muere_atk and not getattr(criatura_atk, '_garra', False):
                V.log_add(f"  💀 '{criatura_atk.nombre}' destruida!")
                carril_atk.remover_criatura()
            elif muere_atk:
                criatura_atk.defensa = 1; criatura_atk._garra = False
                V.log_add(f"  🛡 '{criatura_atk.nombre}' sobrevive por La Garra!")
        else:
            daño = criatura_atk.ataque
            if carril_atk.edificio and carril_atk.edificio.nombre == "La Estancia":
                daño += 1
            if carril_atk.edificio and carril_atk.edificio.nombre == "El Estadio":
                daño += 2
            if carril_atk.edificio and carril_atk.edificio.nombre == "El Centenario":
                daño += 2
            defensor.recibir_daño(daño)
            V.log_add(f"Carril {num}: '{criatura_atk.nombre}' → {daño} daño a {defensor.nombre}!")
            agregar_notificacion(f"-{daño} HP!", (220,80,80),
                                 V.ALTO_HEADER + V.ALTO_CARRIL + 40)

        for c in defensor.tablero.carriles:
            if c.edificio and c.edificio.nombre == "La Rambla":
                atacante.recibir_daño(1)
                V.log_add(f"🏖️  La Rambla devuelve 1 daño a {atacante.nombre}")

        import sprites as SP
        cx_anim = V.MARGEN_LAT + (num-1) * V.ANCHO_CARRIL + V.ANCHO_CARRIL // 2
        cy_anim = V.ALTO_HEADER + V.ALTO_CARRIL + V.ALTO_CARRIL // 2
        SP.agregar_animacion("ataque", cx_anim, cy_anim, (220,80,40))
        for _ in range(20):
            V.render(None, None, 0, "Batalla")
            pygame.time.wait(25)
        pygame.time.wait(150)

# ── Turno de la IA ──────────────────────────────────────────

def turno_ia(ia, jugador, turno):
    ia.iniciar_turno()
    fade_negro(12)
    V.log_add(f"🤖 Turno de {ia.nombre}...")
    V.render(jugador, ia, turno, "Turno IA")
    fade_in(12)
    pygame.time.wait(600)
    mensajes = ia.jugar_turno(jugador)
    for msg in mensajes:
        V.log_add(msg.strip())
        V.render(jugador, ia, turno, "Turno IA")
        pygame.time.wait(400)
    V.log_add(f"⚔️  {ia.nombre} ataca...")
    V.render(jugador, ia, turno, "Batalla IA")
    pygame.time.wait(400)
    fase_batalla(ia, jugador)

# ── Render seguro ───────────────────────────────────────────

_render_orig = V.render
def render_safe(jugador, ia, turno, fase, seleccion_mano=-1, botones=None, pa=2):
    if jugador is None or ia is None:
        return
    result = _render_orig(jugador, ia, turno, fase, seleccion_mano, botones, pa)
    actualizar_notificaciones(V.pantalla)
    actualizar_particulas(V.pantalla)
    pygame.display.flip()
    return result
V.render = render_safe

# ── Loop principal ──────────────────────────────────────────

def jugar(jugador, ia):
    turno = 1
    while jugador.esta_vivo() and ia.esta_vivo():
        turno_jugador(jugador, ia, turno)
        if not ia.esta_vivo():
            break
        turno_ia(ia, jugador, turno)
        turno += 1
    ganador  = jugador.nombre if jugador.esta_vivo() else ia.nombre
    perdedor = ia.nombre      if jugador.esta_vivo() else jugador.nombre
    V.log_add(f"🏆 ¡{ganador} gana la partida!")
    V.render(jugador, ia, turno, "FIN")
    pygame.time.wait(1000)
    V.pantalla_fin(ganador, perdedor)

# ── Entry point ─────────────────────────────────────────────

def main():
    V.pantalla_titulo_pygame()
    nombre, mazo_idx = pantalla_seleccion()

    # Modo online
    if nombre == "__ONLINE__":
        _mazos_fn2 = [
            get_mazo_oriental, get_mazo_uruguayo, get_mazo_charrua,
            get_mazo_politico, get_mazo_celeste,
        ]
        mazo_online = _mazos_fn2[mazo_idx]() if isinstance(mazo_idx, int) and 0 <= mazo_idx < 5 else get_mazo_oriental()
        resultado = pantalla_online(nombre if nombre != "__ONLINE__" else "Jugador", mazo_online)
        if resultado:
            cliente, datos_inicio = resultado
            nombres_online = datos_inicio["nombres"]
            mazos_online   = datos_inicio["mazos"]
            from online import _deserializar_mazo
            j1 = Jugador(nombres_online[0], _deserializar_mazo(mazos_online[0]))
            j2 = Jugador(nombres_online[1], _deserializar_mazo(mazos_online[1]))
            V.log_add(f"🌐 {j1.nombre} vs {j2.nombre} — ¡Partida online!")
            # Por ahora usa el modo 2J local como base
            jugar_2j(j1, j2, turno_jugador, fase_batalla)
        main()
        return

    # Modo 2 jugadores
    if nombre == "__2J__":
        resultado = pantalla_config_2j()
        if resultado:
            j1, j2 = resultado
            V.log_add(f"⚔ {j1.nombre} vs {j2.nombre} — ¡Que empiece!")
            jugar_2j(j1, j2, turno_jugador, fase_batalla)
            otra = V.pantalla_fin(
                j1.nombre if j1.esta_vivo() else j2.nombre,
                j2.nombre if j1.esta_vivo() else j1.nombre
            )
            if otra:
                V._log.clear(); main()
            else:
                pygame.quit()
        else:
            main()
        return

    # Mazo personalizado (viene como tupla desde Mis Mazos)
    if isinstance(mazo_idx, tuple):
        nombre_mazo_custom, cartas_custom = mazo_idx
        mazo_ia   = random.choice([get_mazo_oriental, get_mazo_uruguayo,
                                   get_mazo_charrua, get_mazo_politico,
                                   get_mazo_celeste])()
        jugador   = Jugador(nombre, cartas_custom)
        ia        = IA("El Rival Misterioso", mazo_ia)
        V.log_add(f"¡Bienvenido, {nombre}! Mazo: {nombre_mazo_custom}")
        jugar(jugador, ia)
    else:
        _mazos_fn = [
            (get_mazo_oriental, "El Gaucho Cibernético"),
            (get_mazo_uruguayo, "La Máquina Uruguaya"),
            (get_mazo_charrua,  "El Espíritu Charrúa"),
            (get_mazo_politico, "El Sistema"),
            (get_mazo_celeste,  "La Máquina Celeste"),
        ]
        mazo_jug_fn, _    = _mazos_fn[mazo_idx]
        opciones_ia       = [i for i in range(len(_mazos_fn)) if i != mazo_idx]
        ia_idx            = random.choice(opciones_ia)
        mazo_ia_fn, nombre_ia = _mazos_fn[ia_idx]
        jugador = Jugador(nombre, mazo_jug_fn())
        ia      = IA(nombre_ia, mazo_ia_fn())
        V.log_add(f"¡Bienvenido, {nombre}! Que empiece la batalla.")
        jugar(jugador, ia)

    otra = V.pantalla_fin(
        jugador.nombre if jugador.esta_vivo() else ia.nombre,
        ia.nombre      if jugador.esta_vivo() else jugador.nombre
    )
    if otra:
        V._log.clear()
        main()
    else:
        pygame.quit()

if __name__ == "__main__":
    main()
