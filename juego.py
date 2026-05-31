# juego.py
# ─────────────────────────────────────────────────────────────
#  PATRIA O MUERTE — El juego de cartas
#  Motor del juego: maneja los turnos, el combate y los efectos
# ─────────────────────────────────────────────────────────────

from carta import Carta
from cartas_data import get_mazo_oriental, get_mazo_uruguayo

def limpiar():
    print("\n" * 2)

def separador():
    print("\n" + "═" * 50)

def pausar():
    input("\n  Presioná ENTER para continuar...")

# ── Mostrar estado completo ────────────────────────────────

def mostrar_estado(jugador, ia):
    separador()
    print(f"\n  🇺🇾  PATRIA O MUERTE — El juego de cartas\n")
    print(f"  ❤️  {jugador.nombre}: {jugador.hp} HP   |   ❤️  {ia.nombre}: {ia.hp} HP")
    ia.tablero.mostrar(ia.nombre)
    jugador.tablero.mostrar(jugador.nombre)
    jugador.mostrar_mano()

# ── Fase: jugar cartas ─────────────────────────────────────

def fase_jugar_cartas(jugador, oponente):
    """El jugador humano juega cartas de su mano."""
    while jugador.puntos_accion > 0:
        print(f"\n  ⚡ Puntos de Acción: {jugador.puntos_accion}")
        print("  ¿Qué querés hacer?")
        print("  [1] Jugar una carta")
        print("  [2] Ver info de una carta")
        print("  [3] Pasar a la fase de FLOOP")

        opcion = input("\n  Tu opción: ").strip()

        if opcion == "1":
            _jugar_carta(jugador, oponente)
        elif opcion == "2":
            _ver_info_carta(jugador)
        elif opcion == "3":
            break
        else:
            print("  Opción inválida.")

def _jugar_carta(jugador, oponente):
    jugables = [c for c in jugador.mano if c.costo <= jugador.puntos_accion]
    if not jugables:
        print("  No tenés cartas que puedas jugar con los PA que te quedan.")
        return

    print("\n  Cartas que podés jugar:")
    for i, carta in enumerate(jugador.mano):
        marca = "  " if carta.costo > jugador.puntos_accion else "▶ "
        print(f"  {marca}{i + 1}. {carta}")

    try:
        idx = int(input("\n  ¿Cuál jugás? (número, 0 para cancelar): ")) - 1
    except ValueError:
        return

    if idx == -1:
        return
    if idx < 0 or idx >= len(jugador.mano):
        print("  Número inválido.")
        return

    carta = jugador.mano[idx]

    if carta.costo > jugador.puntos_accion:
        print(f"  No tenés suficientes PA. Necesitás {carta.costo}, tenés {jugador.puntos_accion}.")
        return

    if carta.tipo == "criatura":
        _colocar_en_carril(jugador, carta, "criatura")
    elif carta.tipo == "edificio":
        _colocar_en_carril(jugador, carta, "edificio")
    elif carta.tipo == "hechizo":
        resultado = _aplicar_hechizo(jugador, oponente, carta)
        if resultado:
            jugador.mano.remove(carta)
            jugador.descarte.append(carta)
            jugador.puntos_accion -= carta.costo
            print(f"\n  ✨ Hechizo '{carta.nombre}': {resultado}")

def _colocar_en_carril(jugador, carta, tipo):
    print("\n  ¿En qué carril? (1-4):")
    jugador.tablero.mostrar(jugador.nombre)

    try:
        num = int(input("  Carril: "))
    except ValueError:
        return

    if num < 1 or num > 4:
        print("  Carril inválido.")
        return

    carril = jugador.tablero.get_carril(num)

    if tipo == "criatura":
        if carril.tiene_criatura():
            print("  Ya hay una criatura en ese carril.")
            return
        carril.colocar_criatura(carta)
    elif tipo == "edificio":
        if carril.tiene_edificio():
            print("  Ya hay un edificio en ese carril.")
            return
        carril.colocar_edificio(carta)

    jugador.mano.remove(carta)
    jugador.puntos_accion -= carta.costo
    print(f"\n  ✅ '{carta.nombre}' colocado en carril {num}.")

def _ver_info_carta(jugador):
    if not jugador.mano:
        print("  No tenés cartas en la mano.")
        return
    jugador.mostrar_mano()
    try:
        idx = int(input("\n  ¿Cuál querés ver? (número): ")) - 1
    except ValueError:
        return
    if 0 <= idx < len(jugador.mano):
        print(jugador.mano[idx].info_completa())

# ── Fase: FLOOP ────────────────────────────────────────────

