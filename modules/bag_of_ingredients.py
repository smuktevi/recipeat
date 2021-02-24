import pandas as pd
from constants import *
# from firebase import firebase
from pyrebase import pyrebase

class BagOfIngeredients:
    def __init__(self):
        self.ingredients = []
        self.number_of_ingredients = 0
        self.user_id = 0
        #get bag of ingredients from database and convert to pandas dataframe

    def authenticate_user():
        pass

    def get_boi():
        pass

    def update_boi():
        pass

    def delete_boi():
        self.ingredients = []
        self.number_of_ingredients = 0


#authorization config will REPLACE
config = {
    "apiKey": "AIzaSyALmQ-MUJqlIWPmZZK8P73JTxgiWFzcTwY",
    "authDomain": "recipeat-e5c29.firebaseapp.com",
    "databaseURL": "https://recipeat-e5c29-default-rtdb.firebaseio.com",
    "projectId": "recipeat-e5c29",
    # 'serviceAccount': ""
    "storageBucket": "recipeat-e5c29.appspot.com",
    "messagingSenderId": "141820818637",
    "appId": "1:141820818637:web:303e5636dc57aabbd9e584",
    "measurementId": "G-SHGP23CXCE"
}

firebase = pyrebase.initialize_app(config)

#for now using defaults
username = "saivenkatnow@gmail.com"
password = "vishu123"
######

#try insert into firebase:
# Get a reference to the auth service
auth = firebase.auth()

# Log the user in
user = auth.sign_in_with_email_and_password(username, password)
# Get a reference to the database service
db = firebase.database()
# data to save
data = {
    "name": "Mortimer 'Morty' Smith",
    "description": "SUCCESSFUL DATABASE PUSH!!"
}
data_2 = {
    "name": "Recipeat Users",
    "BagOfIngredients" : [
        
        {"1": "Apple"}, 
        {"12": "Grapes"} 
    ]
    
}
# Pass the user's idToken to the push method
results = db.child("users").push(data, user['idToken'])
db.child("new_node").child("users").set(data_2)
print(results)