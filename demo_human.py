from kings_corner import HumanPlayer
player = HumanPlayer("Demo_Player")
player.hand = [('K', 'Red'), (5, 'Black'), (2, 'Red'), ('Q', 'Black')]
# Create a simple game state
state = {
    'piles': {
        'N': [(6, 'Red')],
        'S': [],
        'E': [(4, 'Black')],
        'W': [],
        'NE': [],
        'NW': [],
        'SE': [],
        'SW': []
    },
    'draw_pile': [('A', 'Red'), (3, 'Black')]
}
print("\nTaking a turn...")
print("(Choose options 1-4 to test different actions)")
action = player.turn(state)
print(f"\nFinal action result: {action}")