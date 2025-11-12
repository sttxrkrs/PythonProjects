import random

# Introducción
intro = [
    "==============================================",
    "                    PÓKER",
    "    4 jugadores contra la CASA (crupier)",
    "   Objetivo: tener mejor mano que la CASA",
    "   Manos: Trio, Doble Par, Par, Carta Alta",
    "=============================================="
]
print("\n".join(intro))

# Baraja
palos = ["Corazones", "Diamantes", "Treboles", "Picas"]
valores = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
baraja = [(v, p) for p in palos for v in valores]
random.shuffle(baraja)

def val_num(v):
    if v == "A": return 14
    if v == "K": return 13
    if v == "Q": return 12
    if v == "J": return 11
    return int(v)

def evaluar_mano(mano):
    from collections import Counter
    nums = sorted([val_num(v) for v, _ in mano], reverse=True)
    count = Counter(nums)
    if 3 in count.values():
        return (4, max(k for k, v in count.items() if v == 3))
    pairs = sorted([k for k, v in count.items() if v == 2], reverse=True)
    if len(pairs) == 2:
        return (3, pairs[0], pairs[1])
    if len(pairs) == 1:
        return (2, pairs[0])
    return (1, nums[0])

def mostrar_mano(nombre, mano, ocultar=False):
    if ocultar:
        print(nombre + ": [Ocultas] -> ?")
    else:
        cartas = [str(v) + " de " + str(p) for v, p in mano]
        print(nombre + ": " + ", ".join(cartas))

def robar():
    return baraja.pop() if baraja else None

# Jugadores
n_jugadores = 4
nombres = ["Jugador " + str(i+1) for i in range(n_jugadores)]
manos = {nombre: [] for nombre in nombres}
mano_casa = []

# Reparto inicial
for _ in range(5):
    for nombre in nombres:
        manos[nombre].append(robar())
    mano_casa.append(robar())

# Mostrar mesa inicial
for nombre in nombres:
    mostrar_mano(nombre, manos[nombre])
mostrar_mano("CASA", mano_casa, ocultar=True)
print("----------------------------------------------")

# Turnos de jugadores (cambiar cartas)
for nombre in nombres:
    mano = manos[nombre]
    cambios = 0
    while cambios < 3:
        mostrar_mano(nombre, mano)
        r = input(nombre + ", ¿cambias una carta? si/no: ").strip().lower()
        if r == "si":
            try:
                idx = int(input("Indice de carta a cambiar (1-5): ")) - 1
                if 0 <= idx < 5:
                    nueva = robar()
                    if nueva:
                        mano[idx] = nueva
                        cambios += 1
                    else:
                        print("No quedan cartas.")
                        break
                else:
                    print("Indice invalido.")
            except ValueError:
                print("Ingresa un numero.")
        elif r == "no":
            break
        else:
            print("Opcion no valida. Escribe si/no.")

print("----------------------------------------------")
# Juega la CASA (no cambia cartas)
print("Revelando cartas de la CASA...")
mostrar_mano("CASA", mano_casa)

eval_casa = evaluar_mano(mano_casa)
print("==============================================")
print("Mano final CASA evaluada.")
print("==============================================")

# Resultados
for nombre in nombres:
    eval_j = evaluar_mano(manos[nombre])
    if eval_j > eval_casa:
        estado = "Ganas a la CASA!"
    elif eval_j == eval_casa:
        estado = "Empate con la CASA."
    else:
        estado = "Pierdes contra la CASA."
    print(nombre + " -> " + estado)

print("Gracias por jugar. ¡Que la suerte te acompañe!")
