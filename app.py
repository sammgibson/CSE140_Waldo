import torch
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import Dataset, DataLoader
import numpy as np


def load_dataset():
    data_path = '/train' # WILL NEED TO CHANGE THIS
    train_dataset = torchvision.datasets.Imagefolder(
        root = data_path,
        transforms=torchvision.transforms.ToTensor()
        )
    train_load = torch.utils.data.DataLoader(
        train_dataset,
        batch_size=64,
        num_workers=0,
        shuffle=True
        )
    return train_loader


transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

trainset = load_dataset()
classes = ('waldo', 'not waldo')
