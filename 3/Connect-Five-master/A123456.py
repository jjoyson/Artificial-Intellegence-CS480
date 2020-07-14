# Example AI Player Subclass

from aiplayer import AIPlayer


class A123456(AIPlayer):
    """ Super Player
    """
    def __init__(self):
        AIPlayer.__init__(self, "A123456", "x", 4)
