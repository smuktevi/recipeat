import pandas as pd
from modules.constants import *
import json
from pyrebase import pyrebase
from modules.bag_of_ingredients import BagOfIngredients

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

    def __init__(self, name="", email="", height=0, weight=0, age=0, gender=""):
        self.name = name
        self.email = email
        self.height = height
        self.weight = weight
        self.age = age
        self.gender = gender
        self.bag_of_ingredients = BagOfIngredients()

    @staticmethod
    def authenticate_user(username, password):
        try:
            auth.sign_in_with_email_and_password(username, password)  # Log the user in
        except:
            return False

        # TODO return user object instead of True
        user = User()

        return True

    @staticmethod
    def register_user(username, password):
        try:
            # Successful Registration
            auth.create_user_with_email_and_password(username, password)
        except:
            return False

        # TODO Need to implement a write to firebase realtime database here. (Create account)
        return True

    @staticmethod
    def get_user(username):
        # TODO Read from firebase realtime database. Build user object and return it.
        pass
