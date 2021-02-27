import pandas as pd
from constants import *
import json
from pyrebase import pyrebase

class BagOfIngredients:
    def __init__(self):
        self.username = None
        self.ingredients = []
        self.number_of_ingredients = 0
        self.db_user = None
        #get bag of ingredients from database and convert to pandas dataframe

    def authenticate_user(self, username, password):
        self.username = usn
        try:
            self.db_user = auth.sign_in_with_email_and_password(username, password) # Log the user in
        except:
            return False
        return True

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


#authorization config will REPLACE
config = {
    "apiKey": "AIzaSyALmQ-MUJqlIWPmZZK8P73JTxgiWFzcTwY",
    "authDomain": "recipeat-e5c29.firebaseapp.com",
    "databaseURL": "https://recipeat-e5c29-default-rtdb.firebaseio.com",
    "projectId": "recipeat-e5c29",
    "storageBucket": "recipeat-e5c29.appspot.com",
    "messagingSenderId": "141820818637",
    "appId": "1:141820818637:web:303e5636dc57aabbd9e584",
    "measurementId": "G-SHGP23CXCE"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database() # Get a reference to the database service

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
    