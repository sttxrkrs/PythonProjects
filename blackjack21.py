import random

# Introducción tipo "recuadro"
intro = [
    "==============================================",
    "                 BLACKJACK 21",
    "    4 jugadores contra la CASA (crupier)",
    " Objetivo: acercarte a 21 y ganarle a la CASA",
    "    As (A) vale 1 u 11 según te convenga",
    "=============================================="
]
print("\n".join(intro))

# Baraja francesa simple
palos = ["Corazones", "Diamantes", "Tréboles", "Picas"]
valores = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
baraja = [(v, p) for p in palos for v in valores]
random.shuffle(baraja)

def valor_carta(v):
    if v in ["J", "Q", "K"]:
        return 10
    if v == "A":
        return 11
    return int(v)

def puntaje_mano(mano):
    total = sum(valor_carta(v) for v, _ in mano)
    ases = sum(1 for v, _ in mano if v == "A")
    while total > 21 and ases > 0:
        total -= 10
        ases -= 1
    return total

def mostrar_mano(nombre, mano, ocultar_primera=False):
    if ocultar_primera:
        visibles = ["[Oculta]", str(mano[1][0]) + " de " + str(mano[1][1])]
        print(nombre + ": " + ", ".join(visibles) + "  -> ? puntos")
    else:
        cartas = [str(v) + " de " + str(p) for v, p in mano]
        print(nombre + ": " + ", ".join(cartas) + "  -> " + str(puntaje_mano(mano)) + " puntos")

def robar():
    return baraja.pop() if baraja else None

# Configuración de jugadores
n_jugadores = 4
nombres = ["Jugador " + str(i+1) for i in range(n_jugadores)]
manos = {nombre: [] for nombre in nombres}
mano_casa = []

# Reparto inicial
for _ in range(2):
    for nombre in nombres:
        manos[nombre].append(robar())
    mano_casa.append(robar())

# Mostrar mesa inicial
for nombre in nombres:
    mostrar_mano(nombre, manos[nombre])
mostrar_mano("CASA", mano_casa, ocultar_primera=True)
print("----------------------------------------------")

# Turnos de jugadores
for nombre in nombres:
    while True:
        puntaje = puntaje_mano(manos[nombre])
        if puntaje >= 21:
            break
        r = input(nombre + ", ¿pides carta? si/no: ").strip().lower()
        if r == "si":
            carta = robar()
            if not carta:
                print("No quedan cartas en la baraja.")
                break
            manos[nombre].append(carta)
            mostrar_mano(nombre, manos[nombre])
        elif r == "no":
            break
        else:
            print("Opción no válida. Escribe si/no.")

print("----------------------------------------------")
# Juega la CASA (se planta en 17+)
print("Revelando cartas de la CASA...")
mostrar_mano("CASA", mano_casa)
while puntaje_mano(mano_casa) < 17:
    carta = robar()
    if not carta:
        print("No quedan cartas en la baraja para la CASA.")
        break
    mano_casa.append(carta)
    mostrar_mano("CASA", mano_casa)

punt_casa = puntaje_mano(mano_casa)
print("==============================================")
print("Puntaje final CASA: " + str(punt_casa))
print("==============================================")

# Resultados
for nombre in nombres:
    pj = puntaje_mano(manos[nombre])
    if pj > 21:
        estado = "Te pasaste de 21. Pierdes contra la CASA."
    elif punt_casa > 21:
        estado = "La CASA se pasó. ¡Ganas!"
    elif pj > punt_casa:
        estado = "¡Ganas a la CASA!"
    elif pj == punt_casa:
        estado = "Empate con la CASA."
    else:
        estado = "Pierdes contra la CASA."
    print(nombre + ": " + str(pj) + " vs CASA " + str(punt_casa) + " -> " + estado)

print("Gracias por jugar. ¡Que la suerte te acompañe!")
