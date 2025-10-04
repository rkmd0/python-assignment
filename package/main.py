from yahtzee import *

def main():
    """Main game loop for Yahtzee."""
    print("Welcome to Yahtzee!")

    # Initialize scorecard
    # --- [Your code here] ---
    card = create_empty_scorecard()
    #print(card)

    # Play 13 rounds 
    # --- [Your code here] ---
    for round_num in range(1,14):
        print("round start")
        play_round(card)

    
    # Display scorecard after each round
    # --- [Your code here] ---
    display_scorecard(card)

    # Calculate final score
    # If upper section total >= 63, bonus = 35
    # --- [Your code here] ---
    upper_total = sum((card[str(i)] or 0) for i in range(1,7)) # sum the categories values, 0 if none
    bonus_total = 35 if upper_total >= 63 else 0 # grant the bonus if it is
    final_score = sum(v for v in card.values() if v is not None) + bonus_total
    
    print(f"\nGame over! Final score: {final_score}")

if __name__ == "__main__":
    main()
