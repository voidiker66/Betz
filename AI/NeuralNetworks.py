import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


class Cuore(torch.nn.Module):
    
    def __init__(self):
        super(Cuore, self).__init__()

        
        self.IL = nn.Linear(325,250)
        self.HL1 = nn.Linear(250,150)
        self.HL2 = nn.Linear (150,100)
        self.OL = nn.Linear(100,52)
#         self.Mem = nn.RNN(input_size, 
#                           hidden_size, 
#                           num_layers, 
#                           nonlinearity=activation_function, 
#                           dropout=dropout, 
#                           bidirectional=bidirectional)
        
    def forward(self,game_state,memory):
        

        
        x = F.relu(self.IL(game_state))
        x = F.relu(self.HL1(x))
        x = F.relu(self.HL2(x))
        x = F.relu(self.OL(x)) + 0.0001*torch.ones((1,52))
               
        return x


class Gioco(torch.nn.Module):
    
    def __init__(self):
        super(Gioco, self).__init__()

        
        self.IL = nn.Linear(325,250)
        self.HL1 = nn.Linear(250,150)
        self.HL2 = nn.Linear (150,100)
        self.OL = nn.Linear(100,52)
#         self.Mem = nn.RNN(input_size, 
#                           hidden_size, 
#                           num_layers, 
#                           nonlinearity=activation_function, 
#                           dropout=dropout, 
#                           bidirectional=bidirectional)
        
    def forward(self,game_state,memory):
        

        x = F.relu(self.IL(game_state))
        x = F.relu(self.HL1(x))
        x = F.relu(self.HL2(x))
        x = torch.sigmoid(self.OL(x))
               
        return x