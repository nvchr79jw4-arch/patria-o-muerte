# servidor_web.py
# ─────────────────────────────────────────────────────────────
#  PATRIA O MUERTE — Servidor web + multijugador
#  → py -3.12 servidor_web.py
# ─────────────────────────────────────────────────────────────

import os
import json
import random
import string
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__, static_folder='web/static', template_folder='web')
app.config['SECRET_KEY'] = 'patria-o-muerte-2024'
socketio = SocketIO(app, cors_allowed_origins="*")

PORT = int(os.environ.get("PORT", 5000))

# ── Salas de juego ─────────────────────────────────────────
salas = {}

def generar_codigo():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class Sala:
    def __init__(self, codigo):
        self.codigo    = codigo
        self.jugadores = []   # lista de session IDs
        self.nombres   = []
        self.mazos     = []
        self.turno     = 0
        self.estado    = "esperando"
        self.hp        = [25, 25]
        self.tableros  = [
            [{"criatura": None, "edificio": None} for _ in range(4)],
            [{"criatura": None, "edificio": None} for _ in range(4)],
        ]
        self.manos     = [[], []]
        self.mazos_cartas = [[], []]
        self.puntos_accion = [2, 2]

# ── Rutas web ──────────────────────────────────────────────

@app.route('/')
def index():
    return send_from_directory('web', 'index.html')

@app.route('/web/<path:filename>')
def static_files(filename):
    return send_from_directory('web', filename)

# ── Eventos Socket.IO ──────────────────────────────────────

@socketio.on('connect')
def on_connect():
    print(f"Cliente conectado: {socketio.server.environ.get('REMOTE_ADDR', 'unknown')}")

@socketio.on('disconnect')
def on_disconnect():
    from flask import request
    sid = request.sid
    for codigo, sala in list(salas.items()):
        if sid in sala.jugadores:
            idx = sala.jugadores.index(sid)
            nombre = sala.nombres[idx] if idx < len(sala.nombres) else "Jugador"
            ganador_idx = 1 - idx
            if sala.estado == "jugando" and ganador_idx < len(sala.nombres):
                socketio.emit('fin_partida', {
                    'ganador': sala.nombres[ganador_idx],
                    'perdedor': nombre,
                    'razon': 'desconexión'
                }, room=codigo)
            sala.jugadores.remove(sid)
            if not sala.jugadores:
                del salas[codigo]
            break

@socketio.on('crear_sala')
def on_crear_sala(data):
    from flask import request
    codigo = generar_codigo()
    while codigo in salas:
        codigo = generar_codigo()
    sala = Sala(codigo)
    sala.jugadores.append(request.sid)
    salas[codigo] = sala
    join_room(codigo)
    emit('sala_creada', {'codigo': codigo})

@socketio.on('unirse_sala')
def on_unirse_sala(data):
    from flask import request
    codigo = data.get('codigo', '').upper()
    if codigo not in salas:
        emit('error', {'msg': f"Sala '{codigo}' no encontrada"})
        return
    sala = salas[codigo]
    if len(sala.jugadores) >= 2:
        emit('error', {'msg': 'La sala está llena'})
        return
    sala.jugadores.append(request.sid)
    join_room(codigo)
    emit('sala_unida', {'codigo': codigo})

@socketio.on('jugador_listo')
def on_jugador_listo(data):
    from flask import request
    codigo = data.get('codigo')
    if codigo not in salas:
        return
    sala = salas[codigo]
    sid  = request.sid
    if sid not in sala.jugadores:
        return
    idx = sala.jugadores.index(sid)
    # Guardar nombre y mazo
    if idx >= len(sala.nombres):
        sala.nombres.append(data.get('nombre', f'Jugador {idx+1}'))
        sala.mazos.append(data.get('mazo', []))
        sala.mazos_cartas[idx] = data.get('mazo', [])[:]
        random.shuffle(sala.mazos_cartas[idx])
        sala.manos[idx] = sala.mazos_cartas[idx][:5]
        sala.mazos_cartas[idx] = sala.mazos_cartas[idx][5:]
    emit('unido', {'idx': idx, 'codigo': codigo})
    if len(sala.nombres) == 2:
        sala.estado = 'jugando'
        socketio.emit('inicio_partida', {
            'nombres': sala.nombres,
            'turno': 0,
            'mano_0': sala.manos[0],
            'mano_1': sala.manos[1],
            'hp': sala.hp,
        }, room=codigo)

