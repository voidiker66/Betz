import numpy as np
import pygame
import time
from CardGames import Hearts


pygame.init()

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

GREEN = (34,139,34)
WHITE = (255,255,255)
RED = (255,0,0)
BLACK = (0,0,0)


CARD_MAPPING = ['2'
				,'3'
				,'4'
				,'5'
				,'6'
				,'7'
				,'8'
				,'9'
				,'10'
				,'J'
				,'Q'
				,'K'
				,'J']

SUIT_MAPPING = ['D'
				,'S'
				,'H'
				,'C']

COLOR_MAPPING = [RED
				,BLACK
				,RED
				,BLACK]


screen = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
screen.fill(GREEN)


pygame.display.flip()

game = Hearts()
game.play_round()





class Card():

    def __init__(self,x,y,width,height,color,text,clickable=False):


    	self.x = x
    	self.y = y
    	self.width = width
    	self.height = height
    	self.text = text
    	self.color = color
    	self.font = pygame.font.SysFont('Comic Sans MS',8)
    	self.presscheck = [False,False]
    	self.clickable = clickable



    def draw_card(self,screen):


    	pygame.draw.rect(screen,self.color,(self.x,self.y,self.width,self.height))
    	pygame.draw.rect(screen,WHITE,((self.x+1,self.y+1,self.width-2,self.height-2)))
    	text = self.font.render(self.text,False,self.color)
    	screen.blit(text,(self.x+6,self.y+15))


    def get_coordinates(self):

        return self.x-5,self.x+self.width+5,self.y,self.y+self.height

    def got_pressed(self,click,mousex,mousey):


    	if self.clickable:

	        start_x1, start_x2, start_y1, start_y2 = self.get_coordinates()   

	        if (click==0 and start_x1<=mousex<=start_x2 and start_y1<=mousey<=start_y2) or self.presscheck[0]==True:

	            if (click==1 and start_x1<=mousex<=start_x2 and start_y1<=mousey<=start_y2) or self.presscheck[1]==True:

	                if (click==0 and start_x1<=mousex<=start_x2 and start_y1<=mousey<=start_y2):
	                    self.presscheck = [False,False]
	                    return True
	                elif (click==1 and start_x1<=mousex<=start_x2 and start_y1<=mousey<=start_y2):
	                    self.presscheck[1] = True
	                else:
	                    self.presscheck = [False,False]
	            elif click==0 and start_x1<=mousex<=start_x2 and start_y1<=mousey<=start_y2:
	                self.presscheck[0] = True
	            else:
	                self.presscheck[0] = False

	        return False

	    # return False






run = True
update_needed = True

while run==True:

	for event in pygame.event.get():

		if event.type==pygame.QUIT:

			run = False

		mousex, mousey = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()[0]

		if update_needed==True:
		
			card_buttons = []

			players_hand = game.get_pile(game.playerlist[0].hand)


			for i in range(len(players_hand[0])):

				card = Card(80+i*50,400,25,40,COLOR_MAPPING[players_hand[:,i][0]],CARD_MAPPING[players_hand[:,i][1]]+SUIT_MAPPING[players_hand[:,i][0]],True)

				card_buttons.append(card)


			table = np.zeros((4,13))

			for player in game.playerlist:
				table+=player.reserve

			table = game.get_pile(table)


			for i in range(len(table[0])):


				card = Card(290+i*50,200,25,40,COLOR_MAPPING[table[:,i][0]],CARD_MAPPING[table[:,i][1]]+SUIT_MAPPING[table[:,i][0]])

				card_buttons.append(card)

			for card in card_buttons:
				card.draw_card(screen)

			update_needed = False


		for i,card in enumerate(card_buttons):

			if card.got_pressed(click,mousex,mousey)==True:
				print(f'hell yeah {i+1}')








		pygame.display.flip()