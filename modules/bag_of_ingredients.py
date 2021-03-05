import pandas as pd
# from constants import *
from .constants import *
import json
from pyrebase import pyrebase
from urllib.parse import parse_qsl, urljoin, urlparse
# from database import Database
from .database import Database

firebase = pyrebase.initialize_app(config)
db = firebase.database()  # Get a reference to the database service


class BagOfIngredients:
    def __init__(self, username):
        self.username = "\'" + username + "\'"  # use a session variable
        self.ingredients = []
        self.number_of_ingredients = 0
        self.db = Database()
        self.db.open()

    def get_boi(self):
        # Gets bag of ingredients for a certain User

        print("Getting Bag of Ingredients from DB>>>\n", self.db.get(
            "bagofingredients", "*", where="user_id="+self.username))

    def push_boi(self, ing: Ingredient):
        # Pushes an ingredient into Bag of Ingredients for the User

        columns = "user_id, ingredient, ingredient_name, amount, unit"
        data = "{0},{1},{2},{3},{4}".format(self.username,
                                            ing.ingredient_full, ing.ingredient, ing.amount, ing.units)
        print("Pushing "+ing.ingredient_full+" into DB>>> Bag of Ingredients.")
        self.db.write("bagofingredients", columns, data)
        self.number_of_ingredients += 1
        self.ingredients.append(ing)

    def delete_boi(self):
        # Deletes all ingredients from Bag for a User

        print("DELETING from BOI with user_id>>>"+self.username)
        delete_query = "DELETE FROM bagofingredients WHERE user_id="+self.username+";"
        self.db.query(delete_query)

    def update_boi(self):
        # Deletes certain rows and adds others if any changes
        pass

# TEST CASES FOR BOI FOR POSTGRESQL
# boi_sample = BagOfIngredients(username)
# boi_sample.get_boi()
# boi_sample.push_boi(sample_ingredient)


'''
THIS CAN BE USED FOR TESTING FIREBASE (OLD).
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
