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

#testing file

def create_table(database, tableName, columns):
    con = sqlite3.connect(database)
    cur = con.cursor()
    SQL_string = "CREATE TABLE " + tableName
    if len(columns) == 0:
        #SQL_string += " (file link, pitch, tempo, classification)"
        SQL_string += " (file path, tempo, command_classification)"
    else:
        SQL_string += " (file path, tempo, command_classification"
        for c in columns:
            SQL_string += ", " + c
        SQL_string += ")"
    try: 
        cur.execute(SQL_string)
        con.commit()
        con.close()
        return "Success!"
    except:
        return "Error - try again"


def insert(database, table, filePath):
    con = sqlite3.connect(database)
    cur = con.cursor()

    #waveform, sample_rate = aql_features.plot_audio(filePath)
    tempoArr = aql_features.find_tempo(filePath)
    tempo = tempoArr[0]

    classification = aql_features.classify_audio(filePath)
    #SQL_string = "INSERT INTO " + table + " VALUES ('" + filePath + "', '" + pitch_array + "', " + tempo
    SQL_string = "INSERT INTO " + table + " VALUES ('" + filePath + "', " + str(tempo) + ", '" + classification + "')"
    print(SQL_string)
    # try: 
    #     cur.execute(SQL_string)
    #     con.commit()
    #     con.close()
    #     return "Success!"
    # except:
    #     return "Error - try again"



if __name__ == "__main__":
    database = input("Which database are you using? (Use name.db format) \n")
    command = ""
    while command != "exit":
        command = input("Enter command. Try -help for additional guidance \n")
        if command == "exit":
            break
        commandArr = command.split()
        if commandArr[0].lower() == "create" and commandArr[1].lower() == "table":
            tableName = commandArr[2]
            colArr = []
            if len(commandArr) > 3:
                for i in range(3, len(commandArr)):
                    colArr.append(commandArr[i])
            print(create_table(database, tableName, colArr))
        if commandArr[0].lower() == "insert":
            tableName = commandArr[2]
            filepath = commandArr[3]
            additionalFields = []
            if len(commandArr) > 4:
                for i in range(4, len(commandArr)):
                    additionalFields.append(commandArr[i])
            print(insert(database, tableName, filepath, additionalFields))

