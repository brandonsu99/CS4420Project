import sqlite3
import os
import torch
import torchaudio
import librosa
import IPython.display as ipd
import matplotlib.pyplot as plt
import requests
import tensorflow
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms, datasets 
from PIL import Image

def plot_audio(filename):
    waveform, sample_rate = torchaudio.load(filename)
    plt.figure()
    plt.plot(waveform.t().numpy())
    return waveform, sample_rate

#returns int
def get_sample_rate(filename):
    return torchaudio.info(filename).sample_rate

#returns int
def get_num_frames(filename):
    return torchaudio.info(filename).num_frames

#returns int
def get_num_channels(filename):
    return torchaudio.info(filename).num_channels

#returns int
def get_bits_per_sample(filename):
    return torchaudio.info(filename).bits_per_sample

#returns string
def get_encoding(filename):
    return torchaudio.info(filename).encoding


class CNNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=5)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(51136, 50)
        self.fc2 = nn.Linear(50, 2)

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        #x = x.view(x.size(0), -1)
        x = self.flatten(x)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = F.relu(self.fc2(x))
        return F.log_softmax(x,dim=1)

#returns string
def classify_audio(filePath):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = CNNet().to(device)
    model.load_state_dict(torch.load("./model.pth", map_location = device))
    model.eval()
    waveform, sample_rate = plot_audio(filePath)
    spectrogram_tensor = torchaudio.transforms.Spectrogram()(waveform)

    # fig = plt.figure()
    filename = os.pat
    h.basename(filePath)
    plt.imsave(f'./data/spectrograms/yes/{filename}.png', spectrogram_tensor.log2()[0,:,:].numpy(), cmap='gray')
    
    file_image = datasets.ImageFolder(
                    root= './data/spectrograms',
                    transform=transforms.Compose([transforms.Resize((201,81)),
                                                transforms.ToTensor()
                                                ])
                )
    dataloader = torch.utils.data.DataLoader(
        file_image,
        batch_size=1,
        num_workers=0,
        shuffle=True
    )

    for batch, (X, Y) in enumerate(dataloader):
        X, Y = X.to(device), Y.to(device)
        pred = model(X)
        pred.argmax(1)

    if (pred.argmax(1)[0] == 0):
        return "Yes"
    elif (pred.argmax(1)[0] == 1):
        return "No"
    else:
        return "Error - no classification found"

#returns int
def find_tempo(filename):
  y, sr = librosa.load(filename)
  onset_env = librosa.onset.onset_strength(y, sr=sr)
  tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)
  return tempo[0].item()


#returns all features in list
def all_features():
    features = [
        ("sample_rate", get_sample_rate),
        ("num_frames", get_num_frames),
        ("num_channels", get_num_channels),
        ("bits_per_sample", get_bits_per_sample),
        ("encoding", get_encoding),
        ("command_classification", classify_audio),
        ("tempo", find_tempo),
    ]
    return features
