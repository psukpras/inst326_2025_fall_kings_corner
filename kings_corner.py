""" Exercise: Collaborative programming. 
# We'll need classes to put these functions in and maybe a Player() class and a Board() class as well.
# 
"""

"""Edit by Michael"""
def player_turn(player_hand, play_piles, draw_pile):
    """Process a complete turn for a player in King's Corner.
    
    Args:
        player_hand: List of cards in player's hand
        play_piles: Dictionary of play piles {'A': [], 'B': [], 'C': [], 'D': [], 'K1': [], 'K2': [], 'K3': [], 'K4': []}
        draw_pile: List representing the draw pile
    
    Returns:
        tuple: (player_hand, play_piles, draw_pile, turn_completed)
    """
    turn_completed = False
    if not turn_completed:
        move_type = get_player_move_choice()
        if move_type == "play_card":
            turn_completed = try_play_card(player_hand, play_piles)
        elif move_type == "move_pile":
            turn_completed = try_move_pile(play_piles)
        elif move_type == "draw_card" and draw_pile:
            player_hand.append(draw_pile.pop())
            turn_completed = True
        elif move_type == "end_turn":
            turn_completed = True
    # If still no move completed and draw pile exists, draw a card
    if not turn_completed and draw_pile:
        player_hand.append(draw_pile.pop())
        turn_completed = True
    return player_hand, play_piles, draw_pile, turn_completed

# Mock functions that would be implemented by other group members
def get_player_move_choice():
    """Mock function to get player's move choice"""
    # In final implementation, this would get real user input
    choices = ["play_card", "move_pile", "draw_card", "end_turn"]
    # Simulating player choosing to play a card
    return "play_card"

def try_play_card(player_hand, play_piles):
    """Mock function to attempt playing a card from hand to a pile"""
    return True

def try_move_pile(play_piles):
    """Mock function to attempt moving one pile onto another"""
    # In final implementation, this would validate pile movement rules
    # For now, just simulate a successful move
    print("Moved one pile onto another")
    return True

"""Edit by Phakjira"""

def valid_moves(hand, card_to_play, piles, move_from = None, move_to = None):
    '''Check whether the player's move is valid according to King's Corner 
    rules.
    
        - If valid: the game state is updated (pile changed, card removed 
                from hand)
        - If invalid: move rejected, no state change.
    
    Args:
        hand (list of tuples): all of the cards currently in the player's hand.
            Including rank and color of each card.
        card_to_play (tuple or None): card that player wants to play. 
            (rank, color).
        piles (dict): all foundation and corner piles. Each key is a pile name 
        (e.g., 'N', 'S') and each value is a list of cards in that pile.
        move_from (str, optional): name of the pile the player wants to move 
            a card or a stack from. Defaults to None.
        move_to (str, optional): name of the pile the player wants to move 
            a card or a stack to. Defaults to None.
            
    Returns:
        str : a message indicating whether the move is valid or invalid.
    '''
    # Rank order from high to low
    rank_order = ['K', 'Q', 'J', 10, 9, 8, 7, 6, 5, 4, 3, 2, 'A']
    corner_piles = ['NW', 'NE', 'SW', 'SE']
    side_piles = ['N', 'S', 'E', 'W']

    # Play card on hand
    if move_to is None:
        return 'Invalid Move! Must choose where to place a card.'
    
    if move_from is None and move_to is not None:
        # Check if player has that card
        if card_to_play not in hand:
            return f"Invalid Move! You don't have {card_to_play} in hand."
        
        # Handle invalid corners names
        if move_to not in corner_piles and move_to not in side_piles:
            return f'Invalid Move! Corner {move_to} doesn\'t exist.'

        # Handle corner piles
        if move_to in corner_piles:
            if card_to_play[0] == 'K':
                piles[move_to].append(card_to_play)
                hand.remove(card_to_play)
                return f"Placed {card_to_play} on {move_to}."
            else:
                return('Invalid Move! Only Kings can be placed in empty '+
            'corner piles.')

        # Handle side piles
        if move_to in side_piles:
            # Handle empty pile
            if not piles[move_to]:
                if card_to_play[0] == 'K':
                    return ('Invalid Move! Kings can be placed only in the '+
                        'corner piles.')
                piles[move_to].append(card_to_play)
                hand.remove(card_to_play)
                return f'Placed {card_to_play} on {move_to}'
           
            # Last card from the pile
            top_card = piles[move_to][-1]
            
            # Unpacked
            top_rank, top_color = top_card
            play_rank, play_color = card_to_play
            
            # Handle descending rank rule
            if rank_order.index(play_rank) != rank_order.index(top_rank) + 1:
                return ('Invalid Move! The card must be a rank ' + 
                    f'lower than {top_card}')
            
            # Handle alternating color rule
            if play_color == top_color:
                return 'Invalid Move! Alternate colors rule applies.'
                
            piles[move_to].append(card_to_play)
            hand.remove(card_to_play)
            print (f'{move_to} changed: {piles[move_to]}')
            print (f'Current Hand changed to: {hand}')
            return f'Placed {card_to_play} on {move_to}'
        
    # Move a full pile
    if move_from is not None and move_to is not None:
        # Handle invalid corners names
        if move_to not in corner_piles and move_to not in side_piles:
            return f'Invalid Move! Corner {move_to} doesn\'t exist.'
        
        if move_from not in corner_piles and move_from not in side_piles:
            return f'Invalid Move! Corner {move_to} doesn\'t exist.'        
        
        stack = piles[move_from]
        
        if not stack:
            return 'Invalid Move! This pile is empty.'
        
        # Move to a corner pile
        if move_to in corner_piles:
            # Handle empty corner pile (move_to)
            if not piles[move_to]:
                return "Invalid Move! Can't move a full pile onto an empty pile."
           
            # Last card from the pile
            top_card = piles[move_to][-1]
            
            # Unpacked
            top_rank, top_color = top_card
            
            # First card of the moving pile (move_from)
            connect_card = stack[0]
            connect_rank, connect_color = connect_card
            
            # Handle descending rank rule
            if rank_order.index(connect_rank) != rank_order.index(top_rank) + 1:
                return ('Invalid Move! First card of the pile must be a rank ' 
                        + f'lower than {top_card}')
           
            # Handle alternating color rule
            if connect_color == top_color:
                return 'Invalid Move! Alternate colors rule applies.'
            
            # Attach the first card of the moving pile to the last card of 
            # the another pile.
            piles[move_to] += stack
            piles[move_from] = []
            print (f'{move_to} changed : {piles[move_to]}')
            print (f'{move_from} changed : {piles[move_from]}')
            return f'Moved stack pile from {move_from} onto {move_to}'
        
        # Move to a side pile
        if move_to in side_piles:
            # Handle empty side pile (move_to)
            if not piles[move_to]:
                # Just move the pile to the empty side pile
                piles[move_to] += stack
                piles[move_from] = []
                print (f'{move_to} changed : {piles[move_to]}')
                print (f'{move_from} changed : {piles[move_from]}')
                return f'Moved stack pile from {move_from} onto {move_to}'
            
            # ---If there's an existing pile---
            
            top_card = piles[move_to][-1]
            top_rank, top_color = top_card
            
            # First card of the moving pile
            connect_card = stack[0]
            connect_rank, connect_color = connect_card
            
            if rank_order.index(connect_rank) != rank_order.index(top_rank) + 1:
                return ('Invalid Move! First card of the pile must be a rank ' 
                        + f'lower than {top_card}')
            if connect_color == top_color:
                return 'Invalid Move! Alternate colors rule applies.'
            # Attach the first card of the moving pile to the last card of 
            # the another pile.
            piles[move_to] += stack
            piles[move_from] = []
            print (f'{move_to} changed : {piles[move_to]}')
            print (f'{move_from} changed : {piles[move_from]}')
            return f'Moved stack pile from {move_from} onto {move_to}'
            

