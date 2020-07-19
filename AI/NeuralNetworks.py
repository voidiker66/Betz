import numpy as np
import torch


class Cuore(torch.nn.Module):
    
    def __init__(self):
        super(Cuore, self).__init__()

        
        self.IL = nn.Linear(325,250)
        self.HL1 = nn.Linear(250,150)
        self.HL2 = nn.Linear (150,100)
        self.OL = nn.Linear(100,52)
        
    def forward(self,game_state,mask,memory):
        

        
        x = self.IL(game_state)
        x = self.HL1(x)
        x = self.HL2(x)
        x = self.OL(x)
        
        x = torch.sigmoid(x)
        
        return mask*x