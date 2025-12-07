""" Exercise: Collaborative programming. 
# We'll need classes to put these functions in and maybe a Player() class and a Board() class as well.
# 
"""

"""Edit by Michael"""
import random
class Player:
    """Base class for a King's Corner player.
    
    Attributes:
        name (str): The player's name.
        hand (list): List of cards in player's hand as (rank, color) tuples.
        score (int): The player's current score.
    """
    def __init__(self, name):
        """Initialize a new player.
        
        Args:
            name (str): The player's name.
        
        Side effects:
            Initializes hand as empty list and score as 0.
        """
        self.name = name
        self.hand = []
        self.score = 0
    
    def turn(self, state):
        raise NotImplementedError
    
    def draw_card(self, draw_pile):
        """Draw a card from the draw pile.
        
        Args:
            draw_pile (list): List of cards representing the draw pile.
            
        Returns:
            bool: True if card was drawn successfully, False if draw pile is empty.
            
        Side effects:
            Adds a card to player's hand and removes it from draw pile.
            Prints draw action to console.
        """
        if draw_pile:
            card = draw_pile.pop()
            self.hand.append(card)
            print(f"{self.name} draws a card")
            return True
        return False
    
    def add_score(self, points):
        """Add points to player's score.
        
        Args:
            points (int): Points to add to player's score.
            
        Side effects:
            Increases player's score by given points.
        """
        self.score += points
        
    def __str__(self):
        """Create string representation of player.
        
        Returns:
            str: Formatted string with player name, card count, and score.
        """
        return f"{self.name}: {len(self.hand)} cards, Score: {self.score}"    

class HumanPlayer(Player):
    
    def __init__(self, name):
    
        super().__init__(name)
        
    def turn(self, state):
        
        print(state)
        user = input(f"{self.name}, place a card from your hand")
        return user
        
class ComputerPlayer(Player):
    def __init__(self, name):
       
   
        self.name = name
    
    def turn(self, state):
        pass

def player_turn(player_hand, play_piles, draw_pile):
    """
    Process a complete turn for a player in King's Corner.
    
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
        
    Side effects:
        - Print updates to the console.
        - Modifies the 'hand' list when a card is successfully play.
        _ Modifies the 'piles' dictionary when a card or stack is moved.
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
            
'''
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
'''

""" Edit by Phakjira (Dec.6, 2025) """
import random

class Deck:
    ''' A deck of 52 cards used in the Kings Corner game.
    
    Cards are represented as (rank, color) tuples. Each rank appears four times: 
    twice in Red and twice in Black. 
   
    Attributes:
        cards (list of tuple): the current ordered list of cards in the deck. 
            Each card is a (rank, color) tuple such as ('Q', 'Red').
    '''
    
    RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    COLORS = ["Red", "Black"]  

    def __init__(self):
        '''Initialize a shuffled deck.
        
        Side effects:
            Creates and populates the attribute 'cards'.
        '''
        # Create 4 cards per rank: 2 Red + 2 Black
        self.cards = []
        for rank in self.RANKS:
            for color in self.COLORS:
                # Duplicate to simulate 52 cards
                self.cards.append((rank, color))
                self.cards.append((rank, color))  

        random.shuffle(self.cards)

    def deal(self):
        '''Deal 7 cards from top of deck to the player. 
        
        Returns: 
            list of tuples: the list of those 7 cards.
        
        Side effects:
            Removes 7 cards from the beginning of 'self.cards'.
        '''
        hand = self.cards[:7]
        self.cards = self.cards[7:]
        return hand
    
    def draw_one(self):
        '''Draw 1 card from the deck. 
        
        Returns:
            tuple: the top card of the deck. Ex. ('K', 'Black').
            
        Side effects:
            Removes 1 card from the beginning of 'self.cards'.
        '''
        return self.cards.pop(0)
    
    def turn_up_four(self):
        '''Draw 4 cards from the deck and place them in a cross (N, S, E, W).
        
            - Note: These are the foundation piles.
        
        Returns:
            foundation (dict): a dictionary with keys 'N', 'S', 'E', 'W' and 
            their drawn cards.
            
        Side effects:
            Removes 4 cards from the beginning of 'self.cards'.
        '''
        foundations = {
            "N": self.draw_one(),
            "S": self.draw_one(),
            "E": self.draw_one(),
            "W": self.draw_one(),
        }
        return foundations

    def __str__(self):
        '''Return an informal string of cards (Human-readable formate).'''
        return str(self.cards)
# Testing
deck = Deck()
print('List of 52 cards:\n')
print(deck)
print(f"\nList of 7 cards:\n\n {deck.deal()}")
print(f"\nFoundation cards:\n\n {deck.turn_up_four()}")
print(f"\nCards left in deck: {len(deck.cards)}\n")

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

