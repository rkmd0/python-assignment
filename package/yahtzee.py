# Yahtzee Game Logic Exercise
# Implement the logic for each function as described in the docstrings
import random
from collections import Counter

def roll_dice(n=5):
    """Roll n dice with values between 1-6."""
    # Hint: Generate a list of random integers between 1 and 6 with length n
    return [random.randint(1, 6) for i in range(n)]


def create_empty_scorecard():
    """Helper function to create an empty Yahtzee scorecard."""
    # Hint: Create a dictionary with keys for each score category, initialized to None
    # Categories include: '1', '2', ..., '6', 'three_of_a_kind', 'four_of_a_kind',
    # 'full_house', 'four_straight', 'five_straight', 'yahtzee', 'chance'
    category = {
        '1': None,
        '2': None,
        '3': None,
        '4': None,
        '5': None,
        '6': None,
        'three_of_a_kind': None,
        'four_of_a_kind': None,
        'full_house': None,
        'four_straight': None,
        'five_straight': None,
        'yahtzee': None,
        'chance': None
    }
    return category


def select_keep(dice):
    """Prompt user to select which dice to keep."""
    # Hint: Use input() to get user selection of which dice to keep.
    # Ensure selected numbers are in current dice.
    print(f"current dice: {dice}")
    
    while True:
        user_input = input("enter the dice you want to keep (e.g., 135), or press enter to reroll all: ")
        # because why wouldnt we want to reroll all
        if user_input == "":
            return []       

        try:
            kept = [int(ch) for ch in user_input]
        except ValueError:
            print("invalid input. please enter numbers corresponding to the dice values.")
            continue

        temp_dice = dice.copy()
        valid = True
        for value in kept:
            if value in temp_dice:
                temp_dice.remove(value)
            else:
                print(f"you don't have a die with value {value}. please try again.")
                valid = False
                break
        if valid:
            return kept
        else:
            print("please try again omg")


def reroll(dice, kept):
    """Reroll dice that weren't kept."""
    # Hint: Calculate number of dice to reroll, roll them, and combine with kept dice
    num_of_dice_to_reroll = len(dice) - len(kept)
    new_dice = roll_dice(num_of_dice_to_reroll)
    return kept + new_dice


def has_straight(dice, length):
    """Check for straights (sequences) in dice."""
    # Hint: Check if there is a sequence of 'length' consecutive numbers in dice
    unique_sorted = sorted(set(dice))
    count = 1
    for i in range(1, len(unique_sorted)):
        if unique_sorted[i] == unique_sorted[i - 1] + 1:
            count += 1
            if count >= length:
                return True
        else:
            count = 1

    return False

def evaluate(dice):
    """Calculate scores for all possible categories based on current dice."""
    # Hint: For each category, calculate the score based on the dice
    # Example: three_of_a_kind checks if there are at least three dice showing the same face
    scores = {}
    counts = Counter(dice)
    for i in range(1, 7):
        scores[str(i)] = dice.count(i) * i
    scores['three_of_a_kind'] = sum(dice) if max(counts.values()) >= 3 else 0
    scores['four_of_a_kind'] = sum(dice) if max(counts.values()) >= 4 else 0
    if sorted(counts.values()) == [2, 3]:
        scores['full_house'] = 25
    else:
        scores['full_house'] = 0
    scores['four_straight'] = 30 if has_straight(dice, 4) else 0
    scores['five_straight'] = 40 if has_straight(dice, 5) else 0
    scores['yahtzee'] = 50 if max(counts.values()) == 5 else 0
    scores['chance'] = sum(dice)
    return scores


def choose(scores, used):
    """Present available scoring options to player and get their selection."""
    # Hint: Display available scoring options to the user and get their choice
    print("\nAvailable categories:")
    available = {category: val for category, val in scores.items() if category not in used}

    for i, (category, val) in enumerate(available.items(), 1):
        print(f"{i}. {category} → {val}")

    while True:
        choice = input("Choose a category by number: ")
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(available):
                chosen_category = list(available.keys())[choice - 1]
                return chosen_category, scores[chosen_category]
        print("Invalid choice, try again.")


def display_scorecard(card):
    """Display current scorecard with all categories and their scores."""
    # Hint: Iterate over the scorecard and print each category along with its score
    print("\n--- Scorecard ---")
    upper_total = 0
    for category, score in card.items():
        print(f"{category:15} : {score}")
        if category in ['1', '2', '3', '4', '5', '6'] and score is not None:
            upper_total += score
    bonus = 35 if upper_total >= 63 else 0
    total = sum(v for v in card.values() if v is not None) + bonus
    print(f"Upper Section Total: {upper_total}")
    print(f"Bonus: {bonus}")
    print(f"Total Score: {total}")

def play_round(card):
    """Play one round of Yahtzee with 3 rolls."""
    # Hint: Implement the round logic which includes rolling and rerolling dice
    dice = roll_dice(5)
    print(f"First roll: {dice}")
    for roll in range(2, 4):  # até 2 rerolls
        kept = select_keep(dice)
        dice = reroll(dice, kept)
        print(f"Roll {roll}: {dice}")
        again = input("Reroll again? (y/n): ")
        if again.lower() != "y":
            break
    scores = evaluate(dice)
    used = [k for k, v in card.items() if v is not None]
    chosen_category, points = choose(scores, used)
    card[chosen_category] = points
    display_scorecard(card)
