# INST326_2025_FALL_KINGS_CORNER
                        Final Project

## Purpose of Each File
* ### `demo_game.py` and `demo_human.py`

    These are demo files used to illustrate how the game would look and behave during the presentation. They allow us to simulate gameplay and demonstrate player actions, but they are **`not required to run the final program`**. At the time of the presentation, the main game code was not fully complete, so these files helped showcase the gameplay flow.

* ### `kings_corner.py`

    This is the actual implementation of the King’s Corner game. It contains all the necessary classes, functions, and methods to run the game fully, including deck setup, game modes, player turns, move validation, hand management, board display, scoring, and win condition. This is the file used to run the program in its complete form.

## How to Run the Program:
`python3 kings_corner.py`

## How to Use the Program / Interpret Output
* The program will prompt you to select a mode:
    * **P1** : Play against another human player.
    * **CPU** : Play against the computer.
* The program will then prompt you to enter your name.
* Follow the on-screen prompts to play the game:
    * You will be asked to choose an action (1-5):

        1. **Play a card** 
            - Select a card from your hand by its index (0-based). 
            - Then choose which pile to place it on using the pile names (`N`, `S`, `E`, `W`, `NW`, `NE`, `SW`, `SE`).
        2. **Move a pile**  
            - Choose a source pile and a destination pile by name.  
            - The program will attempt to move the stack according to the game rules.
        3. **Draw a card**  
            - The program will draw a card for you automatically.
            **NOTE**: A card will also be drawn automatically if you attempt an invalid move.
        4. **Sort hand**
            - The program will sort the cards in player's hand in ascending order based on rank.
        5. **End turn**  
            - The turn passes to the next player (the computer, in this case).

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
|  KingsGame._\_init__ |   Phakjira Sukprasert | Composition of two custom classes |
| valid_moves   | Phakjira Sukprasert | Optional parameters / keyword arguments |
|HumanPlayer._\_init__()| Michael Huang | super() |
|Player._\_str__ | Michael Huang | Magic methods other than ._\_init__ |
|HumanPlayer.sort_hand| Attowla Kouadio | Use of a key function with list.sort() |
|top_card (nested in build_board) | Attowla Kouadio | Conditional expression |
| end_round | Charles Bukoski | Sequence unpacking |
| win_condition | Charles Bukoski |f-strings containing expressions |