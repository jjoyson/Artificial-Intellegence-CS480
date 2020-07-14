HOW TO RUN:
Requires Python 3
Run the command line game with: "python3 playInteractive.py"

You can run a tournament with: "python3 playTourney.py"

The game will then prompt you to make Players (and name them) before
you can start playing.  The user may select for human vs human, human
vs computer, and even computer vs computer.


EXPLANATION OF OUR IMPLEMENTATION:

Main Module

connect5.py contains main function and object definitions, player.py
contains the Player object, and aiplayer.py contains the AIPlayer
object which is a rudimentary computer player.

Within connect5.py, the object that is defined is Game, player.py
defines Player, and aiplayer.py defines AIPlayer.

When playInteractive.py is executed, an instance of Game is
initialized. When the game is initialized, the program asks the user
to select a human or computer player for Player 1 (who will be
represented in the game with "x") and Player 2 (represented with "o").
For each human player, an instance of Player is initialized and for
each computer player, an instance of AIPlayer is initialized.
AIPlayer is a subclass of Player.  When an AIPlayer is initialized, a
difficulty value is set represents the level to which the minimax
algorithm searches.

After a game is played, the program prompts the user to play again.
The program tracks wins/losses/ties over multiple rounds and displays
these statistics after each game.

When a Five-in-a-row is made, the characters representing the pieces
in that streak are capitalized.  This makes it clear why the game
ended.

minimax.py is a module which contains an implementation of the minimax
algorithm for Connect 5.  This module also has methods for creating
state objects (states of the board) as well as functions for checking
characteristic of a given state.  An example characteristic is the
number of streaks of length k.  There is a method which counts this
number, and which takes a search length parameter.
