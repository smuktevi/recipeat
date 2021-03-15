from .constants import config, Ingredient
from pyrebase import pyrebase
from .database import Database

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
        except:
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

    @staticmethod
    def to_json(recipe_list):
        """
        Function used to serialize a list of recipes.

        :param recipe_list: list(Recipe). list of recipes
        :return: json. A json dictionary to be serialized.
        """
        return json.dumps(recipe_list, default=lambda o: o.__dict__,
                        sort_keys=True, indent=4)

    @staticmethod
    def from_json(json_list):
        """
        Function used to convert a serialized dictionary back to a list of recipes.

        :param json_list: json. A json dictionary.
        :return: list(Recipe). List of recipes constructed back
        """
        json_list = json.loads(json_list)
        recipe_list = reconstruct_recipe_list(json_list)
        return recipe_list

    @staticmethod
    def reconstruct_recipe_list(recipe_dictionary_list):
        """
        This is a helper function used to reconstruct Recipe and Ingredient objects
        back into their original form from a dictionary.

        :param recipe_dictionary_list: dict. A serialized dictionary.
        :return: list(Recipe). List of recipes constructed from the dictionary.
        """
        recipe_list = []
        for recipe_dictionary in recipe_dictionary_list:
            recipe_id = recipe_dictionary['recipe_id']
            recipe_name = recipe_dictionary['recipe_name']
            recipe_source_url = recipe_dictionary['source_url']
            recipe_img_url = recipe_dictionary['img_url']
            recipe_description = recipe_dictionary['description']
            ingredient_list = []
            for ingredient in recipe_dictionary['ingredients']:
                ingredient_full_name = ingredient['ingredient_full']
                ingredient_name = ingredient['ingredient']
                ingredient_amount = ingredient['amount']
                ingredient_unit = ingredient['units']
                new_ingredient = Ingredient(ingredient_full=ingredient_full_name,
                                            ingredient_name=ingredient_name,
                                            amount=ingredient_amount,
                                            units=ingredient_unit)
                ingredient_list.append(new_ingredient)
            new_recipe = Recipe(recipe_id=recipe_id, recipe_name=recipe_name,
                                source_url=recipe_source_url,
                                img_url=recipe_img_url,
                                description=recipe_description,
                                ingredients=ingredient_list)
            recipe_list.append(new_recipe)
        return recipe_list
