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
import aql_features
from AQL import AQL

if __name__ == "__main__":
    database = input("Which database are you using? (Use name.db format) \n")
    command = ""
    currDB = AQL(database)
    while command != "exit":
        command = input("Enter command. Try -help for additional guidance \n")
        if command == "exit":
            break
        commandArr = command.split()

        if commandArr[0].lower() == "create" and commandArr[1].lower() == "table":
            currDB.set_table(commandArr[2])
            default_features = input("Creating a table will use the default AQL features. Please confirm the action (y/n) \n")
            if (default_features == "y"):
                currDB.set_features(aql_features.all_features())
                print(currDB.create_table())
        elif commandArr[0].lower() == "insert":
            if commandArr[1].lower == "batch":
                currDB.set_table(commandArr[3])
                filepath = commandArr[4]
                print(currDB.insert_batch(filepath))
            else:
                currDB.set_table(commandArr[2])
                filepath = commandArr[3]
                print(currDB.insert(filepath))
        elif commandArr[0].lower() == "select":
            print(currDB.select(command))
        else: 
            print("Command not found. Please check ReadMe for additional information.")

