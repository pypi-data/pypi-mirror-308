import random

PALOS = ['corazones', 'diamantes', 'tréboles', 'picas']
VALORES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

class Carta:
    def __init__(self, palo, valor):
        self.palo = palo
        self.valor = valor

    def __str__(self):
        return f"{self.valor} de {self.palo}"

class Baraja:
    def __init__(self):
        self.cartas = [Carta(palo, valor) for palo in PALOS for valor in VALORES]
        random.shuffle(self.cartas)

    def repartir_carta(self):
        return self.cartas.pop() if self.cartas else None

    def __len__(self):
        return len(self.cartas)
    

import random

class Baraja:
    def __init__(self):
        # Representación simplificada de una baraja de cartas
        self.cartas = [
            ('A', 11), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6),
            ('7', 7), ('8', 8), ('9', 9), ('10', 10), ('J', 10), ('Q', 10), ('K', 10)
        ] * 4  # 4 palos de cada carta
        random.shuffle(self.cartas)

    def repartir_carta(self):
        # Devuelve una carta y la remueve de la baraja
        return self.cartas.pop()

import random

class Baraja:
    def __init__(self):
        self.cartas = [
            ('A', 11), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6),
            ('7', 7), ('8', 8), ('9', 9), ('10', 10), ('J', 10), ('Q', 10), ('K', 10)
        ] * 4  # 4 palos de cada carta
        random.shuffle(self.cartas)

    def repartir_carta(self):
        return self.cartas.pop()

import random

class Baraja:
    def __init__(self):
        self.cartas = [
            ('A', 11), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6),
            ('7', 7), ('8', 8), ('9', 9), ('10', 10), ('J', 10), ('Q', 10), ('K', 10)
        ] * 4  # 4 palos de cada carta
        random.shuffle(self.cartas)

    def repartir_carta(self):
        return self.cartas.pop()

class Blackjack:
    def __init__(self):
        self.baraja = Baraja()
        self.mano_jugador = []
        self.mano_casa = []

    def calcular_valor_mano(self, mano):
        valor = 0
        ases = 0
        for carta, puntos in mano:
            if carta == 'A':
                ases += 1
            valor += puntos

        # Ajusta el valor de los Ases si es necesario
        while valor > 21 and ases > 0:
            valor -= 10
            ases -= 1

        return valor

    def jugar(self):
        print("¡Bienvenido a Blackjack!")
        
        # Reparte las primeras dos cartas al jugador y la casa
        for _ in range(2):
            self.mano_jugador.append(self.baraja.repartir_carta())
            self.mano_casa.append(self.baraja.repartir_carta())

        # Mostrar la mano inicial del jugador
        valor_jugador = self.calcular_valor_mano(self.mano_jugador)
        print("Tu mano inicial:", self.mano_jugador)
        print("Valor actual de tu mano:", valor_jugador)

        # Turno del jugador
        while True:
            if valor_jugador >= 21:
                break
            accion = input("¿Quieres pedir otra carta (p) o plantarte (s)? ").lower()
            if accion == 'p':
                carta = self.baraja.repartir_carta()
                self.mano_jugador.append(carta)
                valor_jugador = self.calcular_valor_mano(self.mano_jugador)
                
                # Mostrar el estado actual de la mano del jugador
                print("Carta nueva:", carta)
                print("Tu mano:", self.mano_jugador)
                print("Valor actual de tu mano:", valor_jugador)

                if valor_jugador > 21:
                    print("Te has pasado de 21. ¡Perdiste!")
                    return
            elif accion == 's':
                print("Te plantas con un valor de:", valor_jugador)
                break
            else:
                print("Opción no válida. Intenta de nuevo.")
        
        # Turno de la casa
        valor_casa = self.calcular_valor_mano(self.mano_casa)
        print("Mano inicial de la casa:", self.mano_casa)
        print("Valor actual de la mano de la casa:", valor_casa)
        
        while valor_casa < 17:
            carta = self.baraja.repartir_carta()
            self.mano_casa.append(carta)
            valor_casa = self.calcular_valor_mano(self.mano_casa)
            print("La casa pide una carta:", carta)
            print("Mano de la casa ahora:", self.mano_casa)
            print("Valor actual de la mano de la casa:", valor_casa)

        # Resultados
        print("\nResultado final:")
        print("Tu mano:", self.mano_jugador, "con un valor de:", valor_jugador)
        print("Mano de la casa:", self.mano_casa, "con un valor de:", valor_casa)

        if valor_jugador > 21:
            print("Te has pasado. La casa gana.")
        elif valor_casa > 21 or valor_jugador > valor_casa:
            print("¡Felicidades, ganaste!")
        elif valor_jugador < valor_casa:
            print("La casa gana.")
        else:
            print("Es un empate.")


        
class Poker:
    def __init__(self, jugadores=2):
        self.baraja = Baraja()
        self.jugadores = {f'Jugador {i+1}': [] for i in range(jugadores)}
        self.jugadores["Máquina"] = []  # Añadir la máquina como otro jugador

    def repartir_manos(self):
        for jugador in self.jugadores:
            self.jugadores[jugador] = [self.baraja.repartir_carta() for _ in range(5)]

    def mostrar_manos(self):
        for jugador, mano in self.jugadores.items():
            print(f"{jugador}: {', '.join(str(c) for c in mano)}")

    def calcular_fuerza_mano(self, mano):
        """
        Simula una función para calcular la fuerza de una mano de póker. Este es un ejemplo simplificado.
        La máquina puede basarse en esta "fuerza" para decidir qué hacer.
        """
        # Este es solo un ejemplo básico. Puedes agregar una lógica más avanzada de cálculo de manos de póker.
        valores = [c[0] for c in mano]
        if 'A' in valores:
            return 1  # Mano con As (simplemente para ilustrar)
        elif 'K' in valores:
            return 2  # Mano con Rey
        elif 'Q' in valores:
            return 3  # Mano con Reina
        return 0  # Manos básicas

    def jugar(self):
        self.repartir_manos()
        self.mostrar_manos()

        # Turno del jugador humano
        print("\nTu turno:")
        decision = input("¿Quieres plantar (s) o apostar (a)? ").lower()
        while decision not in ['s', 'a']:
            print("Opción no válida. Debes escribir 's' para plantar o 'a' para apostar.")
            decision = input("¿Quieres plantar (s) o apostar (a)? ").lower()
        
        if decision == 'a':
            print("Has apostado.")
        else:
            print("Te plantas.")

        # Turno de la máquina (decisión simple basada en la fuerza de la mano)
        print("\nTurno de la Máquina:")
        fuerza = self.calcular_fuerza_mano(self.jugadores["Máquina"])
        if fuerza >= 1:
            print("La máquina apuesta.")
        else:
            print("La máquina se planta.")

        # Resultado final
        print("\nResultado:")
        print("Tu mano:", self.jugadores["Jugador 1"])
        print("La mano de la máquina:", self.jugadores["Máquina"])

        # Simulación del ganador (puedes ajustar esto con reglas más avanzadas de póker)
        if fuerza >= 1:  # La máquina gana si tiene un As o superior
            print("¡La máquina gana!")
        else:
            print("¡Has ganado!")


