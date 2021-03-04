import pandas as pd
from .constants import *
import json
from pyrebase import pyrebase
import urllib.parse

firebase = pyrebase.initialize_app(config)
db = firebase.database() # Get a reference to the database service

class BagOfIngredients:
    def __init__(self):
        self.username = None
        self.ingredients = []
        self.number_of_ingredients = 0
        self.db_user = None
        #get bag of ingredients from database and convert to pandas dataframe

        self.conn = None
        self.cursor = None
        if url:
            self.open(url)
    
    def open(self,url):
	
        self.url = url
	
	# Access credentials via the passed on url. The url must
	# be parsed with the urlparse library. 
	self.conn = psycopg2.connect(database = 
        self.url.path[1:],
        user = self.url.username,
        password = self.url.password,
        host = self.url.hostname,
        port = self.url.port)
            
        self.cursor = self.conn.cursor()

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