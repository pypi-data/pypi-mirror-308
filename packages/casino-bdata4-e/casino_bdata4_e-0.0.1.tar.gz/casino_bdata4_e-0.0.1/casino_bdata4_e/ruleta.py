import random

# Definición de colores para cada número en la ruleta.
COLORES = {n: 'rojo' if n in {
    1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36} else 'negro' for n in range(1, 37)}

DOCENAS = {
    1: range(1, 13),
    2: range(13, 25),
    3: range(25, 37)
}

COLUMNAS = {
    1: {1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34},
    2: {2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35},
    3: {3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36}
}

def girar_ruleta():
    return random.randint(0, 36)

def obtener_color(numero):
    return COLORES.get(numero, 'verde')  # El 0 es verde

def es_par(numero):
    return numero != 0 and numero % 2 == 0

def es_impar(numero):
    return numero != 0 and numero % 2 == 1

def en_docena(numero):
    for docena, numeros in DOCENAS.items():
        if numero in numeros:
            return docena
    return None

def en_columna(numero):
    for columna, numeros in COLUMNAS.items():
        if numero in numeros:
            return columna
    return None

def es_mitad(numero):
    if numero == 0:
        return "ninguna"
    return "alta" if numero > 18 else "baja"

def jugar_ruleta():
    print("Bienvenido a la ruleta. ¿A qué quieres apostar?")
    print("1. Número específico (0-36)")
    print("2. Color (rojo/negro)")
    print("3. Docena (1, 2 o 3)")
    print("4. Mitad (alta/baja)")
    print("5. Par o Impar")

    try:
        opcion = int(input("Selecciona una opción (1-5): "))
    except ValueError:
        print("Opción inválida. Por favor, ingresa un número entre 1 y 5.")
        return

    numero_girado = girar_ruleta()
    color_girado = obtener_color(numero_girado)
    mitad_girada = es_mitad(numero_girado)
    paridad_girada = "par" if es_par(numero_girado) else "impar"

    if opcion == 1:
        try:
            apuesta = int(input("Apuesta un número entre 0 y 36: "))
            if 0 <= apuesta <= 36 and numero_girado == apuesta:
                print(f"¡Felicidades! Has ganado. El número premiado ha sido el {numero_girado}.")
            else:
                print(f"Lo siento, no has ganado esta vez. El número premiado ha sido el {numero_girado}.")
        except ValueError:
            print("Entrada inválida. Debes ingresar un número entre 0 y 36.")
        
    elif opcion == 2:
        color_apuesta = input("Apuesta a un color (rojo/negro): ").strip().lower()
        if color_apuesta in ['rojo', 'negro'] and color_apuesta == color_girado:
            print(f"¡Felicidades! Has ganado, el número es {color_girado}.")
        else:
            print(f"Lo siento, no has ganado. El número es {color_girado}.")

    elif opcion == 3:
        try:
            docena_apuesta = int(input("Apuesta a una docena (1, 2 o 3): "))
            if docena_apuesta in [1, 2, 3] and en_docena(numero_girado) == docena_apuesta:
                print(f"¡Felicidades! Has ganado, el número está en la docena {docena_apuesta}.")
            else:
                print(f"Lo siento, no has ganado. El número está en la docena {en_docena(numero_girado)}.")
        except ValueError:
            print("Entrada inválida. Debes ingresar un número entre 1 y 3.")

    elif opcion == 4:
        mitad_apuesta = input("Apuesta a la mitad (alta/baja): ").strip().lower()
        if mitad_apuesta in ['alta', 'baja'] and mitad_apuesta == mitad_girada:
            print(f"¡Felicidades! Has ganado, el número está en la mitad {mitad_apuesta}.")
        else:
            print(f"Lo siento, no has ganado. El número está en la mitad {mitad_girada}.")

    elif opcion == 5:
        par_impar_apuesta = input("Apuesta a par o impar (par/impar): ").strip().lower()
        if par_impar_apuesta in ['par', 'impar'] and par_impar_apuesta == paridad_girada:
            print(f"¡Felicidades! Has ganado, el número es {paridad_girada}.")
        else:
            print(f"Lo siento, no has ganado. El número es {paridad_girada}.")

    else:
        print("Opción inválida. Por favor, selecciona un número del 1 al 5.")

