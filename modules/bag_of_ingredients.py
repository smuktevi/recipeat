import pandas as pd
from modules.constants import *
import json
from pyrebase import pyrebase

firebase = pyrebase.initialize_app(config)
db = firebase.database() # Get a reference to the database service

class BagOfIngredients:
    def __init__(self):
        self.username = None
        self.ingredients = []
        self.number_of_ingredients = 0
        self.db_user = None
        #get bag of ingredients from database and convert to pandas dataframe

    def get_boi(self):
        user = db.child("users").get()
        print(user.key(), user.val())

    def push_boi(self, data):
        db.child("users").child(self.username).set(data)

    def update_boi(self, key, data):
        _update = {key:data}
        db.child("users").child(self.username).update(_update)
        
    def delete_boi(self):
        self.ingredients = []
        self.number_of_ingredients = 0
        db.child("users").child(self.username).remove()


'''
data = sample_user #check constants.py

# CRUD operations example with predefined user from constants.py
boi_sample = BagOfIngredients()
authenticated = boi_sample.authenticate_user(username, password)
if authenticated:
    print("AUTHENTICATED!!")
    boi_sample.get_boi()
    boi_sample.push_boi(sample_user)
    boi_sample.update_boi("diet","non-vegetarian")
    # boi_sample.delete_boi()
'''