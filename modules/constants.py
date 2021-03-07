import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# class Recipe:
#     def __init__(self, recipe_id=None, recipe_name=None, source_url=None, img_url=None, description=None, ingredients=None):
#         self.recipe_id = recipe_id
#         self.recipe_name = recipe_name
#         self.source_url = source_url
#         self.img_url = img_url
#         self.description = description
#         self.ingredients = ingredients  # list


# AVAILABLE API KEYS
apikey1 = 'apiKey=4078ba908cf14212b9c3754a84a262f5'
apikey2 = 'apiKey=d18b19ea103f46929e677ecacef2c15c'
apikey3 = 'apiKey=000c6ad96dd4406084b8c5492a302592'
apikey4 = 'apiKey=f25da678f94b474ba41918b8da3f390f'
apikey5 = 'apiKey=0e45cc48d56d4c4d9018f326e30b32ee'
apikey6 = 'apiKey=3044984a97a14d01b73d460a186ffa72'

# Config firebase
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

db_url = "postgres://fbporsgtkyccmc:846ffc72335cec44f0861518fc4d1acfda4f890f52471fdb31dda4a637f3932a@ec2-100-24-139-146.compute-1.amazonaws.com:5432/d9umass2brvfdv"


def get_postgresql_connection():
    conn = psycopg2.connect(dbname="d9umass2brvfdv", user="fbporsgtkyccmc",
                            password="846ffc72335cec44f0861518fc4d1acfda4f890f52471fdb31dda4a637f3932a",
                            host="ec2-100-24-139-146.compute-1.amazonaws.com", sslmode='require')
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return conn


# sample user details
username = "q@gmail.com"
password = "qwerty01"
usn = "johndoe1"

# sample user json data
sample_user = {
    "email": "recipeat@gmail.com",
    "username": "johndoe1",
    "details": {
        "height": "999",
        "weight": "999",
        "age": "999",
        "gender": "male"
    },
    "boi": [
        {
            "ingredientFull": "1 cup green tea",
            "ingredient": "green tea",
            "amount": 1,
            "unit": "cup"
        },
        {
            "ingredientFull": "2 oz mushrooms",
            "ingredient": "mushrooms",
            "amount": 2,
            "unit": "oz"
        },
        {
            "ingredientFull": "150 g egg whites",
            "ingredient": "egg whites",
            "amount": 150,
            "unit": "g"
        }
    ],
    "cuisine": [
        "italian"
    ],
    "tolerances": [
        "gluten"
    ],
    "diet": "vegetarian"
}


class Preferences:
    def __init__(self, cuisine: list, intolerances: list, diet: list, calories_per_day: int):
        self.cuisine = cuisine
        self.intolerances = intolerances
        self.diet = diet
        self.calories_per_day = calories_per_day

'''
class IngredientRR:
    def __init__(self, ingredient: str, amount: int, unit: str):
        self.ingredient = ingredient
        self.amount = amount
        self.unit = unit

    def __str__(self):
        return "ingredients: {ingredients} \n amount: {amount} {unit} \n".format(ingredients=self.ingredient, amount=self.amount, unit=self.unit)
'''

class Ingredient:
    def __init__(self, ingredient_full=None, ingredient_name=None, amount=None, units=None):
        self.ingredient_full = ingredient_full
        self.ingredient = ingredient_name
        self.amount = amount
        self.units = units

    @staticmethod
    def parse_string(ingredient_full):
        ingredient_string = ingredient_full.split()
        if(len(ingredient_string) == 2):
            ingredient = Ingredient(ingredient_full=ingredient_full, ingredient_name=ingredient_string[1], amount=ingredient_string[0])
        else:
            ingredient = Ingredient(ingredient_full=ingredient_full, ingredient_name=ingredient_string[2], amount=ingredient_string[0], units=ingredient_string[1])
        return ingredient

    def __str__(self):
        return_str = self.ingredient + " " + str(self.amount)
        if self.units is not None:
            return_str += " " + self.units
        return return_str

    def __repr__(self):
        return_str = self.ingredient + " " + str(self.amount)
        if self.units is not None:
            return_str += " " + self.units
        return return_str


sample_ingredient = Ingredient(
    "\'4 cups apple\'", "\'apple\'", "4", "\'cups\'")


class Recipe:
    def __init__(self, recipe_id=None, recipe_name: str = None, source_url: str = None, img_url: str = None, description: str = None, ingredients: list = None):
        # , calories:int, carbs:int, protein:int, fat:int):
        self.recipe_id = recipe_id
        self.recipe_name = recipe_name
        self.source_url = source_url
        self.img_url = img_url
        self.description = description
        self.ingredients = ingredients
        # self.calories = calories
        # self.carbs = carbs
        # self.protein = protein
        # self.fat = fat

    def __str__(self):
        # return "recipe id: {recipe_id} \n recipe name {recipe_name} \n source_url: {source_url} \n img_url: {img_url} \n calories: {calories} \n carbs: {carbs} \n protein: {protein} \n fat: {fat}".format(recipe_id=self.recipe_id, recipe_name=self.recipe_name, source_url=self.source_url, img_url=self.img_url, calories=self.calories, carbs=self.carbs, protein=self.protein, fat=self.fat)
        return "recipe id: {recipe_id} \n recipe name {recipe_name} \n source_url: {source_url} \n".format(recipe_id=self.recipe_id, recipe_name=self.recipe_name, source_url=self.source_url)
