from .constants import config, Ingredient
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
        self.ingredients = self.db.get(
            "BagOfIngredients", "*", where="user_id=" + self.username
        )
        return self.ingredients

    def push_boi(self, ing: Ingredient):
        # Pushes an ingredient into Bag of Ingredients for the User

        columns = "user_id, ingredient, ingredient_name, amount, unit"
        data = "{0},'{1}','{2}',{3},'{4}'".format(
            self.username, ing.ingredient_full, ing.ingredient, ing.amount,
            ing.units
        )
        push_success = self.db.write("BagOfIngredients", columns, data)
        self.number_of_ingredients += 1
        self.ingredients.append(ing)
        return push_success

    def delete_ingredient(self, ingredient_name):
        # Deletes one ingredient
        try:
            delete_query = (
                "DELETE FROM bagofingredients WHERE user_id="
                + self.username
                + " AND ingredient_name="
                + ingredient_name
                + ";"
            )
            print(delete_query)
            check = self.db.query(delete_query)
        except:
            print("ERROR OCCURED IN DELETION!")
            return False
        return check

    def update_ingredient(self, ingredient_name, new_quantity):
        # Updates ingredient with new quantity
        try:
            update_query = (
                "UPDATE bagofingredients SET amount="
                + new_quantity
                + "WHERE user_id="
                + self.username
                + " AND ingredient_name="
                + ingredient_name
                + ";"
            )
            check = self.db.query(update_query)
        except:
            print("ERROR OCCURED IN UPDATING!")
            return False
        return check
