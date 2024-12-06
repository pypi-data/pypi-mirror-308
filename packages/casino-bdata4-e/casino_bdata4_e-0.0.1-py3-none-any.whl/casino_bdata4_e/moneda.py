import random

def lanzar_moneda():
    # Generamos un número aleatorio para determinar cara o cruz
    resultado = random.choice(["Cara", "Cruz"])
    return resultado

def jugar_moneda():
    print("¡Bienvenido al juego de Cara o Cruz!")
    eleccion = input("Elige 'Cara' o 'Cruz': ").capitalize()
    
    if eleccion not in ["Cara", "Cruz"]:
        print("Opción inválida. Por favor elige 'Cara' o 'Cruz'.")
        return

    resultado = lanzar_moneda()
    print(f"La moneda ha caído en: {resultado}")
    
    if eleccion == resultado:
        print("¡Felicidades! Has ganado.")
    else:
        print("Lo siento, has perdido. ¡Inténtalo de nuevo!")

