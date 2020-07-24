import os
from os import path
from collections import deque
import random
from random import shuffle

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from CustomDatasets import GameMemoryDataset,PlayerMemoryDataset

from CardGames import Hearts

CURRENT_DIR = path.abspath(path.curdir)
NAME_WHEEL = ['Lain','Turing','Tesla','Silver']
BATCH_SIZE = 1024
MINIBATCH_SIZE = 64
DECAY = 0.9999

game_counter = 0




game = Hearts(train=True)

game_model_directory = os.listdir(CURRENT_DIR + f'/Models/Gamma/')

if len(game_model_directory)==0:

        game.version = 1
        torch.save(game.strat_nnet.state_dict(),CURRENT_DIR + f'/Models/Gamma/GNet {game.version}')

else:
    game.version = np.max(np.array([int(model.split(' ')[1]) for model in game_model_directory]))
    game.strat_nnet.load_state_dict(torch.load(CURRENT_DIR + f'/Models/Gamma/GNet {game.version}'))



game.optimizer = torch.optim.Adam(game.strat_nnet.parameters(),lr=0.0001)

for i,player in enumerate(game.playerlist):
    
    player.name = NAME_WHEEL[i]
    player.optimizer = torch.optim.Adam(player.response_nnet.parameters(),lr=0.0001)
    
    player_model_directory = os.listdir(CURRENT_DIR + f'/Models/{player.name}/Versions/')

    if len(player_model_directory)==0:

        player.version = 1
        torch.save(player.response_nnet.state_dict(),CURRENT_DIR + f'/Models/{player.name}/Versions/QNet {player.version}')

    else:
        player.version = np.max(np.array([int(model.split(' ')[1]) for model in player_model_directory]))
        player.response_nnet.load_state_dict(torch.load(CURRENT_DIR + f'/Models/{player.name}/Versions/QNet {player.version}'))

    if "QNet Prime" in os.listdir(CURRENT_DIR + f'/Models/{player.name}/'):
        
        player.best_response_nnet.load_state_dict(torch.load(CURRENT_DIR + f'/Models/{player.name}/QNet Prime'))

    else:

        torch.save(player.response_nnet.state_dict(),CURRENT_DIR + f'/Models/{player.name}/QNet Prime')



for i in range(10):

    while not game.round_over:

        game.play_round()

    
    game_counter += 1
    game.reset()
    shuffle(game.playerlist)
    game.EPSILON = max(game.EPSILON*DECAY,0.05)

    if len(game.memory)>game.MIN_MEM_LEN and game_counter%1000==0:


        batch = random.sample(list(game.memory),BATCH_SIZE)
        dataset = GameMemoryDataset(batch)
        dataloader = DataLoader(
                        dataset, 
                        batch_size=MINIBATCH_SIZE,
                        shuffle=True
                        )
    
        for game_state,memory,action in dataloader:

            prediction = game.strat_nnet(game_state,memory)
            
            loss = nn.MSELoss()

            game.optimizer.zero_grad()

            output = loss(prediction.squeeze(),action.squeeze())
            output.backward()       
            game.optimizer.step()  

        game.version += 1

        
        torch.save(game.strat_nnet.state_dict(),CURRENT_DIR + f'/Models/Gamma/GNet {game.version}')

        for player in game.playerlist:
        
            batch = random.sample(player.memory,BATCH_SIZE)
            dataset = PlayerMemoryDataset(batch)
            dataloader = DataLoader(
                            dataset, 
                            batch_size=MINIBATCH_SIZE,
                            shuffle=True
                            )
            
            for game_state, memory, action, reward, maxq in dataloader:

                prediction = player.response_nnet(game_state,memory)

                player.optimizer.zero_grad()


                loss = torch.mean((reward + maxq - torch.sum(prediction*action))**2)
                loss.backward()

                player.optimizer.step()

            player.version += 1

            torch.save(player.response_nnet.state_dict(),CURRENT_DIR + f'/Models/{player.name}/Versions/QNet {player.version}')
            torch.save(player.response_nnet.state_dict(),CURRENT_DIR + f'/Models/{player.name}/QNet Prime')  
            player.best_response_nnet.load_state_dict(torch.load(CURRENT_DIR + f'/Models/{player.name}/QNet Prime'))          




            




