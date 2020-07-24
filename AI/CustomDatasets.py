import torch
from torch.utils.data import Dataset, DataLoader

class GameMemoryDataset(Dataset):

    def __init__(self,data):
        self.data = data
        
    def __len__(self):
        return len(self.data)
        
    def __getitem__(self,index):

        if torch.is_tensor(index):
            index = index.tolist()

        item = self.data[index]
        
                
        return item[0],item[1],item[2]


class PlayerMemoryDataset(Dataset):

    def __init__(self,data):
        self.data = data
        
    def __len__(self):
        return len(self.data)
        
    def __getitem__(self,index):

        if torch.is_tensor(index):
            index = index.tolist()

        item = self.data[index]
        
                
        return item[0],item[1],item[2],item[3],item[4]