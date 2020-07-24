from collections import deque

import numpy as np
import torch

from Player import Player
from NeuralNetworks import Cuore, Gioco



       
        

class CardGame():
    
    def __init__(self,deckshape,handsize,numplayers,dealer=None):
        
        """
			The best way to handle a generic deck of cards is to allow for the representation of
            the deck to be a numpy array.  It's a bitboard where each value in the array stands for
            a single card.  This is normally 13x4 for a normal deck, but can a be used to describe
            other decks, such as UNO or pinochle.  It's very easy to turn a numpy array into a one
            dimensional tensor for use by the neural network as well as calculate points and available
            moves.
            
            The game state is a composition of what I'm going to refer to as "piles".  Piles represent
            different locations that the cards can be.  In theory, ΣP = np.ones(deckshape) where P is
            a pile.  This makes it very easy to build inputs into the neural network as we can exclude
            or include piles depending on the person.  They way each pile is used can be specified by
            the game itself.
		"""
        
        
        self.game_over = False
        self.round_over = False
        
        self.deckshape = deckshape
        self.handsize = handsize
        self.numplayers = numplayers
        
        self.deck = np.ones(self.deckshape)
        self.discard = np.zeros(self.deckshape)
        self.table = np.zeros(self.deckshape)

        self.playerlist = [Player(self.deckshape) for _ in range(self.numplayers)]
        self.dealer = np.random.randint(0,4) if dealer is None else dealer
        self.turn = 0
        self.suit = None
        self.winning_round = None
        self.history = []
        

        
                

 
    def reset(self):
        
        self.deck = np.ones(self.deckshape)
        self.discard = np.zeros(self.deckshape)
        self.suit = None
        self.round_over = False
        self.history = []

        for player in self.playerlist:

            player.reset()        
   
        self.game_specific_reset()
    
    
    def shuffle(self):
        
        self.deck += self.discard
        self.discard = np.zeros(self.deckshape)
    
            
            
    def deal(self,dealing_player):
        
        for i in range(self.handsize * self.numplayers):
            
            a,b = self.random_card(self.deck)
            
            self.playerlist[(i+dealing_player)%self.numplayers].hand[a,b] = 1
            self.deck[a,b] = 0
            
            self.playerlist[(i+dealing_player)%self.numplayers].cards += 1
    

    def game_specific_reset():
        
        pass
            
            
    def random_card(self,pile):
        
        available_cards = np.nonzero(pile)
        pulled_card = np.random.randint(0,len(available_cards[0]))
        
        return available_cards[0][pulled_card], available_cards[1][pulled_card]
    
 
    def get_pile(self,pile):
    
        available_cards = np.nonzero(pile)
        
        return np.array((available_cards[0],available_cards[1]))


class Hearts(CardGame):
    
    def __init__(self,train=False):
        super().__init__((4,13),13,4)
        
        self.train = train
        self.hearts_broken = False
        self.first_round = True
        self.shoot_the_moon = None
        self.MAX_MEM_LEN = 100000
        self.MIN_MEM_LEN = 10000
        self.EPSILON = 0.9
        
        self.memory = deque([], maxlen=self.MAX_MEM_LEN)
        
        self.strat_nnet = Gioco()
        
        for player in self.playerlist:
            
            player.hearts = 0
            player.queen_of_spades = 0
            
            player.response_nnet = Cuore()
            player.best_response_nnet = Cuore()
            
            player.memory = deque([], maxlen=self.MAX_MEM_LEN)
            player.train_examples = []

            
        
        
    def game_specific_reset(self):
        
        self.hearts_broken = False
        self.first_round = True
        self.shoot_the_moon = None

        if self.train:

            for player in self.playerlist:

                player.points = 0
        
        
    def check_for_2clubs(self):
        
        for i,player in enumerate(self.playerlist):
            
            if player.hand[3,0]==1:
                
                return i
            
        
        return None
    
    
    def choose_card(self,player): #fix this for hearts broken logic
        
        
        if player.human:
            
            pass
        
        else:
            
            if self.suit==None:

                return self.random_card(player.hand)

            else:

                if np.sum(player.hand[self.suit])==0:

                    return self.random_card(player.hand)

                else:

                    available_moves = player.hand.copy()
                    available_moves[:self.suit] = 0
                    available_moves[self.suit+1:] = 0

                    return self.random_card(available_moves)
   
    
    
    def play_round(self):
        
       
        previous_b = -1
        self.winning_round = None
        
        
        if self.first_round:
            
            self.deal(self.dealer)
            self.dealer = (self.dealer + 1)%self.numplayers
            
            self.turn = self.check_for_2clubs()
            
            self.record_history(3,0)

            self.playerlist[self.turn].hand[3,0] = 0
            self.table[3,0] = 1
            
            self.first_round = False
            self.suit = 3
            previous_b = 0
            self.winning_round = self.turn
            
            self.turn = (self.turn + 1)%self.numplayers
            
        while np.sum(self.table)<self.numplayers:
            
            if self.train==False:
                
                a,b = self.choose_card(self.playerlist[self.turn])
                
            else:
                
                game_state, mask, memory = self.nnet_input()
                
                with torch.no_grad():
                    output = self.playerlist[self.turn].response_nnet(game_state,memory)*mask
                

                prediction = output / torch.sum(output)
                prediction = prediction.squeeze().numpy()
                
               


                
                if np.random.uniform(0,1)<self.EPSILON:
                    


                    choice = np.random.choice(52,p=prediction)
                    a,b = int(choice/13), choice%13


                    
                    
                    
                
                else:


                    
                    choice = np.argmax(prediction)
                    a,b = int(choice/13), choice%13

                    action = torch.zeros((1,52))
                    action[0,choice] = 1
                    self.memory.append([game_state,memory,action])
                
                action = torch.zeros((1,52))
                action[0,choice] = 1
 

                if len(self.playerlist[self.turn].train_examples)>0:
                    
                    self.playerlist[self.turn].train_examples[-1][4] = torch.max(output)
                                



                if len(self.playerlist[self.turn].train_examples)<12:
                
                    self.playerlist[self.turn].train_examples.append([
                                    game_state
                                    ,memory
                                    ,action
                                    ,None # reward
                                    ,None # max q'
                                    ])     
                

            
