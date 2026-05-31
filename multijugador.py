# multijugador.py
# ─────────────────────────────────────────────────────────────
#  PATRIA O MUERTE — Modo 2 jugadores local
# ─────────────────────────────────────────────────────────────

import pygame
import sys
import random

from jugador      import Jugador
from cartas_data  import get_mazo_oriental, get_mazo_uruguayo
from mazos_extra  import get_mazo_charrua, get_mazo_politico, get_mazo_celeste
from editor_mazos import pantalla_mis_mazos
import ventana    as V

MAZOS_FN = [
    (get_mazo_oriental, "🌿 Oriental",  "Gauchos y caudillos",  V.VERDE_MED),
    (get_mazo_uruguayo, "🎭 Uruguayo",  "Fútbol y carnaval",    (80,40,120)),
    (get_mazo_charrua,  "🏹 Charrúa",   "Guerreros originarios",(120,60,20)),
    (get_mazo_politico, "🏛 Político",  "Historia oriental",    (60,60,100)),
    (get_mazo_celeste,  "🩵 Celeste",   "La selección",         (20,80,160)),
]

# ── Pantalla de configuración 2 jugadores ──────────────────

def pantalla_config_2j():
    """
    Pide nombre y mazo a cada jugador.
    Devuelve (jugador1, jugador2) o None si cancela.
    """
    estado    = 0   # 0 = jugador 1, 1 = jugador 2
    nombres   = ["", ""]
    mazos_idx = [0, 1]

    while True:
        actual = estado  # 0 o 1

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return None
                if ev.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                if ev.key == pygame.K_BACKSPACE:
                    nombres[actual] = nombres[actual][:-1]
                elif ev.key == pygame.K_RETURN and len(nombres[actual]) >= 1:
                    if actual == 0:
                        estado = 1
                    else:
                        # Crear jugadores
                        fn1, cartas1 = _get_mazo(mazos_idx[0])
                        fn2, cartas2 = _get_mazo(mazos_idx[1])
                        j1 = Jugador(nombres[0], cartas1)
                        j2 = Jugador(nombres[1], cartas2)
                        return j1, j2
                elif ev.key == pygame.K_RIGHT:
                    mazos_idx[actual] = (mazos_idx[actual]+1) % len(MAZOS_FN)
                elif ev.key == pygame.K_LEFT:
                    mazos_idx[actual] = (mazos_idx[actual]-1) % len(MAZOS_FN)
                elif ev.unicode.isprintable() and len(nombres[actual]) < 16:
                    nombres[actual] += ev.unicode

            if ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = ev.pos
                # Mazos
                bw, gap = 180, 10
                total   = len(MAZOS_FN)*bw + (len(MAZOS_FN)-1)*gap
                x0      = (V.ANCHO-total)//2
                for i in range(len(MAZOS_FN)):
                    bx = x0 + i*(bw+gap)
                    r  = pygame.Rect(bx, 320, bw, 75)
                    if r.collidepoint(mx, my):
                        mazos_idx[actual] = i
                # Botón siguiente/jugar
                r_sig = pygame.Rect(V.ANCHO//2-100, V.ALTO-80, 200, 50)
                if r_sig.collidepoint(mx, my) and len(nombres[actual]) >= 1:
                    if actual == 0:
                        estado = 1
                    else:
                        fn1, cartas1 = _get_mazo(mazos_idx[0])
                        fn2, cartas2 = _get_mazo(mazos_idx[1])
                        j1 = Jugador(nombres[0], cartas1)
                        j2 = Jugador(nombres[1], cartas2)
                        return j1, j2
                # Botón mis mazos
                r_mios = pygame.Rect(V.ANCHO//2+110, V.ALTO-80, 160, 50)
                if r_mios.collidepoint(mx, my):
                    resultado = pantalla_mis_mazos()
                    if resultado:
                        _, cartas = resultado
                        # Asignar al jugador actual
                        if actual == 0:
                            mazos_idx[0] = -1
                            _mazo_custom = [cartas, None]
                        else:
                            mazos_idx[1] = -1
                            _mazo_custom = [None, cartas]

        # ── Render ─────────────────────────────────────────
        V.pantalla.fill(V.NEGRO)
        for y in range(V.ALTO):
            t = y/V.ALTO
            pygame.draw.line(V.pantalla,(int(10+15*t),int(20+40*t),int(10+15*t)),(0,y),(V.ANCHO,y))

        # Título
        V.texto(V.pantalla, "👥  2 JUGADORES", V.fuente_titulo, V.DORADO, V.ANCHO//2, 30, centrado=True)

        # Indicador de paso
        for i in range(2):
            cx  = V.ANCHO//2 - 120 + i*240
            col = V.AMARILLO if i == actual else V.GRIS_MED
            pygame.draw.circle(V.pantalla, col, (cx, 85), 12)
            V.texto(V.pantalla, f"J{i+1}", V.fuente_med, V.NEGRO if i==actual else V.GRIS_CLAR,
                    cx, 79, centrado=True)
            if nombres[i]:
                V.texto(V.pantalla, nombres[i], V.fuente_peq, col, cx, 102, centrado=True)
        pygame.draw.line(V.pantalla, V.GRIS_MED, (V.ANCHO//2-100,85),(V.ANCHO//2+100,85), 2)

        # Jugador actual
        num_jug = actual + 1
        col_jug = (20,120,20) if actual==0 else (20,40,150)
        V.texto(V.pantalla, f"Jugador {num_jug} — ingresá tus datos",
                V.fuente_grande, V.AMARILLO, V.ANCHO//2, 130, centrado=True)

        # Campo nombre
        V.texto(V.pantalla, "Tu nombre:", V.fuente_grande, V.BLANCO, V.ANCHO//2, 165, centrado=True)
        r_input = pygame.Rect(V.ANCHO//2-160, 193, 320, 42)
        V.rect_redondeado(V.pantalla, (20,35,20), r_input, 8, 2, V.AMARILLO)
        import time
        cursor = "|" if int(time.time()*2)%2==0 else ""
        V.texto_rect(V.pantalla, nombres[actual]+cursor, V.fuente_grande, V.BLANCO, r_input)

        # Mazos
        V.texto(V.pantalla, "Elegí tu mazo  (← →):", V.fuente_grande, V.BLANCO, V.ANCHO//2, 270, centrado=True)
        bw, gap = 180, 10
        total   = len(MAZOS_FN)*bw + (len(MAZOS_FN)-1)*gap
        x0      = (V.ANCHO-total)//2
        for i, (_, nombre_m, desc, col) in enumerate(MAZOS_FN):
            bx  = x0 + i*(bw+gap)
            r   = pygame.Rect(bx, 300, bw, 75)
            sel = (i == mazos_idx[actual])
            if sel:
                V.rect_redondeado(V.pantalla, V.AMARILLO_OSC, pygame.Rect(bx-2,298,bw+4,79), 10)
            V.rect_redondeado(V.pantalla, col if sel else V.GRIS_OSC, r, 8, 2,
                              V.AMARILLO if sel else V.GRIS_MED)
            V.texto(V.pantalla, nombre_m, V.fuente_med,  V.BLANCO,    bx+bw//2, 313, centrado=True)
            V.texto(V.pantalla, desc,     V.fuente_peq,  V.GRIS_CLAR, bx+bw//2, 336, centrado=True)
            if sel:
                V.texto(V.pantalla, "✓", V.fuente_grande, V.AMARILLO, bx+bw//2, 355, centrado=True)

        # Mazo del otro jugador (si ya eligió)
        otro = 1 - actual
        if nombres[otro]:
            idx_otro  = mazos_idx[otro]
            nom_mazo  = MAZOS_FN[idx_otro][1] if 0 <= idx_otro < len(MAZOS_FN) else "Personalizado"
            V.texto(V.pantalla, f"{nombres[otro]} eligió: {nom_mazo}",
                    V.fuente_peq, V.GRIS_CLAR, V.ANCHO//2, 390, centrado=True)

        # Botones
        r_sig  = pygame.Rect(V.ANCHO//2-100, V.ALTO-80, 200, 50)
        label  = "Siguiente →" if actual==0 else "¡A JUGAR!"
        col_b  = V.VERDE_MED if len(nombres[actual])>=1 else V.GRIS_OSC
        V.rect_redondeado(V.pantalla, col_b, r_sig, 8, 2, V.AMARILLO)
        V.texto_rect(V.pantalla, label, V.fuente_grande, V.BLANCO, r_sig)

        r_mios = pygame.Rect(V.ANCHO//2+110, V.ALTO-80, 160, 50)
        V.rect_redondeado(V.pantalla, (100,60,20), r_mios, 8, 2, V.NARANJA)
        V.texto_rect(V.pantalla, "🛠 Mis mazos", V.fuente_med, V.BLANCO, r_mios)

        r_volver = pygame.Rect(V.ANCHO//2-270, V.ALTO-80, 160, 50)
        V.rect_redondeado(V.pantalla, V.GRIS_OSC, r_volver, 8, 2, V.GRIS_MED)
        V.texto_rect(V.pantalla, "← Volver", V.fuente_med, V.BLANCO, r_volver)
        for ev2 in pygame.event.get(pygame.MOUSEBUTTONDOWN):
            if pygame.Rect(V.ANCHO//2-270,V.ALTO-80,160,50).collidepoint(ev2.pos):
                return None

        pygame.display.flip()
        V.reloj.tick(V.FPS)


def _get_mazo(idx):
    if 0 <= idx < len(MAZOS_FN):
        fn = MAZOS_FN[idx][0]
        return fn, fn()
    return get_mazo_oriental, get_mazo_oriental()


# ── Bucle de juego 2 jugadores ─────────────────────────────

def jugar_2j(j1, j2, turno_jugador_fn, fase_batalla_fn):
    """
    Bucle principal para 2 jugadores.
    Alterna turnos entre j1 y j2.
    turno_jugador_fn: función que maneja el turno de un jugador humano
    """
    turno    = 1
    jugadores = [j1, j2]

    while j1.esta_vivo() and j2.esta_vivo():
        actual   = jugadores[(turno-1) % 2]
        rival    = jugadores[turno % 2]

        turno_jugador_fn(actual, rival, turno)
        if not rival.esta_vivo():
            break

        turno += 1

    ganador  = j1.nombre if j1.esta_vivo() else j2.nombre
    perdedor = j2.nombre if j1.esta_vivo() else j1.nombre
    V.log_add(f"🏆 ¡{ganador} gana la partida!")
    V.render(j1 if j1.esta_vivo() else j2,
             j2 if j1.esta_vivo() else j1, turno, "FIN")
    pygame.time.wait(1000)
    V.pantalla_fin(ganador, perdedor)