@socketio.on('accion')
def on_accion(data):
    from flask import request
    codigo = data.get('codigo')
    if codigo not in salas:
        return
    sala = salas[codigo]
    sid  = request.sid
    if sid not in sala.jugadores:
        return
    idx = sala.jugadores.index(sid)
    if idx != sala.turno:
        emit('error', {'msg': 'No es tu turno'})
        return
    # Reenviar acción al rival
    socketio.emit('accion_rival', data, room=codigo, skip_sid=sid)

@socketio.on('sync_estado')
def on_sync_estado(data):
    from flask import request
    codigo = data.get('codigo')
    if codigo not in salas:
        return
    sala = salas[codigo]
    sid  = request.sid
    # Actualizar estado en el servidor
    idx = sala.jugadores.index(sid) if sid in sala.jugadores else -1
    if idx >= 0:
        if 'hp' in data:
            sala.hp = data['hp']
        if 'tablero' in data:
            sala.tableros[idx] = data['tablero']
    # Reenviar al rival
    socketio.emit('sync_estado', data, room=codigo, skip_sid=sid)

@socketio.on('fin_turno')
def on_fin_turno(data):
    from flask import request
    codigo = data.get('codigo')
    if codigo not in salas:
        return
    sala = salas[codigo]
    sid  = request.sid
    idx  = sala.jugadores.index(sid) if sid in sala.jugadores else -1
    if idx != sala.turno:
        return
    sala.turno = 1 - sala.turno
    # Robar carta para el nuevo jugador activo
    nuevo_idx = sala.turno
    carta_nueva = None
    if sala.mazos_cartas[nuevo_idx]:
        carta_nueva = sala.mazos_cartas[nuevo_idx].pop(0)
        sala.manos[nuevo_idx].append(carta_nueva)
    socketio.emit('cambio_turno', {
        'turno': sala.turno,
        'carta_nueva': carta_nueva,
        'para_jugador': nuevo_idx,
    }, room=codigo)

@socketio.on('chat')
def on_chat(data):
    from flask import request
    codigo = data.get('codigo')
    if codigo not in salas:
        return
    sala = salas[codigo]
    sid  = request.sid
    idx  = sala.jugadores.index(sid) if sid in sala.jugadores else 0
    nombre = sala.nombres[idx] if idx < len(sala.nombres) else 'Jugador'
    socketio.emit('chat', {
        'nombre': nombre,
        'mensaje': data.get('mensaje', '')[:100]
    }, room=codigo)

@socketio.on('rendirse')
def on_rendirse(data):
    from flask import request
    codigo = data.get('codigo')
    if codigo not in salas:
        return
    sala = salas[codigo]
    sid  = request.sid
    idx  = sala.jugadores.index(sid) if sid in sala.jugadores else 0
    ganador_idx = 1 - idx
    socketio.emit('fin_partida', {
        'ganador': sala.nombres[ganador_idx] if ganador_idx < len(sala.nombres) else 'Rival',
        'perdedor': sala.nombres[idx] if idx < len(sala.nombres) else 'Jugador',
        'razon': 'rendición'
    }, room=codigo)
    sala.estado = 'terminado'

# ── Main ───────────────────────────────────────────────────
if __name__ == '__main__':
    os.makedirs('web/static', exist_ok=True)
    print(f"🇺🇾 Servidor web Patria o Muerte en puerto {PORT}")
    socketio.run(app, host='0.0.0.0', port=PORT, debug=False)
