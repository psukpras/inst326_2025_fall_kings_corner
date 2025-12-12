""" Kings Corner Game """

import random 

""" Edit by Phakjira (Dec.10, 2025) """

class KingsGame:
    """ 
    Manage and run a full game of King's Corner.
    
    Attributes:
        deck (Deck): The deck of cards used for the game.
        p1 (HumanPlayer): Player 1 object.
        p2 (HumanPlayer or ComputerPlayer): Player 2 object.
        foundation_cards (dict): The initial four face-up piles (N, S, E, W).
        piles (dict): Dictionary mapping pile names to lists of cards.
        draw_pile (list): Remaining undealt cards after setup.
    """
    def __init__(self):
        """
        Initialize a new King's Corner game.
        
        Side effects:
            Set instance attributes for deck, p1, p2, foundation_cards,
                piles, draw_pile.
            Prompts the user to select a mode (P2 or CPU).
            Prompts the user to enter their name.
            Modifies the deck by dealing cards and removing foundation cards.
            
        Raises:
            ValueError: If the user enters a mode other than "P2" or "CPU".
        """
        # Create deck
        self.deck = Deck()
        
        # Ask for mode
        mode_selection = input('Do you want to play against "P2" ' + 
                               'or "CPU?" ').strip()
        # P2 mode
        if(mode_selection == "P2".casefold()):
            # Ask player 1 name
            player_name = input("Enter Player 1 name: ").strip()
            if player_name == "":
                player_name = "Player 1"
            # Ask player 2 name
            player2_name = input("Enter Player 2 name: ").strip()
            if player2_name == "":
                player2_name = "Player 2"
            # Create players
            self.p1 = HumanPlayer(player_name)
            self.p2 = HumanPlayer(player2_name)
        # CPU mode
        elif(mode_selection == "CPU".casefold()):
            # Ask player 1 name
            player_name = input("Enter your name: ").strip()
            if player_name == "":
                player_name = "Player 1"
             # Create players
            self.p1 = HumanPlayer(player_name)
            self.p2 = ComputerPlayer("Computer")
        else:
            raise ValueError('Invalid mode selection. Choose "P2" or "CPU".')
        
        # Deal hands
        self.p1.hand = self.deck.deal()
        self.p2.hand = self.deck.deal()

        # Turn up N/S/E/W foundations 
        self.foundation_cards = self.deck.turn_up_four()

        # Convert them into piles (lists)
        self.piles = {}
        for position, card in self.foundation_cards.items():
            self.piles[position] = [card]
        for corner in ['NW', 'NE', 'SW', 'SE']:
            self.piles[corner] = []
        
        # Draw pile is whatever remains in the deck
        self.draw_pile = self.deck.cards
        
    def play_game(self):
        """
        Run the main gameplay loop for King's Corner.
        
        Game ends when:
            - A player empties their hand, or
            - The draw pile becomes empty.

        On ending, both players' scores are calculated using end_round(), and
        win_condition() is used to determine and display the winner.
        
        Side effects:
            Prints the board, piles, scores, and game status each turn.
            Calls player_turn(), which may modify hands and piles.
            Mutates self.piles, self.draw_pile, and player hands.
            Prints final results.
        """
        print("\n=== Starting King’s Corner ===\n")

        players = [self.p1, self.p2]
        turn_index = 0

        while True:
            current_player = players[turn_index % 2]
            
            print("===========================")
            # Build and print updated board each turn
            board = build_board(self.piles)
            print("\nCurrent Board:\n")
            for row in board:
                print(  " ".join(row))
            # Print updated piles each turn
            print("\nCurrent piles:\n")
            for pile_name, cards in self.piles.items():
                print(f"  {pile_name}: {cards}")
            # Remaining # card in deck
            print(f"\nCards left in deck: {len(self.deck)}\n")

            # Use existing player_turn function
            current_player.hand, self.piles, self.draw_pile, done = (
                player_turn(current_player.hand, self.piles, self.draw_pile, 
                current_player)
            )
                       
            # Check end conditions
            end_game = False
            reason = ""

            # If Player emptied their hand
            if len(current_player.hand) == 0:
                end_game = True
                reason = f"{current_player.name} emptied their hand!"

            # If there's No cards left in draw pile
            elif len(self.draw_pile) == 0:
                end_game = True
                reason = "No cards left in the draw pile!"

            # Calculate scores and announce winner if game ends
            if end_game:
                print(f"\n{reason} Round over.\n")
                p1_score = end_round(self.p1.hand)
                p2_score = end_round(self.p2.hand)
                print(f"{self.p1.name} score: {p1_score}")
                print(f"{self.p2.name} score: {p2_score}\n")
                win_condition(p1_score, p2_score)
                break

            turn_index += 1
            
