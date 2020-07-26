import numpy as np


class Player():
    
    def __init__(self,deckshape,human=False):
        
        
        """
            Very basic player information, automatically assumes Player is AI unless specified
        """
        
        self.wins = 0
        self.cards = 0
        self.points = 0
        self.round_points = 0
        self.human = human
        self.model = 'Heuristic'

        
        self.deckshape = deckshape
        self.hand = np.zeros(self.deckshape)
        self.reserve = np.zeros(self.deckshape)

        
        """
            Reset handles the bare basics of ending a round and setting it up for the next one.
            It doesn't deal out new cards but it clears away all cards from the hand or reserve.
            It does not clear up stat tracking information like total points or how many queen of spades they've received
        """
        
    def reset(self):
        
        self.cards = 0
        self.round_points = 0

        
        self.hand = np.zeros(self.deckshape)
        self.reserve = np.zeros(self.deckshape)