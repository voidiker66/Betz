import os
from os import path
from collections import deque
import random
from random import shuffle
from datetime import datetime

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
DECAY = 0.99
DISCOUNT = 0.97
EPSILON = 0.08
MIN_EPSILON = 0.01

game_counter = 0
batch_counter = 0



game = Hearts(train=True)
game.EPSILON = EPSILON

game_model_directory = os.listdir(CURRENT_DIR + f'/Models/Gamma/')

if len(game_model_directory)==0:

        game.version = 1
        torch.save(game.strat_nnet.state_dict(),CURRENT_DIR + f'/Models/Gamma/GNet {game.version}')

else:
    game.version = np.max(np.array([int(model.split(' ')[1]) for model in game_model_directory]))
    game.strat_nnet.load_state_dict(torch.load(CURRENT_DIR + f'/Models/Gamma/GNet {game.version}'))



game.optimizer = torch.optim.SGD(game.strat_nnet.parameters(),lr=0.01,momentum=0)

for i,player in enumerate(game.playerlist):
    
    player.name = NAME_WHEEL[i]
    player.optimizer = torch.optim.SGD(player.response_nnet.parameters(),lr=0.1,momentum=0)
    
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



while batch_counter<1000:

    while not game.round_over:

        game.play_round()

    
    game_counter += 1
    game.reset()
    shuffle(game.playerlist)


    if len(game.playerlist[0].memory)>game.MIN_MEM_LEN and game_counter%1000==0:

        batch_counter += 1


        game.EPSILON = max(game.EPSILON*DECAY,MIN_EPSILON)


        if len(game.memory)>game.MIN_MEM_LEN:


            game_batch = random.sample(list(game.memory),BATCH_SIZE)
            game_dataset = GameMemoryDataset(game_batch)
            game_dataloader = DataLoader(
                            game_dataset, 
                            batch_size=MINIBATCH_SIZE,
                            shuffle=True
                            )
        
            for game_state,memory,mask,action in game_dataloader:

                game.optimizer.zero_grad()

                prediction = game.strat_nnet(game_state,memory)


                ideal_prediction = torch.where(mask==1,action,prediction)    


                output = torch.mean((ideal_prediction - prediction)**2)
                output.backward()       
                game.optimizer.step()  

            game.version += 1

        
            torch.save(game.strat_nnet.state_dict(),CURRENT_DIR + f'/Models/Gamma/GNet {game.version}')



        avg_loss = 0

        for player in game.playerlist:
        
            batch = random.sample(player.memory,BATCH_SIZE)


            dataset = PlayerMemoryDataset(batch)

            dataloader = DataLoader(
                            dataset, 
                            batch_size=MINIBATCH_SIZE,
                            shuffle=True
                            )

            temp_loss = 0


            for game_state, memory, action, reward, maxq in dataloader:

                player.optimizer.zero_grad()

                prediction = player.response_nnet(game_state,memory)
                ideal_qs = reward + (DISCOUNT * maxq)
                ideal_prediction = prediction.clone()

                # print(torch.mean(ideal_qs))


                for i in range(MINIBATCH_SIZE):

                    choice = np.argmax(action[i])


                    ideal_prediction[i,0,choice] = ideal_qs[i]


                loss = torch.mean((ideal_prediction - prediction)**2)

                

                loss.backward()

                player.optimizer.step()

                temp_loss += loss


            temp_loss /= (BATCH_SIZE/MINIBATCH_SIZE)

            avg_loss += temp_loss

            player.version += 1

            torch.save(player.response_nnet.state_dict(),CURRENT_DIR + f'/Models/{player.name}/Versions/QNet {player.version}')

            if batch_counter%50==0:
                torch.save(player.response_nnet.state_dict(),CURRENT_DIR + f'/Models/{player.name}/QNet Prime')  
                player.best_response_nnet.load_state_dict(torch.load(CURRENT_DIR + f'/Models/{player.name}/QNet Prime'))          



        avg_loss /= 4

        print(f'Batch {batch_counter} completed {datetime.now()} with an avg loss of {avg_loss}')


