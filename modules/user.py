import pandas as pd
from constants import *
import json
from pyrebase import pyrebase
from bag_of_ingredients import BagOfIngredients

# authorization config will REPLACE
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
db = firebase.database()  # Get a reference to the database service

class User:

    def __init__(self, name = "", email = "", password = "", height = 0, weight = 0, age = 0, gender = ""):
        self.name = name
        self.email = email
        self.password = password
        self.height = height
        self.weight = weight
        self.age = age
        self.gender = gender
        self.bag_of_ingredients = BagOfIngredients()

    def authenticate_user(self, username, password):
        try:
            auth.sign_in_with_email_and_password(self.username, self.password)  # Log the user in
        except:
            return False

        # TODO return user object instead of True

        return True

    def register_user(self):
        try:
            # Successful Registration
            auth.create_user_with_email_and_password(self.username, self.password)


            # TODO May need to implement a read/write to firebase realtime database here. (Create account)
        except:
            return False

    def get_user_details(self):
        # TODO implement this if necessary
        pass