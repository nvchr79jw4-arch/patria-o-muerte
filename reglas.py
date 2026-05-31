# reglas.py
# ─────────────────────────────────────────────────────────────
#  PATRIA O MUERTE — Pantalla de reglas
# ─────────────────────────────────────────────────────────────

import pygame
import sys
import ventana as V

# ── Contenido de las reglas ────────────────────────────────

PAGINAS = [
    {
        "titulo": "¿Cómo se juega?",
        "contenido": [
            "El objetivo es reducir los HP del rival de 25 a 0.",
            "",
            "Cada turno tenés 2 Puntos de Acción (PA).",
            "Usá los PA para jugar cartas de tu mano.",
            "",
            "Al final de tu turno, tus criaturas atacan",
            "automáticamente al carril rival enfrentado.",
            "",
            "El juego termina cuando alguien llega a 0 HP.",
            "El ganador es el COOL GUY.",
            "El perdedor es el DWEEB.",
        ],
        "icono": "🇺🇾"
    },
    {
        "titulo": "Tipos de cartas",
        "contenido": [
            "⚔  CRIATURA  (verde)",
            "   Se coloca en un carril del campo.",
            "   Tiene ATK (ataque) y DEF (defensa).",
            "   Pelea contra la criatura del carril opuesto.",
            "",
            "✨  HECHIZO  (azul)",
            "   Efecto inmediato y va al descarte.",
            "   No ocupa carril.",
            "",
            "🏛  EDIFICIO  (naranja)",
            "   Se coloca en un carril.",
            "   Da ventajas pasivas a tus criaturas.",
        ],
        "icono": "🃏"
    },
    {
        "titulo": "El sistema de carriles",
        "contenido": [
            "El tablero tiene 4 carriles por jugador.",
            "",
            "Carril 1 enfrenta al Carril 1 del rival.",
            "Carril 2 enfrenta al Carril 2 del rival.",
            "...y así sucesivamente.",
            "",
            "Si atacás un carril VACÍO del rival,",
            "el daño va directo a sus HP.",
            "",
            "Solo puede haber UNA criatura por carril.",
            "Pero sí podés tener criatura + edificio juntos.",
        ],
        "icono": "⚔"
    },
    {
        "titulo": "El FLOOP",
        "contenido": [
            "Algunas criaturas tienen habilidad FLOOP.",
            "Se indica con ✨ en la carta.",
            "",
            "Para usar el FLOOP:",
            "1. Apretá el botón 'FLOOP'",
            "2. Elegí qué criatura floopás",
            "",
            "Cada criatura solo puede usar FLOOP",
            "una vez por turno.",
            "",
            "Ejemplos de FLOOP:",
            "  El Gaucho → +2 ATK este turno",
            "  Artigas   → todas las criaturas aliadas +1 ATK",
            "  El Crack  → esquiva el próximo ataque",
        ],
        "icono": "✨"
    },
    {
        "titulo": "Los mazos",
        "contenido": [
            "MAZO ORIENTAL — Folklore y campo",
            "  El Gaucho, Artigas, La Payadora...",
            "  Estilo: agresivo y resistente.",
            "  Fuerte en combate directo.",
            "",
            "MAZO URUGUAYO — Ciudad y cultura",
            "  El Crack, El Murguero, El Chivito...",
            "  Estilo: ágil y con efectos especiales.",
            "  Fuerte en hechizos y FLOOP.",
            "",
            "La IA usa el mazo contrario al tuyo.",
        ],
        "icono": "📚"
    },
    {
        "titulo": "Consejos",
        "contenido": [
            "💡 Llenás los 4 carriles = más daño por turno.",
            "",
            "💡 Los edificios dan ventajas pasivas,",
            "   construilos temprano.",
            "",
            "💡 Usá hechizos para eliminar criaturas",
            "   fuertes antes de que ataquen.",
            "",
            "💡 El FLOOP de Artigas es muy poderoso,",
            "   usalo cuando tengas muchas criaturas.",
            "",
            "💡 Si el rival tiene un carril vacío,",
            "   mandá tu criatura más fuerte ahí.",
            "",
            "¡Buena suerte, orientale! 🇺🇾",
        ],
        "icono": "💡"
    },
]

# ── Pantalla de reglas ─────────────────────────────────────

