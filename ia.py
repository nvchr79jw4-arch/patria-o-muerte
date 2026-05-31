# ia.py
# ─────────────────────────────────────────────────────────────
#  PATRIA O MUERTE — El juego de cartas
#  La IA del oponente. Toma decisiones automáticas cada turno.
#  Estrategia: llena carriles vacíos, prioriza criaturas fuertes
# ─────────────────────────────────────────────────────────────

import random
from jugador import Jugador

class IA(Jugador):
    """Jugador controlado por la computadora."""

    def __init__(self, nombre, mazo):
        super().__init__(nombre, mazo)

    def jugar_turno(self, oponente):
        """
        La IA juega su turno completo automáticamente.
        Devuelve una lista de mensajes para mostrar al jugador.
        """
        mensajes = []
        mensajes.append(f"\n  🤖 {self.nombre} está pensando...")

        # ── 1. Jugar cartas mientras tenga PA ──────────────────
        intentos = 0
        while self.puntos_accion > 0 and self.mano and intentos < 20:
            intentos += 1

            # Filtrar cartas que puede jugar
            jugables = [c for c in self.mano if c.costo <= self.puntos_accion]
            if not jugables:
                break

            carta = self._elegir_carta(jugables)

            if carta.tipo == "criatura":
                carril = self._elegir_carril_para_colocar()
                if carril:
                    self.mano.remove(carta)
                    carril.colocar_criatura(carta)
                    self.puntos_accion -= carta.costo
                    mensajes.append(f"  🤖 {self.nombre} coloca '{carta.nombre}' en carril {carril.numero}")
                else:
                    break  # No hay carriles libres para criaturas

            elif carta.tipo == "edificio":
                carril = self._elegir_carril_para_edificio()
                if carril:
                    self.mano.remove(carta)
                    carril.colocar_edificio(carta)
                    self.puntos_accion -= carta.costo
                    mensajes.append(f"  🤖 {self.nombre} construye '{carta.nombre}' en carril {carril.numero}")
                else:
                    break

            elif carta.tipo == "hechizo":
                resultado = self._usar_hechizo(carta, oponente)
                if resultado:
                    self.mano.remove(carta)
                    self.descarte.append(carta)
                    self.puntos_accion -= carta.costo
                    mensajes.append(f"  🤖 {self.nombre} usa hechizo '{carta.nombre}': {resultado}")
                else:
                    break

        # ── 2. FLOOPear criaturas que puedan ──────────────────
        for carril in self.tablero.carriles:
            if carril.criatura and carril.criatura.puede_floop():
                msg = self._usar_floop(carril, oponente)
                if msg:
                    mensajes.append(f"  🤖 FLOOP! '{carril.criatura.nombre}': {msg}")

        return mensajes

    # ── Métodos internos de decisión ──────────────────────────

    def _elegir_carta(self, jugables):
        """Prioriza criaturas de alto ataque, luego hechizos, luego edificios."""
        criaturas = [c for c in jugables if c.tipo == "criatura"]
        hechizos  = [c for c in jugables if c.tipo == "hechizo"]
        edificios = [c for c in jugables if c.tipo == "edificio"]

        if criaturas:
            return max(criaturas, key=lambda c: c.ataque)
        if hechizos:
            return random.choice(hechizos)
        if edificios:
            return random.choice(edificios)
        return random.choice(jugables)

    def _elegir_carril_para_colocar(self):
        """Elige un carril vacío (sin criatura) para poner una criatura."""
        vacios = [c for c in self.tablero.carriles if not c.tiene_criatura()]
        return random.choice(vacios) if vacios else None

    def _elegir_carril_para_edificio(self):
        """Elige un carril sin edificio."""
        sin_edificio = [c for c in self.tablero.carriles if not c.tiene_edificio()]
        return random.choice(sin_edificio) if sin_edificio else None

    def _usar_hechizo(self, carta, oponente):
        """Aplica el efecto del hechizo. Devuelve descripción o None si no se pudo usar."""
        nombre = carta.nombre

        if nombre in ("El Mate", "El Asado"):
            self.robar(2)
            return "roba 2 cartas"

        elif nombre == "Lanza Gaucha":
            # Daña la criatura con más DEF del oponente
            objetivo = self._criatura_mas_fuerte(oponente)
            if objetivo:
                objetivo.recibir_daño(4)
                return f"inflige 4 daño a '{objetivo.nombre}'"
            else:
                oponente.recibir_daño(4)
                return "inflige 4 daño directo"

        elif nombre == "Gol de Vestuario":
            oponente.recibir_daño(5)
            return "inflige 5 daño directo"

        elif nombre == "Grito de Asencio":
            for carril in oponente.tablero.carriles:
                if carril.criatura:
                    carril.criatura.recibir_daño(2)
                    if carril.criatura.defensa <= 0:
                        carril.remover_criatura()
            return "2 daño a todas las criaturas enemigas"

        elif nombre == "La Murga":
            objetivo = self._edificio_enemigo(oponente)
            if objetivo:
                objetivo.remover_edificio()
                return "destruye un edificio enemigo"
            return None  # no hay edificios que destruir

        elif nombre == "Campo de Pesadillas":
            objetivo = self._carril_con_criatura(oponente)
            if objetivo and objetivo.criatura:
                objetivo.criatura.ataque = max(0, objetivo.criatura.ataque - 2)
                return f"'-2 ATK' a '{objetivo.criatura.nombre}'"
            return None

        return None  # hechizo no reconocido, no gastar PA

    def _usar_floop(self, carril, oponente):
        """Usa el FLOOP de la criatura en el carril dado."""
        criatura = carril.criatura
        nombre   = criatura.nombre

        if nombre == "El Gaucho":
            criatura.ataque += 2
            criatura.floopada = True
            return f"+2 ATK este turno (ahora {criatura.ataque})"

        elif nombre == "Artigas":
            for c in self.tablero.carriles:
                if c.criatura:
                    c.criatura.ataque += 1
            criatura.floopada = True
            return "todas las criaturas aliadas +1 ATK"

        elif nombre == "La Curandera":
            # Cura la criatura aliada con menos DEF
            objetivo = self._criatura_mas_dañada()
            if objetivo:
                objetivo.curar(3)
                criatura.floopada = True
                return f"cura 3 DEF a '{objetivo.nombre}'"

        elif nombre == "El Crack":
            # La IA no esquiva (no tiene sentido en ataque)
            criatura.floopada = True
            return "esquiva activada"

        elif nombre == "El Murguero":
            self.robar(1)
            oponente.recibir_daño(1)
            criatura.floopada = True
            return "roba 1 carta y 1 daño directo"

        elif nombre == "El Tamborilero":
            for c in self.tablero.carriles:
                if c.criatura:
                    c.criatura.ataque += 1
            criatura.floopada = True
            return "todas las criaturas aliadas +1 ATK"

        elif nombre == "El Chivito":
            for c in self.tablero.carriles:
                if c.criatura:
                    c.criatura.curar(2)
            criatura.floopada = True
            return "cura 2 DEF a todas las criaturas aliadas"

        elif nombre == "La Vedette":
            objetivo = self._carril_con_criatura(oponente)
            if objetivo and objetivo.criatura:
                objetivo.criatura.ataque = max(0, objetivo.criatura.ataque - 2)
                criatura.floopada = True
                return f"'-2 ATK' permanente a '{objetivo.criatura.nombre}'"

        elif nombre == "La Payadora":
            objetivo = self._carril_con_criatura(oponente)
            if objetivo and objetivo.criatura:
                oponente.paralizado[objetivo.numero] = True
                criatura.floopada = True
                return f"'{objetivo.criatura.nombre}' paralizada"

        elif nombre == "Arquero Dan":
            oponente.recibir_daño(2)
            criatura.floopada = True
            return "2 daño directo al rival"

        elif nombre == "Legión Terricola":
            for c in oponente.tablero.carriles:
                if c.criatura:
                    murio = c.criatura.recibir_daño(criatura.ataque)
                    if murio:
                        c.remover_criatura()
            criatura.floopada = True
            return f"ataca TODAS las criaturas enemigas"

        elif nombre == "Guardián del Silo":
            criatura.floopada = True
            return "ve la mano del rival (sin efecto en IA)"

        return None

    # ── Helpers ───────────────────────────────────────────────

    def _criatura_mas_fuerte(self, jugador):
        """Criatura con más DEF del jugador dado."""
        criaturas = [c.criatura for c in jugador.tablero.carriles if c.criatura]
        return max(criaturas, key=lambda c: c.defensa) if criaturas else None

    def _criatura_mas_dañada(self):
        """Criatura propia con menos DEF relativa."""
        criaturas = [c.criatura for c in self.tablero.carriles if c.criatura]
        return min(criaturas, key=lambda c: c.defensa / c.defensa_max) if criaturas else None

    def _carril_con_criatura(self, jugador):
        """Carril aleatorio del jugador que tenga criatura."""
        con_criatura = [c for c in jugador.tablero.carriles if c.criatura]
        return random.choice(con_criatura) if con_criatura else None

    def _edificio_enemigo(self, jugador):
        """Carril aleatorio del jugador que tenga edificio."""
        con_edificio = [c for c in jugador.tablero.carriles if c.edificio]
        return random.choice(con_edificio) if con_edificio else None