def fase_floop(jugador, oponente):
    """El jugador activa habilidades FLOOP de sus criaturas."""
    floopables = [(i+1, c.criatura) for i, c in enumerate(jugador.tablero.carriles)
                  if c.criatura and c.criatura.puede_floop()]

    if not floopables:
        print("\n  No tenés criaturas con FLOOP disponible.")
        return

    print("\n  ✨ Criaturas que pueden FLOOP:")
    for num, criatura in floopables:
        print(f"  Carril {num}: {criatura.nombre} — FLOOP: {criatura.desc_floop}")

    try:
        num = int(input("\n  ¿Cuál floopás? (número de carril, 0 para saltear): "))
    except ValueError:
        return

    if num == 0:
        return

    if num < 1 or num > 4:
        print("  Carril inválido.")
        return

    carril = jugador.tablero.get_carril(num)
    if not carril.criatura or not carril.criatura.puede_floop():
        print("  Esa criatura no puede FLOOP ahora.")
        return

    resultado = _aplicar_floop(jugador, oponente, carril)
    if resultado:
        carril.criatura.floopada = True
        print(f"\n  ✨ FLOOP! '{carril.criatura.nombre}': {resultado}")

def _aplicar_floop(jugador, oponente, carril):
    criatura = carril.criatura
    nombre   = criatura.nombre

    if nombre == "El Gaucho":
        criatura.ataque += 2
        return f"+2 ATK este turno (ahora {criatura.ataque})"

    elif nombre == "Artigas":
        for c in jugador.tablero.carriles:
            if c.criatura:
                c.criatura.ataque += 1
        return "todas las criaturas aliadas ganan +1 ATK"

    elif nombre == "La Payadora":
        con_criatura = [c for c in oponente.tablero.carriles if c.criatura]
        if not con_criatura:
            return "no hay criaturas enemigas para paralizar"
        print("\n  ¿Qué carril enemigo paralizás?")
        oponente.tablero.mostrar(oponente.nombre)
        try:
            num = int(input("  Carril: "))
        except ValueError:
            return None
        c = oponente.tablero.get_carril(num)
        if c.criatura:
            oponente.paralizado[num] = True
            return f"'{c.criatura.nombre}' en carril {num} paralizada"
        return "ese carril no tiene criatura"

    elif nombre == "La Curandera":
        aliadas = [c.criatura for c in jugador.tablero.carriles if c.criatura]
        if not aliadas:
            return "no hay criaturas aliadas"
        objetivo = min(aliadas, key=lambda c: c.defensa)
        objetivo.curar(3)
        return f"cura 3 DEF a '{objetivo.nombre}' (ahora {objetivo.defensa} DEF)"

    elif nombre == "Caballero Azul":
        aliadas = [c.criatura for c in jugador.tablero.carriles if c.criatura]
        if not aliadas:
            return "no hay criaturas aliadas"
        objetivo = min(aliadas, key=lambda c: c.defensa)
        objetivo.curar(2)
        return f"cura 2 DEF a '{objetivo.nombre}'"

    elif nombre == "El Crack":
        carril._esquivando = True
        return "esquiva activada: no puede ser atacado este turno"

    elif nombre == "El Murguero":
        jugador.robar(1)
        oponente.recibir_daño(1)
        return f"robaste 1 carta y {oponente.nombre} recibe 1 daño directo"

    elif nombre == "El Tamborilero":
        for c in jugador.tablero.carriles:
            if c.criatura:
                c.criatura.ataque += 1
        return "todas las criaturas aliadas +1 ATK"

    elif nombre == "El Chivito":
        for c in jugador.tablero.carriles:
            if c.criatura:
                c.criatura.curar(2)
        return "cura 2 DEF a todas las criaturas aliadas"

    elif nombre == "La Vedette":
        con_criatura = [c for c in oponente.tablero.carriles if c.criatura]
        if not con_criatura:
            return "no hay criaturas enemigas"
        print("\n  ¿A qué carril enemigo le restás ATK?")
        oponente.tablero.mostrar(oponente.nombre)
        try:
            num = int(input("  Carril: "))
        except ValueError:
            return None
        c = oponente.tablero.get_carril(num)
        if c.criatura:
            c.criatura.ataque = max(0, c.criatura.ataque - 2)
            return f"'{c.criatura.nombre}' pierde 2 ATK permanentemente"
        return "ese carril no tiene criatura"

    elif nombre == "Arquero Dan":
        oponente.recibir_daño(2)
        return f"2 daño directo a {oponente.nombre}"

    elif nombre == "Legión Terricola":
        destruidas = []
        for c in oponente.tablero.carriles:
            if c.criatura:
                murio = c.criatura.recibir_daño(criatura.ataque)
                if murio:
                    destruidas.append(c.criatura.nombre)
                    c.remover_criatura()
        msg = f"ataca todas las criaturas enemigas con {criatura.ataque} daño"
        if destruidas:
            msg += f" | destruidas: {', '.join(destruidas)}"
        return msg

    elif nombre == "Guardián del Silo":
        print(f"\n  👁️  Mano de {oponente.nombre}:")
        for carta in oponente.mano:
            print(f"     - {carta}")
        return "revelaste la mano enemiga"

    elif nombre == "Caminante de Maíz":
        criatura.curar(2)
        return f"regenera 2 DEF (ahora {criatura.defensa})"

    return "habilidad no implementada"