def mostrar_reglas():
    """Muestra la pantalla de reglas. Devuelve cuando el usuario sale."""
    pagina_actual = 0
    total_paginas = len(PAGINAS)

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_ESCAPE, pygame.K_q):
                    return
                if ev.key in (pygame.K_RIGHT, pygame.K_d):
                    pagina_actual = min(pagina_actual + 1, total_paginas - 1)
                if ev.key in (pygame.K_LEFT, pygame.K_a):
                    pagina_actual = max(pagina_actual - 1, 0)
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = ev.pos
                # Botón siguiente
                r_sig = pygame.Rect(V.ANCHO - 160, V.ALTO - 70, 140, 45)
                if r_sig.collidepoint(mx, my):
                    if pagina_actual < total_paginas - 1:
                        pagina_actual += 1
                    else:
                        return
                # Botón anterior
                r_ant = pygame.Rect(20, V.ALTO - 70, 140, 45)
                if r_ant.collidepoint(mx, my) and pagina_actual > 0:
                    pagina_actual -= 1
                # Botón salir
                r_sal = pygame.Rect(V.ANCHO//2 - 70, V.ALTO - 70, 140, 45)
                if r_sal.collidepoint(mx, my):
                    return

        _dibujar_pagina(pagina_actual, total_paginas)
        pygame.display.flip()
        V.reloj.tick(V.FPS)


def _dibujar_pagina(idx, total):
    pagina = PAGINAS[idx]

    # Fondo
    V.pantalla.fill(V.NEGRO)
    fondo = pygame.Rect(0, 0, V.ANCHO, V.ALTO)
    for y in range(V.ALTO):
        t   = y / V.ALTO
        col = (int(10+10*t), int(20+40*t), int(10+10*t))
        pygame.draw.line(V.pantalla, col, (0,y), (V.ANCHO,y))

    # Panel central
    panel = pygame.Rect(60, 60, V.ANCHO-120, V.ALTO-150)
    V.rect_redondeado(V.pantalla, (20,30,20), panel, 12, 2, V.VERDE_MED)

    # Icono grande
    V.texto(V.pantalla, pagina["icono"], V.fuente_titulo,
            V.DORADO, V.ANCHO//2, 85, centrado=True)

    # Título
    V.texto(V.pantalla, pagina["titulo"], V.fuente_titulo,
            V.DORADO, V.ANCHO//2, 130, centrado=True)

    # Línea decorativa
    pygame.draw.line(V.pantalla, V.VERDE_MED,
                     (120, 170), (V.ANCHO-120, 170), 2)

    # Contenido
    y_texto = 190
    for linea in pagina["contenido"]:
        if linea == "":
            y_texto += 10
            continue
        # Detectar si es encabezado (empieza con icono)
        es_encabezado = linea and linea[0] in "⚔✨🏛💡📚🇺🇾"
        color  = V.AMARILLO if es_encabezado else V.BLANCO
        fuente = V.fuente_grande if es_encabezado else V.fuente_med
        V.texto(V.pantalla, linea, fuente, color, 100, y_texto)
        y_texto += 28 if es_encabezado else 22

    # Indicador de página
    V.texto(V.pantalla, f"Página {idx+1} de {total}",
            V.fuente_peq, V.GRIS_CLAR, V.ANCHO//2, V.ALTO-110, centrado=True)

    # Puntitos de navegación
    for i in range(total):
        col = V.AMARILLO if i == idx else V.GRIS_MED
        pygame.draw.circle(V.pantalla, col,
                          (V.ANCHO//2 - (total//2 - i)*20, V.ALTO-90), 5)

    # Botones
    # Anterior
    if idx > 0:
        r_ant = pygame.Rect(20, V.ALTO-70, 140, 45)
        V.rect_redondeado(V.pantalla, V.GRIS_OSC, r_ant, 8, 2, V.GRIS_MED)
        V.texto_rect(V.pantalla, "← Anterior", V.fuente_med, V.BLANCO, r_ant)

    # Siguiente / Cerrar
    r_sig = pygame.Rect(V.ANCHO-160, V.ALTO-70, 140, 45)
    if idx < total - 1:
        V.rect_redondeado(V.pantalla, V.VERDE_MED, r_sig, 8, 2, V.VERDE_CLAR)
        V.texto_rect(V.pantalla, "Siguiente →", V.fuente_med, V.BLANCO, r_sig)
    else:
        V.rect_redondeado(V.pantalla, V.ROJO_OSC, r_sig, 8, 2, V.ROJO_CLAR)
        V.texto_rect(V.pantalla, "¡A jugar! →", V.fuente_med, V.BLANCO, r_sig)

    # Salir
    r_sal = pygame.Rect(V.ANCHO//2-70, V.ALTO-70, 140, 45)
    V.rect_redondeado(V.pantalla, V.GRIS_OSC, r_sal, 8, 2, V.GRIS_MED)
    V.texto_rect(V.pantalla, "Salir [ESC]", V.fuente_med, V.BLANCO, r_sal)