""" Edit by Michael 12.06.2025 """

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
        """
        Execute a player's turn.
        
        Args:
            state (dict): Current game state containing piles and draw pile.
            
        Returns:
            str: Action taken by the player ('draw', 'end', 'played_card', 
                'moved_pile', etc.)
            
        Raises:
            NotImplementedError: Must be implemented by subclass.
        """
        raise NotImplementedError
    
    def draw_card(self, draw_pile):
        """Draw a card from the draw pile.
        
        Args:
            draw_pile (list): List of cards representing the draw pile.
            
        Returns:
            bool: True if card was drawn successfully, 
                False if draw pile is empty.
            
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

""" Edit by Michael 12.06.2025 """

class HumanPlayer(Player):
    """Human player controlled by user input."""
    
    def __init__(self, name):
        """Initialize a human player.
        
        Args:
            name(str): The player's name
        
        Side effects:
            Calls parent class __init__ to set up player attributes.
        """
        super().__init__(name)
        
    def turn(self, state):
        """
        Execute a human player's turn with user input.
        
        Args:
            state (dict): Current game state containing piles and draw pile.
            
        Returns:
            str or tuple: Action taken ('draw', 'sort', 'end') or result tuple 
                ('played_card', card) or ('moved_pile', destination).
        """
        print(f"\n=== {self.name}'s Turn ===")
        print(f"\nYour hand: {self.hand}")
        #print(f"Current board state: {state}")
        
        while True:
            print("\nAvailable actions:")
            print("1. Play a card")
            print("2. Move a pile")
            print("3. Draw a card")
            print("4. Sort hand")
            print("5. End turn")
            
            try:
                choice = int(input("Choose an action (1-5): "))
                if 1 <= choice <= 5:
                    break
                else:
                    print("Please enter a number between 1 and 5.")
            except ValueError:
                print("Please enter a valid number")
                
        if choice == 1:
            return self.play_card(state)
        elif choice == 2:
            return self.move_pile(state)
        elif choice == 3:
            return "draw"
        elif choice == 4:
            self.sort_hand()
            return "sort"
        else:
            return "end"
    
    def play_card(self, state):
        """
        Play a card from hand to a pile.
        
        Args:
            state (dict): Current game state containing piles and draw pile.
            
        Returns:
            str or tuple: 'invalid', 'no_play', or ('played_card', 
                card_to_play).
            
        Side effects:
            Prompts user for card index and destination.
            Prints results to Terminal.
        """
        if not self.hand:
            print("No cards in hand to play!")
            return "no_play"
        print("Your hand:", self.hand)
        print("Available piles:", list(state.get('piles', {}).keys()))
        try:
            card_index = int(input("Enter index of card to play (0-based): "))
            if 0 <= card_index < len(self.hand):
                card_to_play = self.hand[card_index]
            else:
                print("Invalid card index!")
                return "invalid"
            
            move_to = input("Enter destination pile " +
                            "(e.g., 'N', 'NE'): ").upper()
            
            result = valid_moves(
                self.hand,
                card_to_play,
                state.get('piles', {}),
                move_to = move_to
            )
            
            if "Invalid" in result:
                print(result)
                return "invalid"
            else:
                print(result)
                return ("played_card", card_to_play)
        except (ValueError, IndexError):
            print("Invalid input!")
            return "invalid"
        
    def move_pile( self, state):
        """
        Move a pile from one location to another.
        
        Args:
            state (dict): Current game state containing piles and draw pile.
            
        Returns:
            str or tuple: 'invalid' or ('moved_pile', move_to).
            
        Side effects:
            Prompts user for source and destination piles.
            Prints results to terminal.
        """
        piles = state.get('piles', {})
        print("Available piles:", list(piles.keys()))
        try:
            move_from = input("Enter source pile to move from: ").upper()
            move_to = input("Enter destination pile to move to: ").upper()
            
            result = valid_moves(
                self.hand,
                None,  # No card from hand
                piles,
                move_from=move_from,
                move_to=move_to
            )
            
            if "Invalid" in result:
                print(result)
                return "invalid"
            else:
                print(result)
                return ("moved_pile", move_to)
                
        except (ValueError, KeyError):
            print("Invalid input!")
            return "invalid"
    
    """ Edit by Attowla """ 
    
    def sort_hand(self):
        #Made by Attowla
        """
        Sort the player's hand by rank, Ace to King
        
        Args: None
        
        Side Effects: Sorts the hand of the player (self.hand)
        """
        
       # Add an order to assist with sorting 
        rank_order = {
    "A": 1,
    "2": 2, "3": 3, "4": 4, "5": 5,
    "6": 6, "7": 7, "8": 8, "9": 9,
    "10": 10,
    "J": 11, "Q": 12, "K": 13
    }
        self.hand.sort(key=lambda card: rank_order[(card[0])])
        
""" Edited By Michael 12.06.2025 """

class ComputerPlayer(Player):
    """Computer-controlled player with predefined strategy."""
    def __init__(self, name):
        """
        Initialize a computer player.
        
        Args:
            name (str): The computer player's name.
        """
        super().__init__(name)
        
    def turn(self, state):
        """
        Execute a computer player's turn with strategic decision-making.
        
        Strategy order:
        1. Play a King to an empty corner pile
        2. Play any card to side piles
        3. Move a pile from one side to another
        4. Draw a card if possible
        5. End turn
        
        Args:
            state (dict): Current game state containing piles and draw pile.
            
        Returns:
            str: Action taken ('draw', 'end', 'played_card', 'moved_pile').
            
        Side effects:
            Prints computer's actions and decisions to terminal.
        """
        print(f"\n=== {self.name}'s Turn (Computer) ===")
        piles = state.get('piles', {})
        draw_pile = state.get('draw_pile', [])
        # Strategy 1: Try to play a King to an empty corner pile
        for card in self.hand:
            if card[0] == 'K':
                corner_piles = ['NW', 'NE', 'SW', 'SE']
                for corner in corner_piles:
                    if not piles.get(corner, []):
                        print(f"{self.name} tries to play {card} to {corner}")
                        result = valid_moves(self.hand, card, piles, 
                                             move_to = corner)
                        if "Invalid" not in result:
                            print(result)
                            return "played_card"
         # Strategy 2: Try to play any card to side piles
        for card in self.hand:
            side_piles = ['N', 'S', 'E', 'W']
            for side in side_piles:
                result = valid_moves(self.hand, card, piles, move_to=side)
                if "Invalid" not in result:
                    print(result)
                    return "played_card"
        # Strategy 3: Try to move a pile
        for from_pile in ['N', 'S', 'E', 'W']:
            for to_pile in ['N', 'S', 'E', 'W']:
                if from_pile != to_pile and piles.get(from_pile):
                    result = valid_moves(
                        self.hand,
                        None,
                        piles,
                        move_from=from_pile,
                        move_to=to_pile
                    )
                    if "Invalid" not in result:
                        print(result)
                        return "moved_pile"
        # Strategy 4: Draw a card if possible
        if draw_pile:
            print(f"{self.name} chooses to draw a card.")
            return "draw"
        # Strategy 5: End turn
        print(f"{self.name} chooses to end turn.")
        return "end"

""" Edit by Michael 12.06.2025 """

def player_turn(player_hand, play_piles, draw_pile, player):
    """
    Process a complete turn for a player in King's Corner.
    
    Args:
        player_hand: List of cards in player's hand
        play_piles: Dictionary of play piles {'N', 'S', 'E', 'W', 'NW', 'NE', 
            'SW', 'SE'}
        draw_pile: List representing the draw pile
        player: Player object taking the turn (HumanPlayer or ComputerPlayer)
    
    Returns:
        tuple: (player_hand, play_piles, draw_pile, turn_completed)
    
    Side effects:
        - May print prompts and messages to console
        - Modifies player_hand, play_piles, and draw_pile
    """
    turn_completed = False
    state = {
        'piles': play_piles,
        'draw_pile': draw_pile
    }
    action = player.turn(state)
    if action == "draw":
        if draw_pile:
            player_hand.append(draw_pile.pop())
            print(f"{player.name} draws a card.")
            turn_completed = True
        else:
            print("Draw pile is empty!")
    elif action == "sort":
        print(f"{player.name} sorts their hand.")
        player_turn(player_hand, play_piles, draw_pile, player)
        turn_completed = True
    elif action == "end":
        print(f"{player.name} ends turn.")
        turn_completed = True
    elif isinstance(action, tuple) and action[0] == "played_card":
        turn_completed = True
    elif isinstance(action, tuple) and action[0] == "moved_pile":
        turn_completed = True
    elif action in ["invalid", "no_play"]:
        if draw_pile:
            player_hand.append(draw_pile.pop())
            print(f"{player.name} draws a card.")
            turn_completed = True
        else:
            print("No valid moves and draw pile is empty.")
            turn_completed = True
    if not turn_completed and draw_pile:
        player_hand.append(draw_pile.pop())
        print(f"{player.name} draws a card (no other moves available).")
        turn_completed = True
    
    return player_hand, play_piles, draw_pile, turn_completed

"""Edit by Phakjira"""

def valid_moves(hand, card_to_play, piles, move_from = None, move_to = None):
    """Check whether the player's move is valid according to King's Corner 
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
        move_to (str): name of the pile the player wants to move 
            a card or a stack to. Defaults to None.
            
    Returns:
        str : a message indicating whether the move is valid or invalid.
        
    Side effects:
        Print updates to the console.
        Modifies the 'hand' list when a card is successfully play.
        Modifies the 'piles' dictionary when a card or stack is moved.
    """
    # Rank order from high to low
    rank_order = ['K', 'Q', 'J', '10', '9', '8', '7', '6', 
                  '5', '4', '3', '2', 'A']
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
            # Handle empty pile
            if not piles[move_to]:
                if card_to_play[0] != 'K':
                    return ('Invalid Move! Only Kings can start the '+
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
                # Just move the card to the empty corner pile if it's a K
                if stack[0][0] == 'K':
                    piles[move_to] += stack
                    piles[move_from] = []
                    print (f'{move_to} changed : {piles[move_to]}')
                    print (f'{move_from} changed : {piles[move_from]}')
                    return f'Moved stack pile from {move_from} onto {move_to}'
                else:
                    return('Invalid Move! Only Kings can be placed in empty '+
                            'corner piles.')
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
'''hand = [
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
print(valid_moves(hand, None, piles, move_from = 'E', move_to = 'T'))'''


""" Edit by Phakjira (Dec.6, 2025) """

class Deck:
    """ A deck of 52 cards used in the Kings Corner game.
    
    Cards are represented as (rank, color) tuples. Each rank appears four times: 
    twice in Red and twice in Black. 
   
    Attributes:
        cards (list of tuple): the current ordered list of cards in the deck. 
            Each card is a (rank, color) tuple such as ('Q', 'Red').
    """
    
    RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    COLORS = ["Red", "Black"]  

    def __init__(self):
        """Initialize a shuffled deck.
        
        Side effects:
            Creates and populates the attribute 'cards'.
        """
        # Create 4 cards per rank: 2 Red + 2 Black
        self.cards = []
        for rank in self.RANKS:
            for color in self.COLORS:
                # Duplicate to simulate 52 cards
                self.cards.append((rank, color))
                self.cards.append((rank, color))  

        random.shuffle(self.cards)

    def deal(self):
        """Deal 7 cards from top of deck to the player. 
        
        Returns: 
            list of tuples: the list of those 7 cards.
        
        Side effects:
            Removes 7 cards from the beginning of 'self.cards'.
        """
        hand = self.cards[:7]
        self.cards = self.cards[7:]
        return hand
    
    def draw_one(self):
        """Draw 1 card from the deck. 
        
        Returns:
            tuple: the top card of the deck. Ex. ('K', 'Black').
            
        Side effects:
            Removes 1 card from the beginning of 'self.cards'.
        """
        return self.cards.pop(0)
    
    def turn_up_four(self):
        """Draw 4 cards from the deck and place them in a cross (N, S, E, W).
        
            - Note: These are the foundation piles.
        
        Returns:
            foundation (dict): a dictionary with keys 'N', 'S', 'E', 'W' and 
                their drawn cards.
            
        Side effects:
            Removes 4 cards from the beginning of 'self.cards'.
        """
        foundations = {
        "N": self.draw_one(),  # Returns card directly, not in list
        "S": self.draw_one(),
        "E": self.draw_one(),
        "W": self.draw_one(),
        }
        return foundations
    

    def __len__(self):
        """Return the number of cards currently in the deck."""
        return len(self.cards)
    
    def __str__(self):
        """Return an informal string of cards (Human-readable formate)."""
        return str(self.cards)
# Testing
'''deck = Deck()
print('\nList of 52 cards:\n')
print(deck.cards)
print(f"\nList of 7 cards:\n\n {deck.deal()}")
print(f"\nFoundation cards:\n\n {deck.turn_up_four()}")
print(f"\nCards left in deck: {len(deck)}\n")'''


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
    if p1_score < p2_score:
        print(f"Player 1 wins! Score:{p1_score}")
    elif p2_score < p1_score:
        print(f"Player 2 wins! Score:{p2_score}")
    else:
        print(f"It's a tie! Both players have score: {p1_score}")
        return None

'''p1 = [(13, "r"), (10, "b"), (8, "r")]
p2 = [(9, "b"), (12, "b"), (3, "r")]

p1_score = end_round(p1)
p2_score = end_round(p2)'''

#print(f"p1 score:{p1_score}")
#print(f"p2 score:{p2_score}")

#win_condition(p1_score, p2_score) #no winner since only one round was played

"""Edit by Attowla"""

def build_board(piles):
    # Attowla
    """
    Build a 3x3 board layout of King's Corner.

    Args:
        piles (dict): Dictionary of all piles (side + corner).

    Returns:
        list: 3x3 list of strings representing the board.
    """
    
    def top_card(pile_name):
        """
        Return the top card of a pile or a dot if the pile is empty.

        Args:
            pile_name (str): Name of the specific pile.

        Returns:
            str: Formatted top card string (e.g., 'KR' )or bullet symbol.
            
        Side effects:
            top_card has the possibility to be altered at every turn.
        """
        pile = piles.get(pile_name, [])
        # Example: 'KR' = King Red  else  Bullet for empty pile
        return f"{pile[-1][0]}{pile[-1][1][0]}" if pile else "\u2022"

    board = [
        [top_card('NW'), top_card('N'), top_card('NE')],
        [top_card('W'), "\u2022", top_card('E')],
        [top_card('SW'), top_card('S'), top_card('SE')]
    ]
    return board

""" Edit by Phakjira """

# main()
def main():
    """ Run a full game of King's Corner.
    
    Sets up the deck, players, and board, then handles turn-by-turn
    gameplay until a winner is determined.
    """
    game = KingsGame()
    game.play_game()

if __name__ == "__main__":
    main()