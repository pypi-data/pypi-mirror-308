import random

# Definition of colors for each number on the roulette wheel.
COLORS = {n: 'red' if n in {
    1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36} else 'black' for n in range(1, 37)}

# Definition of dozens.
DOZENS = {
    1: range(1, 13),
    2: range(13, 25),
    3: range(25, 37)
}

# Definition of columns.
COLUMNS = {
    1: {1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34},
    2: {2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35},
    3: {3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36}
}

def spin_roulette():
    """
    Simulates spinning the roulette wheel.
    
    Returns:
        int: The number that the roulette lands on (0-36).
    """
    return random.randint(0, 36)

def get_color(number):
    """
    Determines the color of a roulette number.
    
    Args:
        number (int): The number on the roulette wheel.
        
    Returns:
        str: 'red', 'black', or 'green' (for 0).
    """
    return COLORS.get(number, 'green')  # 0 is green

def is_even(number):
    """
    Checks if a number is even.
    
    Args:
        number (int): The number to check.
        
    Returns:
        bool: True if the number is even, False otherwise.
    """
    return number != 0 and number % 2 == 0

def is_odd(number):
    """
    Checks if a number is odd.
    
    Args:
        number (int): The number to check.
        
    Returns:
        bool: True if the number is odd, False otherwise.
    """
    return number != 0 and number % 2 == 1

def in_dozen(number):
    """
    Determines which dozen a number belongs to.
    
    Args:
        number (int): The number to check.
        
    Returns:
        int or None: The dozen (1, 2, or 3) or None if not found.
    """
    for dozen, numbers in DOZENS.items():
        if number in numbers:
            return dozen
    return None

def in_column(number):
    """
    Determines which column a number belongs to.
    
    Args:
        number (int): The number to check.
        
    Returns:
        int or None: The column (1, 2, or 3) or None if not found.
    """
    for column, numbers in COLUMNS.items():
        if number in numbers:
            return column
    return None

def is_half(number):
    """
    Determines if a number is in the 'high' or 'low' half of the roulette.
    
    Args:
        number (int): The number to check.
        
    Returns:
        str: 'high', 'low', or 'none' (for 0).
    """
    if number == 0:
        return "none"
    return "high" if number > 18 else "low"

def play_roulette():
    """
    Main function to play roulette. Allows the user to place different types of bets
    and checks the outcome after spinning the wheel.
    """
    print("Welcome to roulette! What would you like to bet on?")
    print("1. Specific number (0-36)")
    print("2. Color (red/black)")
    print("3. Dozen (1, 2, or 3)")
    print("4. Half (high/low)")
    print("5. Even or Odd")

    try:
        option = int(input("Select an option (1-5): "))
    except ValueError:
        print("Invalid option. Please enter a number between 1 and 5.")
        return

    spun_number = spin_roulette()
    spun_color = get_color(spun_number)
    spun_half = is_half(spun_number)
    spun_parity = "even" if is_even(spun_number) else "odd"

    if option == 1:
        try:
            bet = int(input("Bet on a number between 0 and 36: "))
            if 0 <= bet <= 36 and spun_number == bet:
                print(f"Congratulations! You won. The winning number was {spun_number}.")
            else:
                print(f"Sorry, you lost. The winning number was {spun_number}.")
        except ValueError:
            print("Invalid input. You must enter a number between 0 and 36.")
        
    elif option == 2:
        bet_color = input("Bet on a color (red/black): ").strip().lower()
        if bet_color in ['red', 'black'] and bet_color == spun_color:
            print(f"Congratulations! You won. The number is {spun_color}.")
        else:
            print(f"Sorry, you lost. The number is {spun_color}.")

    elif option == 3:
        try:
            bet_dozen = int(input("Bet on a dozen (1, 2, or 3): "))
            if bet_dozen in [1, 2, 3] and in_dozen(spun_number) == bet_dozen:
                print(f"Congratulations! You won. The number is in dozen {bet_dozen}.")
            else:
                print(f"Sorry, you lost. The number is in dozen {in_dozen(spun_number)}.")
        except ValueError:
            print("Invalid input. You must enter a number between 1 and 3.")

    elif option == 4:
        bet_half = input("Bet on the half (high/low): ").strip().lower()
        if bet_half in ['high', 'low'] and bet_half == spun_half:
            print(f"Congratulations! You won. The number is in the {bet_half} half.")
        else:
            print(f"Sorry, you lost. The number is in the {spun_half} half.")

    elif option == 5:
        bet_parity = input("Bet on even or odd (even/odd): ").strip().lower()
        if bet_parity in ['even', 'odd'] and bet_parity == spun_parity:
            print(f"Congratulations! You won. The number is {spun_parity}.")
        else:
            print(f"Sorry, you lost. The number is {spun_parity}.")

    else:
        print("Invalid option. Please select a number between 1 and 5.")


