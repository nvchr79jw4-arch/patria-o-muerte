# servidor.py
# ─────────────────────────────────────────────────────────────
#  PATRIA O MUERTE — Servidor de multijugador online
#  Corré esto en tu PC para jugar en WiFi local, o
#  subilo a Railway para jugar por internet
#
#  → py -3.12 servidor.py
# ─────────────────────────────────────────────────────────────

import asyncio
import websockets
import json
import random
import string
from datetime import datetime

# ── Configuración ──────────────────────────────────────────
HOST = "0.0.0.0"   # acepta conexiones de cualquier IP
PORT = int(__import__('os').environ.get("PORT", 8765))

# ── Estado del servidor ────────────────────────────────────
salas = {}   # {codigo_sala: Sala}

def log(msg):
    hora = datetime.now().strftime("%H:%M:%S")
    print(f"[{hora}] {msg}")

# ── Sala de juego ──────────────────────────────────────────

class Sala:
    def __init__(self, codigo):
        self.codigo    = codigo
        self.jugadores = []   # lista de websockets
        self.nombres   = []   # nombres de los jugadores
        self.mazos     = []   # mazos elegidos
        self.turno     = 0    # índice del jugador actual
        self.estado    = "esperando"  # esperando, jugando, terminado

    def llena(self):
        return len(self.jugadores) >= 2

    def jugador_idx(self, ws):
        return self.jugadores.index(ws) if ws in self.jugadores else -1

    async def enviar_a(self, ws, mensaje):
        try:
            await ws.send(json.dumps(mensaje))
        except:
            pass

    async def broadcast(self, mensaje, excepto=None):
        for ws in self.jugadores:
            if ws != excepto:
                await self.enviar_a(ws, mensaje)

    async def broadcast_todos(self, mensaje):
        for ws in self.jugadores:
            await self.enviar_a(ws, mensaje)


def generar_codigo():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


# ── Manejador de mensajes ──────────────────────────────────

async def manejar_mensaje(ws, sala, datos):
    tipo = datos.get("tipo")
    idx  = sala.jugador_idx(ws)

    # ── Unirse con nombre y mazo ───────────────────────────
    if tipo == "unirse":
        sala.nombres.append(datos.get("nombre", f"Jugador {idx+1}"))
        sala.mazos.append(datos.get("mazo", []))
        log(f"Sala {sala.codigo}: {sala.nombres[-1]} se unió")

        await sala.enviar_a(ws, {
            "tipo": "unido",
            "idx":  idx,
            "codigo": sala.codigo,
        })

        if sala.llena():
            sala.estado = "jugando"
            log(f"Sala {sala.codigo}: ¡partida iniciada! {sala.nombres[0]} vs {sala.nombres[1]}")
            await sala.broadcast_todos({
                "tipo":     "inicio",
                "nombres":  sala.nombres,
                "mazos":    sala.mazos,
                "turno":    0,
            })

    # ── Acción de juego (jugar carta, floop, terminar turno) ──
    elif tipo == "accion":
        if idx != sala.turno:
            await sala.enviar_a(ws, {"tipo": "error", "msg": "No es tu turno"})
            return
        # Reenviar la acción al rival
        await sala.broadcast(datos, excepto=ws)

    # ── Fin de turno ───────────────────────────────────────
    elif tipo == "fin_turno":
        if idx != sala.turno:
            return
        sala.turno = 1 - sala.turno
        await sala.broadcast_todos({
            "tipo":  "cambio_turno",
            "turno": sala.turno,
        })

    # ── Sincronizar estado completo ────────────────────────
    elif tipo == "sync_estado":
        # Un jugador manda su estado completo al rival
        await sala.broadcast(datos, excepto=ws)

    # ── Chat ───────────────────────────────────────────────
    elif tipo == "chat":
        await sala.broadcast_todos({
            "tipo":    "chat",
            "nombre":  sala.nombres[idx],
            "mensaje": datos.get("mensaje", "")[:100],
        })

    # ── Rendirse ───────────────────────────────────────────
    elif tipo == "rendirse":
        ganador_idx = 1 - idx
        await sala.broadcast_todos({
            "tipo":    "fin_partida",
            "ganador": sala.nombres[ganador_idx],
            "perdedor":sala.nombres[idx],
            "razon":   "rendición",
        })
        sala.estado = "terminado"


# ── Conexión principal ─────────────────────────────────────

async def conexion(ws):
    sala_actual = None
    try:
        log(f"Nueva conexión: {ws.remote_address}")

        async for mensaje_raw in ws:
            try:
                datos = json.loads(mensaje_raw)
            except:
                continue

            tipo = datos.get("tipo")

            # ── Crear sala ─────────────────────────────────
            if tipo == "crear_sala":
                codigo = generar_codigo()
                while codigo in salas:
                    codigo = generar_codigo()
                sala = Sala(codigo)
                sala.jugadores.append(ws)
                salas[codigo] = sala
                sala_actual   = sala
                log(f"Sala creada: {codigo}")
                await ws.send(json.dumps({
                    "tipo":   "sala_creada",
                    "codigo": codigo,
                }))

            # ── Unirse a sala ──────────────────────────────
            elif tipo == "unirse_sala":
                codigo = datos.get("codigo", "").upper()
                if codigo not in salas:
                    await ws.send(json.dumps({
                        "tipo": "error",
                        "msg":  f"Sala '{codigo}' no encontrada"
                    }))
                elif salas[codigo].llena():
                    await ws.send(json.dumps({
                        "tipo": "error",
                        "msg":  "La sala está llena"
                    }))
                else:
                    sala = salas[codigo]
                    sala.jugadores.append(ws)
                    sala_actual = sala
                    log(f"Jugador se unió a sala {codigo}")
                    await ws.send(json.dumps({
                        "tipo":   "sala_unida",
                        "codigo": codigo,
                    }))

            # ── Mensajes dentro de una sala ────────────────
            elif sala_actual:
                await manejar_mensaje(ws, sala_actual, datos)

    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        # Limpiar al desconectarse
        if sala_actual and ws in sala_actual.jugadores:
            idx = sala_actual.jugador_idx(ws)
            nombre = sala_actual.nombres[idx] if idx < len(sala_actual.nombres) else "Jugador"
            log(f"Sala {sala_actual.codigo}: {nombre} se desconectó")
            if sala_actual.estado == "jugando":
                ganador_idx = 1 - idx
                if ganador_idx < len(sala_actual.nombres):
                    await sala_actual.broadcast({
                        "tipo":    "fin_partida",
                        "ganador": sala_actual.nombres[ganador_idx],
                        "perdedor": nombre,
                        "razon":   "desconexión",
                    }, excepto=ws)
            sala_actual.jugadores.remove(ws)
            if not sala_actual.jugadores:
                del salas[sala_actual.codigo]
                log(f"Sala {sala_actual.codigo} eliminada")


# ── Main ───────────────────────────────────────────────────

async def main():
    log(f"🇺🇾 Servidor Patria o Muerte iniciado en {HOST}:{PORT}")
    log("Esperando jugadores...")
    async with websockets.serve(conexion, HOST, PORT):
        await asyncio.Future()  # correr para siempre

if __name__ == "__main__":
    asyncio.run(main())
