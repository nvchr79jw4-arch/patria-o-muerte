# efectos.py
# ─────────────────────────────────────────────────────────────
#  PATRIA O MUERTE — Efectos visuales y transiciones
# ─────────────────────────────────────────────────────────────

import pygame
import math
import random
import ventana as V

# ════════════════════════════════════════════════════════════
#  TRANSICIONES FADE
# ════════════════════════════════════════════════════════════

def fade_out(duracion=25):
    """Oscurece la pantalla gradualmente."""
    overlay = pygame.Surface((V.ANCHO, V.ALTO))
    overlay.fill((0, 0, 0))
    for i in range(duracion):
        alpha = int(255 * i / duracion)
        overlay.set_alpha(alpha)
        V.pantalla.blit(overlay, (0, 0))
        pygame.display.flip()
        V.reloj.tick(V.FPS)
        pygame.event.pump()

def fade_in(duracion=25):
    """Aclara la pantalla gradualmente."""
    overlay = pygame.Surface((V.ANCHO, V.ALTO))
    overlay.fill((0, 0, 0))
    for i in range(duracion, -1, -1):
        alpha = int(255 * i / duracion)
        overlay.set_alpha(alpha)
        V.pantalla.blit(overlay, (0, 0))
        pygame.display.flip()
        V.reloj.tick(V.FPS)
        pygame.event.pump()

def fade_negro(duracion=20):
    """Fade completo a negro."""
    fade_out(duracion)

def fade_desde_negro(render_fn, duracion=20):
    """
    Renderiza la escena y hace fade desde negro.
    render_fn: función que dibuja la pantalla actual.
    """
    render_fn()
    fade_in(duracion)


# ════════════════════════════════════════════════════════════
#  PARTÍCULAS
# ════════════════════════════════════════════════════════════

class Particula:
    def __init__(self, x, y, color, vel_x=None, vel_y=None, vida=None, radio=None):
        self.x     = float(x)
        self.y     = float(y)
        self.color = color
        self.vx    = vel_x if vel_x is not None else random.uniform(-3, 3)
        self.vy    = vel_y if vel_y is not None else random.uniform(-4, -1)
        self.vida  = vida  if vida  is not None else random.randint(20, 40)
        self.vida_max = self.vida
        self.radio = radio if radio is not None else random.randint(2, 5)
        self.gravedad = 0.15

    def update(self):
        self.x  += self.vx
        self.y  += self.vy
        self.vy += self.gravedad
        self.vida -= 1

    def draw(self, surf):
        if self.vida <= 0:
            return
        alpha = int(255 * self.vida / self.vida_max)
        r     = max(1, int(self.radio * self.vida / self.vida_max))
        s     = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, alpha), (r, r), r)
        surf.blit(s, (int(self.x)-r, int(self.y)-r))

    def viva(self):
        return self.vida > 0


_particulas = []

def emitir_particulas(x, y, color, cantidad=15, tipo="explosion"):
    for _ in range(cantidad):
        if tipo == "explosion":
            angulo = random.uniform(0, math.pi*2)
            speed  = random.uniform(2, 6)
            p = Particula(x, y, color,
                          vel_x=math.cos(angulo)*speed,
                          vel_y=math.sin(angulo)*speed - 2,
                          vida=random.randint(25, 45))
        elif tipo == "chispa":
            p = Particula(x, y, color,
                          vel_x=random.uniform(-2, 2),
                          vel_y=random.uniform(-5, -2),
                          radio=random.randint(1, 3),
                          vida=random.randint(15, 30))
        elif tipo == "lluvia":
            p = Particula(x + random.randint(-30, 30), y,
                          color,
                          vel_x=random.uniform(-0.5, 0.5),
                          vel_y=random.uniform(2, 5),
                          vida=random.randint(20, 35))
        elif tipo == "confeti":
            p = Particula(x + random.randint(-100, 100),
                          y - random.randint(0, 50),
                          random.choice([(220,50,50),(50,220,50),(50,50,220),
                                         (220,220,50),(220,50,220)]),
                          vel_x=random.uniform(-3, 3),
                          vel_y=random.uniform(-2, 2),
                          radio=random.randint(3, 6),
                          vida=random.randint(40, 80))
        _particulas.append(p)

def actualizar_particulas(surf):
    global _particulas
    for p in _particulas:
        p.update()
        p.draw(surf)
    _particulas = [p for p in _particulas if p.viva()]

def limpiar_particulas():
    global _particulas
    _particulas = []


# ════════════════════════════════════════════════════════════
#  FONDO ANIMADO DEL MENÚ
# ════════════════════════════════════════════════════════════

