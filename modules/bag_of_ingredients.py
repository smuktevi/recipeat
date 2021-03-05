import pandas as pd
from constants import *
# from .constants import *
import json
from pyrebase import pyrebase
import urllib.parse
from database import Database
# from .database import Database

firebase = pyrebase.initialize_app(config)
db = firebase.database()  # Get a reference to the database service


class BagOfIngredients:
    def __init__(self):
        self.username = None
        self.ingredients = []
        self.number_of_ingredients = 0
        self.db = Database(db_url)

    def get_boi(self):
        # user = db.child("users").get()
        # print(user.key(), user.val())
        print(self.db.get("bagofingredients"))

    def push_boi(self, data):
        db.child("users").child(self.username).set(data)

    def update_boi(self, key, data):
        _update = {key: data}
        db.child("users").child(self.username).update(_update)

    def delete_boi(self):
        self.ingredients = []
        self.number_of_ingredients = 0
        db.child("users").child(self.username).remove()


boi_sample = BagOfIngredients()
authenticated = boi_sample.authenticate_user(username, password)
if authenticated:
    print("AUTHENTICATED!!")
    boi_sample.get_boi()

'''
THIS CAN BE USED FOR TESTING.
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
