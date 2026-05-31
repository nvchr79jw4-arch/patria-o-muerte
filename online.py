# online.py
# ─────────────────────────────────────────────────────────────
#  PATRIA O MUERTE — Cliente de multijugador online
# ─────────────────────────────────────────────────────────────

import pygame
import sys
import asyncio
import websockets
import json
import threading
import time
import copy

import ventana as V
from jugador import Jugador
from carta   import Carta

# ── Configuración ──────────────────────────────────────────
SERVIDOR_LOCAL   = "ws://localhost:8765"
SERVIDOR_RAILWAY = ""  # se llena cuando subas a Railway

# ── Estado de conexión ─────────────────────────────────────

class ClienteOnline:
    def __init__(self):
        self.ws           = None
        self.loop         = None
        self.thread       = None
        self.conectado    = False
        self.mensajes     = []   # cola de mensajes recibidos
        self.mi_idx       = -1   # 0 = jugador 1, 1 = jugador 2
        self.codigo_sala  = ""
        self.error        = ""
        self._lock        = threading.Lock()

    def encolar(self, msg):
        with self._lock:
            self.mensajes.append(msg)

    def leer_mensajes(self):
        with self._lock:
            msgs = self.mensajes[:]
            self.mensajes = []
        return msgs

    def enviar(self, datos):
        if self.ws and self.conectado:
            asyncio.run_coroutine_threadsafe(
                self.ws.send(json.dumps(datos)),
                self.loop
            )

    async def _conectar(self, url):
        try:
            async with websockets.connect(url, ping_timeout=10) as ws:
                self.ws        = ws
                self.conectado = True
                async for msg in ws:
                    try:
                        datos = json.loads(msg)
                        self.encolar(datos)
                    except:
                        pass
        except Exception as e:
            self.error     = str(e)
            self.conectado = False

    def conectar(self, url):
        self.loop   = asyncio.new_event_loop()
        self.thread = threading.Thread(
            target=lambda: self.loop.run_until_complete(self._conectar(url)),
            daemon=True
        )
        self.thread.start()

    def desconectar(self):
        self.conectado = False
        if self.ws:
            asyncio.run_coroutine_threadsafe(self.ws.close(), self.loop)


# ── Pantalla de conexión online ────────────────────────────

