# main.py
# ─────────────────────────────────────────────────────────────
#  PATRIA O MUERTE — El juego de cartas
#  Punto de entrada: ejecutá este archivo para jugar
#  → python main.py
# ─────────────────────────────────────────────────────────────

from jugador import Jugador
from ia import IA
from cartas_data import get_mazo_oriental, get_mazo_uruguayo
from juego import jugar

def pantalla_titulo():
    print("""
╔══════════════════════════════════════════════════════╗
║                                                      ║
║          🇺🇾  PATRIA O MUERTE  🇺🇾                    ║
║              El juego de cartas                      ║
║                                                      ║
║   "Los orientales somos o dominamos o morimos"       ║
║                          — José Artigas              ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
    """)

def elegir_mazo():
    print("  ¿Con qué mazo querés jugar?\n")
    print("  [1] Mazo Oriental  — Gauchos, caudillos y el campo")
    print("  [2] Mazo Uruguayo  — Fútbol, candombe y la ciudad")

    while True:
        opcion = input("\n  Tu elección (1 o 2): ").strip()
        if opcion == "1":
            return "Oriental", get_mazo_oriental()
        elif opcion == "2":
            return "Uruguayo", get_mazo_uruguayo()
        else:
            print("  Escribí 1 o 2.")

def elegir_nombre():
    nombre = input("\n  ¿Cómo te llamás? ").strip()
    return nombre if nombre else "Jugador"

def main():
    pantalla_titulo()

    nombre = elegir_nombre()
    nombre_mazo, mazo_jugador = elegir_mazo()

    # La IA usa el mazo contrario
    if nombre_mazo == "Oriental":
        mazo_ia = get_mazo_uruguayo()
        nombre_ia = "La Máquina Uruguaya"
    else:
        mazo_ia = get_mazo_oriental()
        nombre_ia = "El Gaucho Cibernético"

    print(f"\n  Muy bien, {nombre}. Jugás con el mazo {nombre_mazo}.")
    print(f"  Tu rival: {nombre_ia}")
    print(f"\n  Reglas rápidas:")
    print(f"  • Cada turno tenés 2 Puntos de Acción (PA)")
    print(f"  • Colocá criaturas en los 4 carriles")
    print(f"  • Si atacás un carril vacío, dañás al rival directamente")
    print(f"  • Llegá a 0 HP al rival para ganar")
    print(f"  • ✨ = la criatura tiene habilidad FLOOP disponible")

    input("\n  Presioná ENTER para empezar...")

    jugador = Jugador(nombre, mazo_jugador)
    ia      = IA(nombre_ia, mazo_ia)

    jugar(jugador, ia)

    # Preguntar si quiere jugar de nuevo
    print()
    otra = input("  ¿Otra partida? (s/n): ").strip().lower()
    if otra == "s":
        main()
    else:
        print("\n  ¡Hasta la próxima, orientale! 🇺🇾\n")

if __name__ == "__main__":
    main()
