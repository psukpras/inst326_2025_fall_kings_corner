from kings_corner import Deck, HumanPlayer, ComputerPlayer, player_turn

print("=== Complete Game Demo ===")
deck = Deck()
human = HumanPlayer("Player1")
computer = ComputerPlayer("CPU")
human.hand = deck.deal()
computer.hand = deck.deal()
piles = deck.turn_up_four()
foundation_cards = deck.turn_up_four()
piles = {}
for position, card in foundation_cards.items():
    piles[position] = [card]
for corner in ['NW', 'NE', 'SW', 'SE']:
    piles[corner] = []

draw_pile = deck.cards  # Remaining cards become draw pile

print("Game initialized!")
print(f"Human cards: {human.hand}")
print(f"Computer cards: {computer.hand}")
print(f"Foundation piles: {piles}")
print(f"Draw pile: {len(draw_pile)} cards")
print("\n--- Simulating first few turns ---")

# Human turn
print("\n[Human Turn - Choose option 3 or 4 please]")
human_hand, piles, draw_pile, completed = player_turn(
    human.hand, piles, draw_pile, human
)
print(f"Turn completed: {completed}")

# Computer turn
print("\n[Computer Turn]")
computer_hand, piles, draw_pile, completed = player_turn(
    computer.hand, piles, draw_pile, computer
)
print(f"Turn completed: {completed}")
print(f"\nAfter first round:")
print(f"Human hand: {len(human_hand)} cards: {human_hand}")
print(f"Computer hand: {len(computer_hand)} cards: {computer_hand}")
print(f"Draw pile: {len(draw_pile)} cards remaining")