def pantalla_online(nombre_jugador, mazo_cartas):
    """
    Pantalla para crear o unirse a una sala online.
    Devuelve (cliente, mi_idx, nombres, mazos) o None si cancela.
    """
    cliente    = ClienteOnline()
    modo       = None    # "crear" o "unirse"
    codigo_inp = ""
    estado     = "menu"  # menu, conectando, esperando, error
    mensaje_estado = ""
    usar_local = True    # True = local WiFi, False = internet
    tick       = 0

    while True:
        tick += 1
        msgs = cliente.leer_mensajes()

        for msg in msgs:
            tipo = msg.get("tipo")

            if tipo == "sala_creada":
                cliente.codigo_sala = msg["codigo"]
                estado = "esperando"
                mensaje_estado = f"Sala creada: {msg['codigo']} — esperando rival..."
                # Enviar datos del jugador
                cliente.enviar({
                    "tipo":   "unirse",
                    "nombre": nombre_jugador,
                    "mazo":   _serializar_mazo(mazo_cartas),
                })

            elif tipo == "sala_unida":
                cliente.codigo_sala = msg["codigo"]
                estado = "esperando"
                mensaje_estado = "Conectado a la sala — esperando inicio..."
                cliente.enviar({
                    "tipo":   "unirse",
                    "nombre": nombre_jugador,
                    "mazo":   _serializar_mazo(mazo_cartas),
                })

            elif tipo == "unido":
                cliente.mi_idx = msg["idx"]

            elif tipo == "inicio":
                # ¡Partida lista!
                return cliente, msg

            elif tipo == "error":
                estado         = "error"
                mensaje_estado = msg.get("msg", "Error desconocido")
                cliente.desconectar()
                cliente        = ClienteOnline()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    cliente.desconectar()
                    return None
                if ev.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                if estado == "menu" and modo == "unirse":
                    if ev.key == pygame.K_BACKSPACE:
                        codigo_inp = codigo_inp[:-1]
                    elif ev.key == pygame.K_RETURN and len(codigo_inp) >= 4:
                        _conectar_y_unirse(cliente, codigo_inp, usar_local)
                        estado = "conectando"
                        mensaje_estado = "Conectando..."
                    elif ev.unicode.isalnum() and len(codigo_inp) < 6:
                        codigo_inp += ev.unicode.upper()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = ev.pos

                if estado == "menu":
                    # Toggle local/internet
                    r_local = pygame.Rect(V.ANCHO//2 - 220, 180, 200, 45)
                    r_inet  = pygame.Rect(V.ANCHO//2 + 20,  180, 200, 45)
                    if r_local.collidepoint(mx, my): usar_local = True
                    if r_inet.collidepoint(mx, my):  usar_local = False

                    # Botón crear sala
                    r_crear = pygame.Rect(V.ANCHO//2 - 220, 280, 200, 55)
                    if r_crear.collidepoint(mx, my):
                        modo = "crear"
                        _conectar_y_crear(cliente, usar_local)
                        estado = "conectando"
                        mensaje_estado = "Conectando al servidor..."

                    # Botón unirse
                    r_unir = pygame.Rect(V.ANCHO//2 + 20, 280, 200, 55)
                    if r_unir.collidepoint(mx, my):
                        modo = "unirse"

                    # Si está en modo unirse y aprieta confirmar
                    if modo == "unirse":
                        r_conf = pygame.Rect(V.ANCHO//2 - 100, 420, 200, 50)
                        if r_conf.collidepoint(mx, my) and len(codigo_inp) >= 4:
                            _conectar_y_unirse(cliente, codigo_inp, usar_local)
                            estado = "conectando"
                            mensaje_estado = "Conectando..."

                # Botón volver
                r_volver = pygame.Rect(V.ANCHO//2 - 100, V.ALTO - 70, 200, 45)
                if r_volver.collidepoint(mx, my):
                    cliente.desconectar()
                    return None

        # ── Render ─────────────────────────────────────────
        V.pantalla.fill(V.NEGRO)
        for y in range(V.ALTO):
            t = y/V.ALTO
            pygame.draw.line(V.pantalla,(int(10+15*t),int(20+40*t),int(10+15*t)),(0,y),(V.ANCHO,y))

        V.texto(V.pantalla, "🌐  MULTIJUGADOR ONLINE", V.fuente_titulo,
                V.DORADO, V.ANCHO//2, 35, centrado=True)
        pygame.draw.line(V.pantalla, V.VERDE_MED, (100,85),(V.ANCHO-100,85), 1)

        if estado == "menu":
            # Toggle local/internet
            V.texto(V.pantalla, "Conectar a:", V.fuente_grande, V.BLANCO, V.ANCHO//2, 145, centrado=True)
            r_local = pygame.Rect(V.ANCHO//2 - 220, 170, 200, 45)
            r_inet  = pygame.Rect(V.ANCHO//2 + 20,  170, 200, 45)
            V.rect_redondeado(V.pantalla, V.VERDE_MED if usar_local else V.GRIS_OSC,
                              r_local, 8, 2, V.AMARILLO if usar_local else V.GRIS_MED)
            V.rect_redondeado(V.pantalla, V.AZUL_MED if not usar_local else V.GRIS_OSC,
                              r_inet,  8, 2, V.AMARILLO if not usar_local else V.GRIS_MED)
            V.texto_rect(V.pantalla, "📶 WiFi local", V.fuente_med, V.BLANCO, r_local)
            V.texto_rect(V.pantalla, "🌐 Internet",   V.fuente_med, V.BLANCO, r_inet)

            if not usar_local and not SERVIDOR_RAILWAY:
                V.texto(V.pantalla, "⚠ Configurá SERVIDOR_RAILWAY en online.py",
                        V.fuente_peq, V.ROJO_CLAR, V.ANCHO//2, 225, centrado=True)

            # Botones crear/unirse
            r_crear = pygame.Rect(V.ANCHO//2 - 220, 260, 200, 55)
            r_unir  = pygame.Rect(V.ANCHO//2 + 20,  260, 200, 55)
            V.rect_redondeado(V.pantalla, V.VERDE_MED, r_crear, 8, 2, V.VERDE_CLAR)
            V.rect_redondeado(V.pantalla, (60,20,120), r_unir,  8, 2, V.MORADO_CLAR)
            V.texto_rect(V.pantalla, "➕ Crear sala",  V.fuente_grande, V.BLANCO, r_crear)
            V.texto_rect(V.pantalla, "🚪 Unirse",      V.fuente_grande, V.BLANCO, r_unir)

            # Info
            V.texto(V.pantalla, "Crear sala: compartí el código con tu rival",
                    V.fuente_peq, V.GRIS_CLAR, V.ANCHO//2, 330, centrado=True)
            V.texto(V.pantalla, "Unirse: ingresá el código que te dió tu rival",
                    V.fuente_peq, V.GRIS_CLAR, V.ANCHO//2, 350, centrado=True)

            # Campo código (si está en modo unirse)
            if modo == "unirse":
                V.texto(V.pantalla, "Código de sala:", V.fuente_grande,
                        V.BLANCO, V.ANCHO//2, 385, centrado=True)
                r_cod = pygame.Rect(V.ANCHO//2 - 120, 408, 240, 45)
                V.rect_redondeado(V.pantalla, V.GRIS_OSC, r_cod, 8, 2, V.AMARILLO)
                cursor = "|" if tick % 60 < 30 else ""
                V.texto_rect(V.pantalla, codigo_inp + cursor, V.fuente_titulo, V.BLANCO, r_cod)
                r_conf = pygame.Rect(V.ANCHO//2 - 100, 465, 200, 45)
                col_c  = V.VERDE_MED if len(codigo_inp) >= 4 else V.GRIS_OSC
                V.rect_redondeado(V.pantalla, col_c, r_conf, 8, 2, V.VERDE_CLAR)
                V.texto_rect(V.pantalla, "Conectar →", V.fuente_grande, V.BLANCO, r_conf)

        elif estado in ("conectando", "esperando"):
            # Spinner animado
            for i in range(8):
                ang   = (i/8)*3.14159*2 + tick*0.1
                alpha = int(255 * (i/8))
                r_sp  = int(30 + 5*pygame.math.Vector2(1,0).rotate(tick*3).x)
                px    = int(V.ANCHO//2 + 60*pygame.math.Vector2(1,0).rotate(i*45).x)
                py    = int(V.ALTO//2  - 60 + 60*pygame.math.Vector2(1,0).rotate(i*45).y)
                s     = pygame.Surface((12,12), pygame.SRCALPHA)
                pygame.draw.circle(s, (*V.VERDE_CLAR, alpha), (6,6), 6)
                V.pantalla.blit(s, (px-6, py-6))

            V.texto(V.pantalla, mensaje_estado, V.fuente_grande,
                    V.BLANCO, V.ANCHO//2, V.ALTO//2 + 20, centrado=True)

            # Mostrar código si ya fue creada la sala
            if cliente.codigo_sala:
                V.texto(V.pantalla, "Código de sala:", V.fuente_grande,
                        V.GRIS_CLAR, V.ANCHO//2, V.ALTO//2 + 70, centrado=True)
                V.texto(V.pantalla, cliente.codigo_sala, V.fuente_titulo,
                        V.AMARILLO, V.ANCHO//2, V.ALTO//2 + 100, centrado=True)
                V.texto(V.pantalla, "Compartí este código con tu rival",
                        V.fuente_peq, V.GRIS_CLAR, V.ANCHO//2, V.ALTO//2 + 145, centrado=True)

        elif estado == "error":
            V.texto(V.pantalla, "❌ Error de conexión", V.fuente_titulo,
                    V.ROJO_CLAR, V.ANCHO//2, V.ALTO//2 - 40, centrado=True)
            V.texto(V.pantalla, mensaje_estado, V.fuente_med,
                    V.GRIS_CLAR, V.ANCHO//2, V.ALTO//2 + 10, centrado=True)
            estado = "menu"
            modo   = None

        # Botón volver
        r_volver = pygame.Rect(V.ANCHO//2 - 100, V.ALTO - 70, 200, 45)
        V.rect_redondeado(V.pantalla, V.GRIS_OSC, r_volver, 8, 2, V.GRIS_MED)
        V.texto_rect(V.pantalla, "← Volver", V.fuente_med, V.BLANCO, r_volver)

        pygame.display.flip()
        V.reloj.tick(V.FPS)


def _conectar_y_crear(cliente, usar_local):
    url = SERVIDOR_LOCAL if usar_local else SERVIDOR_RAILWAY
    cliente.conectar(url)
    # Esperar conexión y crear sala
    def _crear():
        tiempo = 0
        while not cliente.conectado and tiempo < 50:
            time.sleep(0.1)
            tiempo += 1
        if cliente.conectado:
            cliente.enviar({"tipo": "crear_sala"})
    threading.Thread(target=_crear, daemon=True).start()

def _conectar_y_unirse(cliente, codigo, usar_local):
    url = SERVIDOR_LOCAL if usar_local else SERVIDOR_RAILWAY
    cliente.conectar(url)
    def _unir():
        tiempo = 0
        while not cliente.conectado and tiempo < 50:
            time.sleep(0.1)
            tiempo += 1
        if cliente.conectado:
            cliente.enviar({"tipo": "unirse_sala", "codigo": codigo})
    threading.Thread(target=_unir, daemon=True).start()

def _serializar_mazo(cartas):
    return [{"nombre": c.nombre, "tipo": c.tipo, "costo": c.costo,
             "ataque": c.ataque, "defensa": c.defensa,
             "descripcion": c.descripcion, "desc_floop": c.desc_floop}
            for c in cartas]

def _deserializar_mazo(data):
    return [Carta(c["nombre"], c["tipo"], c["costo"],
                  c.get("ataque",0), c.get("defensa",0),
                  c.get("descripcion",""), c.get("desc_floop",""))
            for c in data]