# Fake data for testing
hand = [
    ('A', 'R'), (2, 'R'), ('K', 'B'), 
    (2, 'B'), (3, 'B'), ('J', 'R'), 
    ('Q', 'B')
]

piles = {
    'N' : [(3, 'R'), (2,'B')],
    'E' : [(4, 'B')],
    'S' : [('A', 'R')],
    'W' : [],
    'NE' : [('K', 'B')],
    'NW' : [],
    'SE' : [],
    'SW' : []
}            

print(valid_moves(hand, (4, 'R'), piles))
print(valid_moves(hand, (4, 'R'), piles, move_to = 'N'))
print(valid_moves(hand, (2, 'B'), piles, move_to = 'S'))
print(valid_moves(hand, ('A', 'R'), piles, move_to = 'B'))
print(valid_moves(hand, ('A', 'R'), piles, move_to = 'N'))
print(valid_moves(hand, None, piles, move_from = 'N', move_to = 'E'))
print(valid_moves(hand, None, piles, move_from = 'N', move_to = 'NE'))
print(valid_moves(hand, None, piles, move_from = 'E', move_to = 'NE'))
print(valid_moves(hand, None, piles, move_from = 'E', move_to = 'T'))

"""Edit by Charlie"""

def end_round(playerturnhand):
    """
    Args: playerturnhand is a list of tuples displaying the amount of cards
        that display the number and color of each card
    """
    score = 0
    for num, color in playerturnhand:
        if num == 13:
            score += 10
        else:
            score += 1
    return score

def win_condition(p1_score, p2_score):
    """
    Args: p1 and p2 score is the players final score
    """
    if p1_score >= 25:
        print(f"player 2 wins! score:{p2_score}")
    elif p2_score >= 25:
        print(f"player 1 wins! score:{p1_score}")
    else:
        return None

p1 = [(13, "r"), (10, "b"), (8, "r")]
p2 = [(9, "b"), (12, "b"), (3, "r")]

p1_score = end_round(p1)
p2_score = end_round(p2)

print(f"p1 score:{p1_score}")
print(f"p2 score:{p2_score}")

win_condition(p1_score, p2_score) #no winner since only one round was played

"""Edit by Attowla"""
def build_board(rows, cols):
    """
    Laying out the initial board.

    Args:
        rows (int): Amount of rows in each board
        cols (int): Amount of columns in each board

    Returns:
        _type_: _description_
    """
    board = [["example card" for _ in range(cols)] for _ in range(rows)]
    return board

board = build_board(3, 3)

for row in board:
    print(" ".join(row))

