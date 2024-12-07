import random
import numpy as np

# Function to generate bingo cards
def generate_cards(players):
    """
    Generates bingo cards for each player.
    Each card contains 15 random numbers from 1 to 90.
    """
    cards = {}
    for player in range(1, players + 1):
        card_name = []
        while len(card_name) < 15:
            number = random.randint(1, 90)
            if number not in card_name:
                card_name.append(number)
                card_name.sort()
        card_matrix = np.array(card_name).reshape(3, 5)
        cards[f"{player}"] = card_matrix
    return cards

# Function to display all cards
def show_all_cards(cards):
    """
    Displays all bingo cards available.
    """
    print("These are all the available cards:")
    for player, card in cards.items():
        print(f"Card {player}:")
        for row in card:
            print(row)
        print()

# Function to display a card with colors
def show_card(colors, card):
    """
    Displays the player's card with colored numbers.
    Green for marked numbers and red for unmarked ones.
    """
    for row in card:
        marked_row = [
            f"\033[32m{num}\033[0m" if colors[num] else f"\033[31m{num}\033[0m"
            for num in row
        ]
        print(' '.join(marked_row))
    print()  # Blank line to separate cards

# Function to select and display the player's card
def my_card(cards):  
    """
    Allows the player to choose a card to play with.
    Displays the selected card.
    """
    show_all_cards(cards)
    selection = input("Choose the number of the card you want to play with: ")
    if selection in cards:
        print(f"\nYou have chosen card {selection}. Your card is:")
        for row in cards[selection]:
            print(row)
        return cards[selection]
    else:
        print("Invalid card.")
        return None

# Function to generate the bingo drum
def generate_bingo_drum():
    """
    Generates the bingo drum with numbers from 1 to 90.
    """
    drum = []
    while len(drum) < 90:
        number = random.randint(1, 90)
        if number not in drum:
            drum.append(number)
    return drum

# Main game function
def play_bingo():
    """
    Main function to start and play the bingo game.
    Handles player input, bingo mechanics, and displays game progress.
    """
    while True:
        try:
            num_players = int(input("How many players do you want to play bingo with? "))
            if num_players >= 1:
                break
            else:
                print("Please enter a number greater than or equal to 1.")
        except ValueError:
            print("Please enter a valid number.")

    cards = generate_cards(num_players)
    card = my_card(cards)  
    if card is None:
        return
    
    drum = generate_bingo_drum()
    print("Bingo drum is ready, let the game begin!\n")
    marked = {n: False for n in card.flatten()}
    line = False
    bingo = False
    draws = 0
    line_printed = False
    colors = {n: False for n in card.flatten()}  # False for red, True for green
    
    while not bingo:
        input(f"\nPress Enter to draw a number from the drum... ({draws + 1} draws)")
        number = drum[draws]
        if number in marked:
            marked[number] = True
            colors[number] = True  # Update to green if marked
            print(f"The number {number} has been drawn -> YES, it’s on your card!")
        else:
            print(f"The number {number} has been drawn -> NO, it’s not on your card.")
        
        show_card(colors, card)  # Display the updated card with colors
        
        for i in range(3):
            if all(marked[card[i, j]] for j in range(5)):
                if not line_printed:
                    line_printed = True
                    print("You have a line! But the game continues.")
                break
        
        if all(marked[num] for num in card.flatten()):
            bingo = True
            print("Bingo! You've won!")
            break
        
        for player, other_card in cards.items():
            marked_player = {n: False for n in other_card.flatten()}
            for i in range(draws + 1):
                number = drum[i]
                if number in marked_player:
                    marked_player[number] = True

            for i in range(3):
                if all(marked_player[other_card[i, j]] for j in range(5)):
                    if not line_printed:
                        print("--------------------------------------------------")
                        print(f"Player {player} has a line! But the game continues.".upper())
                        print("--------------------------------------------------")
                        line_printed = True
                    break
            if all(marked_player[num] for num in other_card.flatten()):
                print("--------------------------------------------------")
                print(f"Player {player} has bingo! The game ends.".upper())
                return

        draws += 1

if __name__ == "__main__":
    play_bingo()
