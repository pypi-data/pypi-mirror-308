import random

def flip_coin():
    """
    Simulates a coin flip and returns the result as 'Heads' or 'Tails'.
    """
    result = random.choice(["Heads", "Tails"])
    return result

def play_coin():
    """
    Plays a simple Heads or Tails game.
    """
    print("Welcome to the Heads or Tails game!")
    choice = input("Choose 'Heads' or 'Tails': ").capitalize()
    
    if choice not in ["Heads", "Tails"]:
        print("Invalid option. Please choose 'Heads' or 'Tails'.")
        return

    result = flip_coin()
    print(f"The coin landed on: {result}")
    
    if choice == result:
        print("Congratulations! You won.")
    else:
        print("Sorry, you lost. Try again!")


