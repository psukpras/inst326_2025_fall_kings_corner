# INST326_2025_FALL_KINGS_CORNER
                        Final Project

## Purpose of Each File
`demo_game.py` and `demo_human.py` are demo files that will be use on the presentation day.

`kings_corner.py` is the actual file for the final. 

## How to Run the Program:
`python3 kings_corner.py`

## How to Use the Program / Interpret Output
* The program will prompt you to enter your name.
* Follow the on-screen prompts to play the game:
    * You will be asked to choose an action (1-4):
        1. **Play a card**  
           - You will select a card from your hand by its index (0-based).  
           - Then choose which pile to place it on using the pile names (`N`, `S`, `E`, `W`, `NW`, `NE`, `SW`, `SE`).
        2. **Move a pile**  
           - You will choose a source pile and a destination pile by name.  
           - The program will attempt to move the stack according to game rules.
        3. **Draw a card**  
           - The program will draw a card for you automatically.
        4. **End turn**  
           - The turn passes to the next player (the computer in this case).
    * Computer player actions are automated and displayed for reference.
* The game ends when:
    1. A player empties their hand — that player wins.
    2. The draw pile is empty — the player with fewer cards in hand wins.
* Each turn displays:
    - Current cards in each pile
    - The current player’s hand
    - Number of cards left in the deck
* The board layout shows side piles (`N`, `S`, `E`, `W`) and corner piles (`NW`, `NE`, `SW`, `SE`) with the top card displayed. Empty piles are represented by a bullet (•).

## Annotated Bibliography

| Source | How It Was Used | URL |
|--------|----------------|-----|
| Bicycle Cards – "How to Play King's Corner" | Used to implement the standard rules for setup, dealing, foundations, and gameplay. | [Bicycle Cards – Kings Corner](https://bicyclecards.com/how-to-play/kings-corner) |

## Attribution

|   Method/function |   Primary author  |   Techniques demonstrated |
|----------------------|----------------|------------------------|
|  KingsGame._\_init__ |   Phakjira Sukprasert | Composition of two custom classes, Optional parameters / keyword arguments |
| valid_moves   | Phakjira Sukprasert | Sequence unpacking   |
| Deck._\_len__| Phakjira Sukprasert  | Magic methods other than _\_init__   |
|Player._\_init__|
|HumanPlayer.__init__()| Michael Huang | super() |
|HumanPlayer.play_card() | Michael Huang | keyword arguments |