class FondoAnimado:
    """Fondo del menú con estrellas y elementos flotantes."""

    def __init__(self):
        self.tick     = 0
        self.estrellas = [
            {
                'x': random.randint(0, V.ANCHO),
                'y': random.randint(0, V.ALTO),
                'r': random.uniform(0.5, 2.5),
                'speed': random.uniform(0.2, 0.8),
                'fase': random.uniform(0, math.pi*2),
            }
            for _ in range(80)
        ]
        self.particulas_menu = []
        self._emit_timer = 0

    def update(self):
        self.tick += 1
        self._emit_timer += 1
        # Emitir partículas decorativas cada 8 frames
        if self._emit_timer >= 8:
            self._emit_timer = 0
            x = random.randint(50, V.ANCHO-50)
            col = random.choice([
                (20,120,20), (40,80,160), (180,140,20),
                (120,20,20), (20,100,100)
            ])
            self.particulas_menu.append(
                Particula(x, V.ALTO + 10, col,
                          vel_x=random.uniform(-0.5, 0.5),
                          vel_y=random.uniform(-1.5, -0.5),
                          radio=random.randint(2, 4),
                          vida=random.randint(60, 120))
            )
        for p in self.particulas_menu:
            p.update()
        self.particulas_menu = [p for p in self.particulas_menu if p.viva()]

    def draw(self, surf):
        # Fondo degradado
        for y in range(V.ALTO):
            t   = y / V.ALTO
            col = (int(5+10*t), int(10+20*t), int(5+10*t))
            pygame.draw.line(surf, col, (0,y), (V.ANCHO,y))

        # Estrellas parpadeantes
        for e in self.estrellas:
            brillo = 0.5 + 0.5 * math.sin(self.tick * e['speed'] + e['fase'])
            alpha  = int(80 + 120 * brillo)
            r      = max(1, int(e['r'] * (0.7 + 0.3 * brillo)))
            s      = pygame.Surface((r*2+2, r*2+2), pygame.SRCALPHA)
            pygame.draw.circle(s, (200, 200, 180, alpha), (r+1, r+1), r)
            surf.blit(s, (int(e['x'])-r, int(e['y'])-r))

        # Partículas decorativas
        for p in self.particulas_menu:
            p.draw(surf)

        # Sol de Artigas animado (centro)
        self._dibujar_sol(surf, V.ANCHO//2, 200)

    def _dibujar_sol(self, surf, cx, cy):
        t = self.tick
        r = 30 + int(4 * math.sin(t * 0.05))
        # Halo exterior
        for i in range(3):
            radio_halo = r + 20 + i*12
            alpha      = 30 - i*8
            s = pygame.Surface((radio_halo*2, radio_halo*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (200,170,30,alpha), (radio_halo,radio_halo), radio_halo)
            surf.blit(s, (cx-radio_halo, cy-radio_halo))
        # Sol
        pygame.draw.circle(surf, (200,160,30), (cx,cy), r)
        pygame.draw.circle(surf, (180,140,20), (cx,cy), r, 2)
        # Rayos giratorios
        for i in range(16):
            ang  = (i/16)*math.pi*2 + t*0.02
            long = r+15 if i%2==0 else r+8
            x1   = int(cx + (r+3)*math.cos(ang))
            y1   = int(cy + (r+3)*math.sin(ang))
            x2   = int(cx + long*math.cos(ang))
            y2   = int(cy + long*math.sin(ang))
            pygame.draw.line(surf, (160,130,20), (x1,y1),(x2,y2), 2)
        # Cara del sol
        ojo_x = 8
        pygame.draw.circle(surf, (140,100,10), (cx-ojo_x, cy-5), 4)
        pygame.draw.circle(surf, (140,100,10), (cx+ojo_x, cy-5), 4)
        pygame.draw.circle(surf, (220,200,100),(cx-ojo_x, cy-6), 2)
        pygame.draw.circle(surf, (220,200,100),(cx+ojo_x, cy-6), 2)
        pygame.draw.arc(surf, (140,100,10),
                        pygame.Rect(cx-8, cy+2, 16, 8), math.pi, 0, 2)


# ════════════════════════════════════════════════════════════
#  LOGO ANIMADO
# ════════════════════════════════════════════════════════════

def dibujar_logo(surf, tick, y=260):
    """Dibuja el título animado con efecto de brillo."""
    # Sombra
    sombra = V.fuente_titulo.render("PATRIA O MUERTE", True, (20,50,20))
    surf.blit(sombra, (V.ANCHO//2 - sombra.get_width()//2 + 2, y+2))

    # Texto principal con color pulsante
    brillo = 0.7 + 0.3 * math.sin(tick * 0.04)
    col    = (int(200*brillo+20), int(160*brillo+10), int(30*brillo))
    titulo = V.fuente_titulo.render("PATRIA O MUERTE", True, col)
    surf.blit(titulo, (V.ANCHO//2 - titulo.get_width()//2, y))

    # Subtítulo
    sub = V.fuente_grande.render("El juego de cartas uruguayo", True, V.CREMA)
    surf.blit(sub, (V.ANCHO//2 - sub.get_width()//2, y+50))

    # Banderitas decorativas
    V.texto(surf, "🇺🇾", V.fuente_titulo, V.BLANCO,
            V.ANCHO//2 - titulo.get_width()//2 - 60, y)
    V.texto(surf, "🇺🇾", V.fuente_titulo, V.BLANCO,
            V.ANCHO//2 + titulo.get_width()//2 + 10, y)


# ════════════════════════════════════════════════════════════
#  NOTIFICACIONES FLOTANTES
# ════════════════════════════════════════════════════════════

class Notificacion:
    def __init__(self, texto, color=None, y_inicio=None):
        self.texto   = texto
        self.color   = color or V.AMARILLO
        self.y       = y_inicio or V.ALTO//2
        self.alpha   = 255
        self.vida    = 90
        self.vida_max= 90

    def update(self):
        self.vida  -= 1
        self.y     -= 0.8
        if self.vida < 30:
            self.alpha = int(255 * self.vida / 30)

    def draw(self, surf):
        if self.vida <= 0:
            return
        s   = V.fuente_grande.render(self.texto, True, self.color)
        img = pygame.Surface(s.get_size(), pygame.SRCALPHA)
        img.fill((0,0,0,0))
        img.blit(s, (0,0))
        img.set_alpha(self.alpha)
        surf.blit(img, (V.ANCHO//2 - s.get_width()//2, int(self.y)))

    def viva(self):
        return self.vida > 0


_notificaciones = []

def agregar_notificacion(texto, color=None, y=None):
    _notificaciones.append(Notificacion(texto, color, y))

def actualizar_notificaciones(surf):
    global _notificaciones
    for n in _notificaciones:
        n.update()
        n.draw(surf)
    _notificaciones = [n for n in _notificaciones if n.viva()]


# ════════════════════════════════════════════════════════════
#  PANTALLA DE FIN MEJORADA
# ════════════════════════════════════════════════════════════

def pantalla_fin_epica(ganador, perdedor):
    """Pantalla de fin de juego con confeti y efectos."""
    tick      = 0
    confeti_emitido = False

    while True:
        tick += 1
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return False
            if ev.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                fade_negro(15)
                return True

        # Fondo
        V.pantalla.fill(V.NEGRO)
        for y in range(V.ALTO):
            t = y/V.ALTO
            pygame.draw.line(V.pantalla,(int(5+10*t),int(10+15*t),int(5+5*t)),(0,y),(V.ANCHO,y))

        # Confeti
        if tick == 10:
            for i in range(8):
                emitir_particulas(random.randint(100, V.ANCHO-100),
                                  V.ALTO//3, V.AMARILLO, 20, "confeti")
        if tick % 30 == 0 and tick < 200:
            emitir_particulas(random.randint(50, V.ANCHO-50),
                              V.ALTO//4, (220,180,30), 15, "confeti")

        actualizar_particulas(V.pantalla)

        # Panel central
        panel = pygame.Rect(V.ANCHO//2-350, V.ALTO//2-160, 700, 320)
        s = pygame.Surface((700,320), pygame.SRCALPHA)
        s.fill((0,0,0,180))
        V.pantalla.blit(s, (V.ANCHO//2-350, V.ALTO//2-160))
        pygame.draw.rect(V.pantalla, V.DORADO, panel, 3, border_radius=16)

        # Trofeo pulsante
        escala = 1.0 + 0.05 * math.sin(tick * 0.1)
        V.texto(V.pantalla, "🏆", V.fuente_titulo, V.DORADO,
                V.ANCHO//2, V.ALTO//2 - 140, centrado=True)

        # Nombre ganador
        brillo = 0.7 + 0.3 * math.sin(tick * 0.06)
        col_g  = (int(100+120*brillo), int(200+50*brillo), int(80+50*brillo))
        V.texto(V.pantalla, f"¡{ganador} GANA!", V.fuente_titulo, col_g,
                V.ANCHO//2, V.ALTO//2 - 80, centrado=True)
        V.texto(V.pantalla, "¡Es el COOL GUY! 😎", V.fuente_grande, V.AMARILLO,
                V.ANCHO//2, V.ALTO//2 - 30, centrado=True)

        # Perdedor
        V.texto(V.pantalla, f"{perdedor} es el DWEEB 😔", V.fuente_grande,
                V.ROJO_CLAR, V.ANCHO//2, V.ALTO//2 + 20, centrado=True)

        # Instrucción parpadeante
        if tick % 60 < 40:
            V.texto(V.pantalla, "Click o cualquier tecla para continuar",
                    V.fuente_med, V.GRIS_CLAR, V.ANCHO//2, V.ALTO//2 + 110, centrado=True)

        pygame.display.flip()
        V.reloj.tick(V.FPS)