# ── Hechizos del jugador humano ────────────────────────────

def _aplicar_hechizo(jugador, oponente, carta):
    nombre = carta.nombre

    if nombre in ("El Mate", "El Asado"):
        jugador.robar(2)
        return "robaste 2 cartas"

    elif nombre == "Lanza Gaucha":
        con_criatura = [c for c in oponente.tablero.carriles if c.criatura]
        if con_criatura:
            print("\n  ¿A qué carril enemigo apuntás?")
            oponente.tablero.mostrar(oponente.nombre)
            try:
                num = int(input("  Carril: "))
            except ValueError:
                return None
            c = oponente.tablero.get_carril(num)
            if c.criatura:
                murio = c.criatura.recibir_daño(4)
                nombre_obj = c.criatura.nombre
                if murio:
                    c.remover_criatura()
                    return f"4 daño a '{nombre_obj}' — destruida!"
                return f"4 daño a '{nombre_obj}' (le quedan {c.criatura.defensa} DEF)"
        oponente.recibir_daño(4)
        return f"4 daño directo a {oponente.nombre}"

    elif nombre == "Gol de Vestuario":
        oponente.recibir_daño(5)
        return f"¡5 daño directo a {oponente.nombre}!"

    elif nombre == "Grito de Asencio":
        destruidas = []
        for c in oponente.tablero.carriles:
            if c.criatura:
                murio = c.criatura.recibir_daño(2)
                if murio:
                    destruidas.append(c.criatura.nombre)
                    c.remover_criatura()
        msg = "2 daño a todas las criaturas enemigas"
        if destruidas:
            msg += f" | destruidas: {', '.join(destruidas)}"
        return msg

    elif nombre == "La Murga":
        con_edificio = [c for c in oponente.tablero.carriles if c.edificio]
        if not con_edificio:
            print("  El rival no tiene edificios.")
            return None
        print("\n  ¿Qué edificio enemigo destruís?")
        oponente.tablero.mostrar(oponente.nombre)
        try:
            num = int(input("  Carril: "))
        except ValueError:
            return None
        c = oponente.tablero.get_carril(num)
        if c.edificio:
            nombre_edif = c.edificio.nombre
            c.remover_edificio()
            return f"destruiste '{nombre_edif}'"
        return "ese carril no tiene edificio"

    elif nombre == "Campo de Pesadillas":
        con_criatura = [c for c in oponente.tablero.carriles if c.criatura]
        if not con_criatura:
            print("  El rival no tiene criaturas.")
            return None
        print("\n  ¿A qué criatura enemiga le restás ATK?")
        oponente.tablero.mostrar(oponente.nombre)
        try:
            num = int(input("  Carril: "))
        except ValueError:
            return None
        c = oponente.tablero.get_carril(num)
        if c.criatura:
            c.criatura.ataque = max(0, c.criatura.ataque - 2)
            return f"'{c.criatura.nombre}' pierde 2 ATK (ahora {c.criatura.ataque})"
        return "ese carril no tiene criatura"

    elif nombre == "Reclamar Terreno":
        criaturas_descarte = [c for c in jugador.descarte if c.tipo == "criatura"]
        if not criaturas_descarte:
            print("  No tenés criaturas en el descarte.")
            return None
        print("\n  ¿Cuál recuperás del descarte?")
        for i, c in enumerate(criaturas_descarte):
            print(f"  {i+1}. {c}")
        try:
            idx = int(input("  Número: ")) - 1
        except ValueError:
            return None
        if 0 <= idx < len(criaturas_descarte):
            recuperada = criaturas_descarte[idx]
            jugador.descarte.remove(recuperada)
            recuperada.defensa = recuperada.defensa_max
            recuperada.floopada = False
            jugador.mano.append(recuperada)
            return f"'{recuperada.nombre}' vuelve a tu mano"
        return "número inválido"

    return None

# ── Fase de batalla ────────────────────────────────────────

