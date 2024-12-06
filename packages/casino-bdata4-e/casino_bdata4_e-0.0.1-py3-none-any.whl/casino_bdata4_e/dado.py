import random

class DadoError(Exception):
    """Excepción base para los errores relacionados con el juego de dados."""
    pass

class ApuestaInvalidaError(DadoError):
    """Excepción lanzada cuando la apuesta no es válida."""
    pass

class JuegoDeDados:
    @staticmethod
    def lanzar_dado():
        """
        Simula el lanzamiento de un dado de seis caras.
        Returns:
            int: Un número aleatorio entre 1 y 6.
        """
        return random.randint(1, 6)

    def numero_especifico(self):
        try:
            apuesta = int(input("Apuesta un número entre 1 y 6: "))
            if apuesta < 1 or apuesta > 6:
                raise ApuestaInvalidaError("Número de apuesta inválido. Debe estar entre 1 y 6.")
            numero_lanzado = self.lanzar_dado()
            if numero_lanzado == apuesta:
                print(f"¡Felicidades! Has ganado. El número lanzado ha sido el {numero_lanzado}.")
            else:
                print(f"Lo siento, no has ganado esta vez. El número lanzado ha sido el {numero_lanzado}.")
        except ValueError:
            print("Error: Debes ingresar un número.")
        except ApuestaInvalidaError as e:
            print(e)

    def alto_o_bajo(self):
        try:
            alto_bajo = input("Apuesta a Alto (4-6) o Bajo (1-3): ").strip().lower()
            if alto_bajo not in ['alto', 'bajo']:
                raise ApuestaInvalidaError("Opción inválida. Debes elegir 'alto' o 'bajo'.")
            numero_lanzado = self.lanzar_dado()
            if (alto_bajo == 'alto' and numero_lanzado > 3) or (alto_bajo == 'bajo' and numero_lanzado <= 3):
                print(f"¡Felicidades! Has ganado. El número lanzado es {alto_bajo}.")
            else:
                print(f"Lo siento, no has ganado esta vez. El número lanzado es {'alto' if numero_lanzado > 3 else 'bajo'}.")
        except ApuestaInvalidaError as e:
            print(e)

    def par_o_impar(self):
        try:
            par_impar = input("Apuesta a par o impar: ").strip().lower()
            if par_impar not in ['par', 'impar']:
                raise ApuestaInvalidaError("Opción inválida. Debes elegir 'par' o 'impar'.")
            numero_lanzado = self.lanzar_dado()
            if (par_impar == 'par' and numero_lanzado % 2 == 0) or (par_impar == 'impar' and numero_lanzado % 2 == 1):
                print(f"¡Felicidades! Has ganado. El número lanzado es {'par' if numero_lanzado % 2 == 0 else 'impar'}.")
            else:
                print(f"Lo siento, no has ganado esta vez. El número lanzado es {'par' if numero_lanzado % 2 == 0 else 'impar'}.")
        except ApuestaInvalidaError as e:
            print(e)

    def suma_objetivo(self):
        try:
            objetivo = int(input("Apuesta a una suma (2-12): "))
            if objetivo < 2 or objetivo > 12:
                raise ApuestaInvalidaError("Número inválido. Debe estar entre 2 y 12.")
            dado1 = self.lanzar_dado()
            dado2 = self.lanzar_dado()
            suma = dado1 + dado2
            print(f"Lanzaste {dado1} y {dado2}. Suma total: {suma}")
            if suma == objetivo:
                print("¡Felicidades! Has ganado.")
            else:
                print("Lo siento, no has ganado esta vez.")
        except ValueError:
            print("Error: Debes ingresar un número.")
        except ApuestaInvalidaError as e:
            print(e)

    def mayor_menor_igual(self):
        try:
            dado1 = self.lanzar_dado()
            print(f"El primer dado es: {dado1}")
            eleccion = input("¿Crees que el próximo lanzamiento será 'mayor', 'menor' o 'igual'? ").strip().lower()
            if eleccion not in ['mayor', 'menor', 'igual']:
                raise ApuestaInvalidaError("Opción inválida. Debes elegir 'mayor', 'menor' o 'igual'.")
            dado2 = self.lanzar_dado()
            print(f"El segundo dado es: {dado2}")
            if (eleccion == 'mayor' and dado2 > dado1) or (eleccion == 'menor' and dado2 < dado1) or (eleccion == 'igual' and dado2 == dado1):
                print("¡Felicidades! Has ganado.")
            else:
                print("Lo siento, no has ganado esta vez.")
        except ApuestaInvalidaError as e:
            print(e)
    
    def exacto_o_aproximado(self):
        """Juego en el que el usuario apuesta a una suma exacta o cercana entre dos dados."""
        try:
            objetivo = int(input("Apuesta a una suma (2-12): "))
            if objetivo < 2 or objetivo > 12:
                raise ApuestaInvalidaError("Número inválido. Debe estar entre 2 y 12.")
            
            dado1 = self.lanzar_dado()
            dado2 = self.lanzar_dado()
            suma = dado1 + dado2
            print(f"Lanzaste {dado1} y {dado2}. Suma total: {suma}")
            
            if suma == objetivo or abs(suma - objetivo) == 1:
                print("¡Felicidades! Has ganado.")
            else:
                print("Lo siento, no has ganado esta vez.")
        except ValueError:
            print("Error: Debes ingresar un número.")
        except ApuestaInvalidaError as e:
            print(e)

    def escalera(self):
        """Juego en el que el usuario acumula puntos si lanza números en orden ascendente."""
        try:
            puntos = 0
            anterior = 0
            while True:
                dado = self.lanzar_dado()
                print(f"Lanzaste un {dado}")
                
                if dado > anterior:
                    puntos += 1
                    anterior = dado
                    print(f"¡Subiste en la escalera! Tienes {puntos} puntos.")
                    continuar = input("¿Quieres continuar? (s/n): ").strip().lower()
                    if continuar != 's':
                        break
                else:
                    print("¡Has fallado! La escalera se rompió.")
                    puntos = 0
                    break
            
            print(f"Juego terminado. Has acumulado {puntos} puntos.")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")

    def tres_dados_mayor(self):
        """Juego en el que el usuario apuesta si el mayor número lanzado entre tres dados será par o impar."""
        try:
            eleccion = input("Apuesta al mayor número: ¿será 'par' o 'impar'? ").strip().lower()
            if eleccion not in ['par', 'impar']:
                raise ApuestaInvalidaError("Opción inválida. Debes elegir 'par' o 'impar'.")
            
            dado1 = self.lanzar_dado()
            dado2 = self.lanzar_dado()
            dado3 = self.lanzar_dado()
            print(f"Lanzaste {dado1}, {dado2} y {dado3}")
            
            mayor = max(dado1, dado2, dado3)
            print(f"El número mayor es {mayor}")
            
            if (eleccion == 'par' and mayor % 2 == 0) or (eleccion == 'impar' and mayor % 2 == 1):
                print("¡Felicidades! Has ganado.")
            else:
                print("Lo siento, no has ganado esta vez.")
        except ApuestaInvalidaError as e:
            print(e)

    def jugar(self):
        opciones = {
            1: self.numero_especifico,
            2: self.alto_o_bajo,
            3: self.par_o_impar,
            4: self.suma_objetivo,
            5: self.mayor_menor_igual,
            6: self.exacto_o_aproximado,
            7: self.escalera,
            8: self.tres_dados_mayor
        }
        print("Bienvenido al juego de dados. ¿A qué quieres apostar?")
        print("1. Número específico (1-6)")
        print("2. Alto o Bajo (1-3 es bajo, 4-6 es alto)")
        print("3. Par o Impar")
        print("4. Suma Objetivo (apuesta a que la suma de dos dados lanzados será un número específico entre 2 y 12)")
        print("5. Mayor, Menor o Igual en dos lanzamientos")
        print("6. Exacto o Aproximado (apuesta a una suma específica o cercana entre dos dados)")
        print("7. Escalera (acumula puntos lanzando números en orden ascendente)")
        print("8. Tres Dados Mayor (apuesta si el mayor número lanzado será par o impar)")

        try:
            opcion = int(input("Selecciona una opción (1-8): "))
            if opcion in opciones:
                opciones[opcion]()
            else:
                raise ApuestaInvalidaError("Opción inválida. Debes seleccionar un número entre 1 y 8.")
        except ValueError:
            print("Error: Debes ingresar un número.")
        except ApuestaInvalidaError as e:
            print(e)

   