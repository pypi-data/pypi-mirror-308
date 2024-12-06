# bingo.py
import random
import numpy as np

# Función para generar cartones
def generar_carton(personas):
    cartones = {}
    for persona in range(1, personas + 1):
        nombre_carton = []
        while len(nombre_carton) < 15:
            numero = random.randint(1, 90)
            if numero not in nombre_carton:
                nombre_carton.append(numero)
                nombre_carton.sort()
        matriz_3x5 = np.array(nombre_carton).reshape(3, 5)
        cartones[f"{persona}"] = matriz_3x5
    return cartones

# Función para mostrar todos los cartones
def mostrar_todos_los_cartones(cartones):
    print("Estos son todos los cartones disponibles:")
    for persona, carton in cartones.items():
        print(f"Cartón {persona}:")
        for fila in carton:
            print(fila)
        print()

# Función para mostrar el cartón con colores
def mostrar_carton(colores, carton):
    for fila in carton:
        fila_marcada = [
            f"\033[32m{num}\033[0m" if colores[num] else f"\033[31m{num}\033[0m"
            for num in fila
        ]
        print(' '.join(fila_marcada))
    print()  # Línea en blanco para separar

# Función para seleccionar y mostrar el cartón del jugador
def mi_carton(cartones):  
    mostrar_todos_los_cartones(cartones)
    seleccion = input("Elige el número del cartón con el que deseas jugar: ")
    if seleccion in cartones:
        print(f"\nHas elegido el cartón {seleccion}. Tu cartón es:")
        for fila in cartones[seleccion]:
            print(fila)
        return cartones[seleccion]
    else:
        print("Cartón no válido.")
        return None

# Función para generar el bombo
def generar_bombo():
    bombo = []
    while len(bombo) < 90:
        numero = random.randint(1, 90)
        if numero not in bombo:
            bombo.append(numero)
    return bombo

# Función principal del juego
def jugar_bingo():
    while True:
        try:
            num_personas = int(input("¿Contra cuántas personas deseas jugar al bingo? "))
            if num_personas >= 1:
                break
            else:
                print("Por favor, ingresa un número mayor o igual a 1.")
        except ValueError:
            print("Por favor, ingresa un número válido.")

    cartones = generar_carton(num_personas)
    carton = mi_carton(cartones)  
    if carton is None:
        return
    
    bombo = generar_bombo()
    print("Bombo listo, ¡comienza el juego!\n")
    marcado = {n: False for n in carton.flatten()}
    linea = False
    bingo = False
    tiradas = 0
    linea_impresa = False
    colores = {n: False for n in carton.flatten()}  # False para rojo, True para verde
    
    while not bingo:
        input(f"\nPresiona Enter para sacar un número del bombo... ({tiradas + 1} tiradas)")
        numero = bombo[tiradas]
        if numero in marcado:
            marcado[numero] = True
            colores[numero] = True  # Actualiza a verde si está marcado
            print(f"Ha salido el número {numero} -> ¡¡SÍ está en tu cartón!!")
        else:
            print(f"Ha salido el número {numero} -> NO está en tu cartón.")
        
        mostrar_carton(colores, carton)  # Muestra el cartón actualizado con colores
        
        for i in range(3):
            if all(marcado[carton[i, j]] for j in range(5)):
                if not linea_impresa:
                    linea_impresa = True
                    print("¡Tienes una línea! Pero el juego sigue.")
                break
        
        if all(marcado[num] for num in carton.flatten()):
            bingo = True
            print("¡Bingo! ¡Has ganado!")
            break
        
        for persona, carton_otro in cartones.items():
            marcado_persona = {n: False for n in carton_otro.flatten()}
            for i in range(tiradas + 1):
                numero = bombo[i]
                if numero in marcado_persona:
                    marcado_persona[numero] = True

            for i in range(3):
                if all(marcado_persona[carton_otro[i, j]] for j in range(5)):
                    if not linea_impresa:
                        print("--------------------------------------------------")
                        print(f"¡La persona {persona} tiene una línea! Pero el juego sigue.".upper())
                        print("--------------------------------------------------")
                        linea_impresa = True
                    break
            if all(marcado_persona[num] for num in carton_otro.flatten()):
                print("--------------------------------------------------")
                print(f"¡La persona {persona} tiene bingo! El juego termina.".upper())
                return

        tiradas += 1

if __name__ == "__main__":
    jugar_bingo()