#             self.record_history(a,b)
            
                      
            if self.suit==None:
                
                self.suit = a
                

        
            self.playerlist[self.turn].hand[a,b] = 0
            self.table[a,b] = 1
            
            
            if self.hearts_broken==False:
                
                
                if np.sum(self.table[2])>0:
                    
                    self.hearts_broken = True
            
            if a==self.suit:
                
                if b>previous_b:
                    
                    previous_b = b
                    self.winning_round = self.turn
                    

                    
                    
            
            self.turn = (self.turn + 1)%self.numplayers
            
        self.playerlist[self.winning_round].reserve += self.table
        self.table = np.zeros(self.deckshape)
        self.turn = self.winning_round
        self.winning_round = None  
        self.suit = None
        
        if np.sum(self.playerlist[0].hand)==0:
            
            self.score_round()
            
            
            self.round_over = True
            
            
            
    def score_round(self):
        

        for i,player in enumerate(self.playerlist):
            
            player.hearts += np.sum(player.reserve[2])
            player.queen_of_spades += player.reserve[1,10]
            player.round_points = np.sum(player.reserve[2]) + 13*player.reserve[1,10]
            
            if player.round_points==26:
                
                self.shoot_the_moon = i
                
        if self.shoot_the_moon!=None:
            
            for i,player in enumerate(self.playerlist):
                
                if i==self.shoot_the_moon:
                    
                    pass
                
                else:
                    
                    player.points += 26
                    
        else:
            
            for player in self.playerlist:
                
                player.points += player.round_points
                
        if self.train:      
            
            for player in self.playerlist:
                    
                for x in player.train_examples:

                    player.memory.append([x[0],x[1],x[2],torch.tensor((26-player.round_points)/13),x[4]])
                
                
    def record_history(self,a,b):
        
        game_state = [player.reserve.copy() for player in self.playerlist]
        game_state.append(self.table.copy())
        
        card_played = np.zeros((4,13))
        card_played[a,b] = 1
        
        game_state.append(card_played)
        
        self.history.append((np.concatenate(game_state),self.turn))
                
                
    def get_mask(self):
        
        mask = self.playerlist[self.turn].hand.copy()
        
        if self.suit==None:
            
            if self.hearts_broken or np.sum(self.playerlist[self.turn].hand[2])==np.sum(self.playerlist[self.turn].hand):
                
                return torch.reshape(torch.tensor(mask),(1,-1))
            
            else:
                
                mask[2] = 0
                
                return torch.reshape(torch.tensor(mask),(1,-1))
        
        
        elif np.sum(self.playerlist[self.turn].hand[self.suit])==0:
            
            return torch.reshape(torch.tensor(mask),(1,-1))
                  
        else:
            
            mask[:self.suit] = 0
            mask[self.suit+1:] = 0
            
            return torch.reshape(torch.tensor(mask),(1,-1))
        
    
    def recall_history(self):
        
        return np.zeros((1,13))
        
        

                

    def nnet_input(self):
    
        game_state = [self.playerlist[(i+self.turn)%self.numplayers].reserve.copy() for i in range(self.numplayers)]
        game_state.append(self.playerlist[self.turn].hand.copy())
        game_state.append(self.table.copy())
        
        memory = self.recall_history()
        game_state.append(memory) #get rid of this once RNN is up and running
        game_state = torch.reshape(torch.tensor(np.concatenate(game_state)).float(),(1,-1))
        
        mask = self.get_mask()
        
        return game_state, mask, memory
