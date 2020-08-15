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










class Cuore2(nn.Module):
    def __init__(self):
        super(Cuore2, self).__init__()
        
        
        self.Conv1 = nn.Conv2d(6,16,3)
        self.Conv2 = nn.Conv2d(16,32,3)
        self.Conv3 = nn.Conv2d(32,64,2)

        self.bnorm1 = nn.BatchNorm2d(16)
        self.bnorm2 = nn.BatchNorm2d(32)
        self.bnorm3 = nn.BatchNorm1d(1000)
        self.bnorm4 = nn.BatchNorm1d(500)
        self.bnorm5 = nn.BatchNorm1d(100)
     
        self.pool = nn.MaxPool2d(2,2)#,return_indices=True)

        self.fc1 = nn.Linear(1600, 1000)
        self.fc2 = nn.Linear(1000,500)
        self.fc3 = nn.Linear(500,100)
        self.fc4 = nn.Linear(100,52)
     
        

    def forward(self, game_state, memory):
        
        x = self.Conv1(game_state)
        x = F.relu(self.bnorm1(x))
        x = self.Conv2(x)
        x = F.relu(self.bnorm2(x))
        x = self.pool(x)
        x = self.Conv3(x)

        x = x.view(-1,1,1600)

        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        x = F.relu(x)
        x = self.fc3(x)
        x = F.relu(x)
        x = self.fc4(x)

        
        return x 



class Gioco2(nn.Module):
    def __init__(self):
        super(Gioco2, self).__init__()
               
        self.Conv1 = nn.Conv2d(6,16,3)
        self.Conv2 = nn.Conv2d(16,32,3)
        self.Conv3 = nn.Conv2d(32,64,2)

        self.bnorm1 = nn.BatchNorm2d(16)
        self.bnorm2 = nn.BatchNorm2d(32)
     
        self.pool = nn.MaxPool2d(2,2)#,return_indices=True)

        self.fc1 = nn.Linear(1600, 1000)
        self.fc2 = nn.Linear(1000,500)
        self.fc3 = nn.Linear(500,100)
        self.fc4 = nn.Linear(100,52)

        
        # self.ConvTrans3 = nn.ConvTranspose2d(64,32,2)
        # self.ConvTrans2 = nn.ConvTranspose2d(32,16,3)
        # self.ConvTrans1 = nn.ConvTranspose2d(16,1,3)
        
        # self.unpool = nn.MaxUnpool2d(2,2)

        
        

    def forward(self, game_state, memory):
        
        x = self.Conv1(game_state)
        x = F.relu(self.bnorm1(x))
        x = self.Conv2(x)
        x = F.relu(self.bnorm2(x))
        x = self.pool(x)
        x = self.Conv3(x)

        x = x.view(-1,1,1600)

        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        x = F.relu(x)
        x = self.fc3(x)
        x = F.relu(x)
        x = self.fc4(x)

        # x = self.ConvTrans3(x)
        # x = self.unpool(x,indices)
        # x = F.relu(nn.BatchNorm2d(x))
        # x = self.ConvTrans2(x)
        # x = F.relu(nn.BatchNorm2d(x))
        # x = self.ConvTrans1(x)
        # print(x)
        
        return torch.sigmoid(x)