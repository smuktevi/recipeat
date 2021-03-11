from .constants import *
from pyrebase import pyrebase
from .database import Database

firebase = pyrebase.initialize_app(config)
db = firebase.database()  # Get a reference to the database service


class BagOfIngredients:
    def __init__(self, username):
        self.username = "'" + username + "'"  # use a session variable
        self.ingredients = []
        self.number_of_ingredients = 0
        self.boi = None
        self.db = Database()
        self.db.open()

    def get_boi(self):
        # Gets bag of ingredients for a certain User

        # print("Getting Bag of Ingredients from DB>>>\n", self.db.get("bagofingredients", "*", where="user_id="+self.username))
        self.ingredients = self.db.get(
            "BagOfIngredients", "*", where="user_id=" + self.username
        )
        print(">>>>")
        return self.ingredients
        
    def push_boi(self, ing: Ingredient):
        # Pushes an ingredient into Bag of Ingredients for the User

        columns = "user_id, ingredient, ingredient_name, amount, unit"
        data = "{0},'{1}','{2}',{3},'{4}'".format(
            self.username, ing.ingredient_full, ing.ingredient, ing.amount, ing.units
        )
        print("Pushing " + ing.ingredient_full + " into DB>>> Bag of Ingredients.")
        push_success = self.db.write("BagOfIngredients", columns, data)
        self.number_of_ingredients += 1
        self.ingredients.append(ing)
        return push_success

    def delete_ingredient(self, ingredient_name):
        # Deletes one ingredient

        try:
            print(
                "DELETING ingredient "
                + ingredient_name
                + " from BOI with user_id>>>"
                + self.username
            )
            delete_query = (
                "DELETE FROM bagofingredients WHERE user_id="
                + self.username
                + "AND ingredient_name="
                + ingredient_name
                + ";"
            )
            self.db.query(delete_query)
        except:
            print("ERROR OCCURED IN DELETION!")
            return False
        return True

    def update_ingredient(self, ingredient_name, new_quantity):
        # Updates ingredient with new quantity

        # NEED TO IMPLEMENT CHECK IF INGREDIENT ALREADY IN BAG.

        try:
            print(
                "UPDATING ingredient "
                + ingredient_name
                + " from BOI with user_id>>>"
                + self.username
            )
            delete_query = (
                "UPDATE bagofingredients SET amount="
                + new_quantity
                + "WHERE user_id="
                + self.username
                + "AND ingredient_name="
                + ingredient_name
                + ";"
            )
            self.db.query(delete_query)
        except:
            print("ERROR OCCURED IN UPDATING!")
            return False
        return True


# TEST CASES FOR BOI FOR POSTGRESQL
# boi_sample = BagOfIngredients(username)
# boi_sample.get_boi()
# boi_sample.push_boi(sample_ingredient)

"""
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
"""
