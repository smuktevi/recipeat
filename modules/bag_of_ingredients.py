from .constants import config, Ingredient
from pyrebase import pyrebase
from .database import Database
from psycopg2 import Error

firebase = pyrebase.initialize_app(config)
db = firebase.database()  # Get a reference to the database service


class BagOfIngredients:
    """
    BagOfIngredient class. Creates a BagOfIngredient object that can be used to
    add ingredients, update ingredients, and delete ingredients for a certain
    user.
    """

    def __init__(self, username):
        """
        Constructor for BagOfIngredients. Takes in a username and setups the
        bag.

        :param username: String. Username (email) of the User.
        """
        self.username = "'" + username + "'"  # use a session variable
        self.ingredients = []
        self.number_of_ingredients = 0
        self.boi = None
        self.db = Database()
        self.db.open()

    def get_boi(self):
        """
        Queries the database for the user's bag of ingredients and returns a
        list of ingredients

        :return: list(Ingredient). A list of ingredient objects.
        """
        self.ingredients = self.db.get(
            "BagOfIngredients", "*", where="user_id=" + self.username
        )
        return self.ingredients

    def push_boi(self, ing: Ingredient):
        """
        Function used to add ingredient to database.

        :param ing: Ingredient. Ingredient to be added
        :return: Boolean. True if ingredient was added, false otherwise
        """
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
        """
        Function used to delete a single ingredient from the ingredient list.

        :param ingredient_name: String. Name of ingredient to be deleted.
        :return: Boolean. True if ingredient was deleted, false otherwise.
        """
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
        except (Error, Exception):
            print("ERROR OCCURED IN DELETION!")
            return False
        return check

    def update_ingredient(self, ingredient_name, new_quantity):
        """
        Function to update the quantity of a certain ingredient.

        :param ingredient_name: String. Name of ingredient to be updated.
        :param new_quantity: int. New quantity of ingredient.
        :return: Boolean. True if ingredient was updated, false otherwise.
        """
        # Updates ingredient with new quantity
        try:
            unit = self.db.get(table="bagofingredients", columns="unit",
                               where=("user_id = {} AND ingredient_name = "
                                      "{}").format(self.username,
                                                   ingredient_name))
            full = new_quantity.replace("'", "") + " " + unit[0][0] + " " + \
                ingredient_name.replace("'", "")
            update_query = ("UPDATE bagofingredients SET amount = {}, ingredie"
                            "nt = '{}' WHERE user_id = {} AND ingredient_name"
                            "= {}").format(new_quantity, full, self.username,
                                           ingredient_name)
            check = self.db.query(update_query)
        except (Error, Exception):
            print("ERROR OCCURED IN UPDATING!")
            return False
        return check
