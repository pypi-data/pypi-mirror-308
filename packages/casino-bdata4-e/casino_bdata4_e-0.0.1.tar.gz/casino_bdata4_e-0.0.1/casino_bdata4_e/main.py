from casino_bdata4_e.ruleta import jugar_ruleta
from casino_bdata4_e.cartas import Blackjack, Poker
from casino_bdata4_e.bingo import jugar_bingo
from casino_bdata4_e.dado import JuegoDeDados  

def menu_principal():
    print("Bienvenido al casino!")
    print("1. Jugar a la Ruleta")
    print("2. Jugar con Cartas")
    print("3. Jugar al Bingo")
    print("4. Jugar con Dados") 
    print("5. Salir")

    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        jugar_ruleta()
    elif opcion == "2":
        jugar_con_cartas()
    elif opcion == "3":
        jugar_bingo()
    elif opcion == "4":
        jugar_con_dados()  
    elif opcion == "5":
        print("Gracias por jugar. ¡Hasta pronto!")
    else:
        print("Opción no válida, por favor intenta de nuevo.")
        menu_principal()

def jugar_con_cartas():
    print("Selecciona el juego de cartas que deseas jugar:")
    print("1. Blackjack")
    print("2. Poker")
    print("3. Volver al menú principal")

    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        jugar_blackjack()
    elif opcion == "2":
        jugar_poker()
    elif opcion == "3":
        menu_principal()
    else:
        print("Opción no válida, por favor intenta de nuevo.")
        jugar_con_cartas()

def jugar_blackjack():
    print("Iniciando Blackjack...")
    juego = Blackjack()
    juego.jugar()

def jugar_poker():
    print("Iniciando Poker...")
    juego = Poker(jugadores=2) 
    juego.jugar()

def jugar_con_dados():
    print("Iniciando el juego de Dados...")
    juego = JuegoDeDados()
    juego.jugar()

if __name__ == "__main__":
    menu_principal()

