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
from pprint import pprint


class AQL:
    #use case: all information passed in by user
    def __init__(self, database, table, features):
        self.database = database
        self.table = table
        self.features = features
    
    #use case: new database - not set up yet, so no relevant tables or features
    def __init__(self, database):
        self.database = database

    #use case: accessing database and creating a table with default features
    def __init__(self, database, table):
        self.database = database
        self.table = table
        self.features = aql_features.all_features()
    
    #use case: need to set new table to create or access different table
    def set_table(self, table):
        self.table = table
    
    def set_features(self, features):
        self.features = features

    def create_database(self):
        try: 
            con = sqlite3.connect(self.database)
            print("Success!")
        except Exception as e:
            print(e)

    def create_table(self):
        con = sqlite3.connect(self.database)
        cur = con.cursor()
        SQL_string = "CREATE TABLE " + self.table + "(filepath"
        for f in self.features:
            SQL_string += ", " + f[0]
        SQL_string += ")"
        try: 
            cur.execute(SQL_string)
            con.commit()
            con.close()
            print("Success!")
        except Exception as e:
            print(e)

    def insert(self, filepath):
        con = sqlite3.connect(self.database)
        cur = con.cursor()

        SQL_string = "INSERT INTO " + self.table + " VALUES ('" + filepath + "'"
        for f in self.features:
            method = f[1]
            result = ""
            try:
                result = method(filepath)
            except Exception as e:
                print("Error while executing feature " + f[0] + ": ", e)
                return

            if (type(result) == str):
                SQL_string += ", '" + result + "'" 
            else:
                SQL_string += ", " + str(result)
            
        SQL_string += ")"

        try: 
            cur.execute(SQL_string)
            con.commit()
            con.close()
            print("Success!")
        except Exception as e:
            print(e)

    def insert_batch(self, filepath):
        for filename in os.listdir(filepath):
            f = os.path.join(filepath, filename)
            if os.path.isfile(f):
                self.insert(f)

    def select(self, query):
        con = sqlite3.connect(self.database)
        cur = con.cursor()
        cur.execute(query)
        res = cur.fetchall()
        con.commit()
        con.close()
        pprint(res)