def fase_batalla(atacante, defensor):
    """Las criaturas del atacante pelean contra las del defensor."""
    separador()
    print(f"\n  ⚔️  FASE DE BATALLA — {atacante.nombre} ataca\n")

    for i, carril_atk in enumerate(atacante.tablero.carriles):
        if not carril_atk.criatura:
            continue

        criatura_atk = carril_atk.criatura
        num_carril   = i + 1
        carril_def   = defensor.tablero.get_carril(num_carril)

        # Verificar esquiva
        esquivando = getattr(carril_def, '_esquivando', False)
        if esquivando:
            print(f"  Carril {num_carril}: '{criatura_atk.nombre}' ataca pero "
                  f"'{carril_def.criatura.nombre}' esquiva!")
            carril_def._esquivando = False
            continue

        # Verificar parálisis
        if num_carril in atacante.paralizado:
            print(f"  Carril {num_carril}: '{criatura_atk.nombre}' está paralizada y no puede atacar.")
            continue

        if carril_def.criatura:
            # Combate entre criaturas
            criatura_def = carril_def.criatura
            print(f"  Carril {num_carril}: '{criatura_atk.nombre}' ({criatura_atk.ataque} ATK) "
                  f"vs '{criatura_def.nombre}' ({criatura_def.defensa} DEF)")

            muere_def = criatura_def.recibir_daño(criatura_atk.ataque)
            muere_atk = criatura_atk.recibir_daño(criatura_def.ataque)

            if muere_def:
                print(f"    💀 '{criatura_def.nombre}' destruida!")
                carril_def.remover_criatura()
            else:
                print(f"    '{criatura_def.nombre}' sobrevive con {criatura_def.defensa} DEF")

            if muere_atk:
                print(f"    💀 '{criatura_atk.nombre}' también destruida!")
                carril_atk.remover_criatura()
            else:
                print(f"    '{criatura_atk.nombre}' sobrevive con {criatura_atk.defensa} DEF")

        else:
            # Daño directo al jugador
            daño = criatura_atk.ataque
            # Bonus de edificio aliado
            if carril_atk.edificio and carril_atk.edificio.nombre == "La Estancia":
                daño += 1
            if carril_atk.edificio and carril_atk.edificio.nombre == "El Estadio":
                daño += 2
            defensor.recibir_daño(daño)
            print(f"  Carril {num_carril}: '{criatura_atk.nombre}' ataca directo "
                  f"→ {defensor.nombre} pierde {daño} HP (le quedan {defensor.hp})")

    # Efecto de La Rambla
    for carril_def in defensor.tablero.carriles:
        if carril_def.edificio and carril_def.edificio.nombre == "La Rambla":
            atacante.recibir_daño(1)
            print(f"  🏖️  La Rambla devuelve 1 daño a {atacante.nombre}")

    pausar()

# ── Turno del jugador humano ───────────────────────────────

def turno_jugador(jugador, ia):
    jugador.iniciar_turno()
    mostrar_estado(jugador, ia)

    print(f"\n  ── Tu turno, {jugador.nombre} ──")

    # Fase jugar cartas
    fase_jugar_cartas(jugador, ia)

    # Fase FLOOP
    print("\n  ── Fase FLOOP ──")
    fase_floop(jugador, ia)

    # Fase batalla
    fase_batalla(jugador, ia)

# ── Turno de la IA ─────────────────────────────────────────

def turno_ia(ia, jugador):
    ia.iniciar_turno()
    separador()
    print(f"\n  🤖 Turno de {ia.nombre}...\n")

    mensajes = ia.jugar_turno(jugador)
    for msg in mensajes:
        print(msg)

    pausar()
    fase_batalla(ia, jugador)

# ── Bucle principal ────────────────────────────────────────

def jugar(jugador, ia):
    """Bucle principal del juego."""
    turno = 1

    while jugador.esta_vivo() and ia.esta_vivo():
        print(f"\n\n  {'─'*20} TURNO {turno} {'─'*20}")

        # Turno del jugador
        turno_jugador(jugador, ia)
        if not ia.esta_vivo():
            break

        # Turno de la IA
        turno_ia(ia, jugador)
        if not jugador.esta_vivo():
            break

        turno += 1

    # Fin del juego
    separador()
    if jugador.esta_vivo():
        print(f"\n  🏆 ¡{jugador.nombre} ganó! ¡Sos el Cool Guy!")
        print(f"  😔 {ia.nombre} es el DWEEB.")
    else:
        print(f"\n  😔 {jugador.nombre} perdió... Sos el DWEEB.")
        print(f"  🏆 {ia.nombre} ganó. ¡La IA es el Cool Guy!")
    separador()
