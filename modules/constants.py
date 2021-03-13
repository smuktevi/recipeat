import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# AVAILABLE API KEYS
apikey1 = 'apiKey=4078ba908cf14212b9c3754a84a262f5'
apikey2 = 'apiKey=d18b19ea103f46929e677ecacef2c15c'
apikey3 = 'apiKey=000c6ad96dd4406084b8c5492a302592'
apikey4 = 'apiKey=f25da678f94b474ba41918b8da3f390f'
apikey5 = 'apiKey=0e45cc48d56d4c4d9018f326e30b32ee'
apikey6 = 'apiKey=3044984a97a14d01b73d460a186ffa72'
apikey7 = 'apiKey=7754ad2676324bc98dc0d4261ca55d1e'

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

# PostgreSQL database URL
db_url = ("postgres://fbporsgtkyccmc:846ffc72335cec44f0861518fc4d1acfda4f890f5"
          "2471fdb31dda4a637f3932a@ec2-100-24-139-146.compute-1.amazonaws.com:"
          "5432/d9umass2brvfdv")


def get_postgresql_connection():
    """
    Function used to get a connection to the postgreSQL database.

    :return: connection object
    """
    conn = psycopg2.connect(dbname="d9umass2brvfdv", user="fbporsgtkyccmc",
                            password=("846ffc72335cec44f0861518fc4d1acfda4f890"
                                      "f52471fdb31dda4a637f3932a"),
                            host="ec2-100-24-139-146.compute-1.amazonaws.com",
                            sslmode='require')
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


class Ingredient:
    """
    Ingredient class used to make ingredient objects.
    """

    def __init__(self, ingredient_full=None, ingredient_name=None, amount=None,
                 units=None):
        """
        Constructor for the Ingredient object.

        :param ingredient_full: String. Full ingredient name
        :param ingredient_name: String. Ingredient name
        :param amount: int. Amount of ingredient
        :param units: String. Unit of ingredient
        """
        self.ingredient_full = ingredient_full
        self.ingredient = ingredient_name
        self.amount = amount
        self.units = units

    @staticmethod
    def parse_string(ingredient_full):
        """
        Static method used to get an Ingredient object from ingredient
        full name.

        :param ingredient_full: String. Ingredient full name
        :return: Ingredient. Returns the constructed ingredient object
        """
        ingredient_string = ingredient_full.split()
        if (len(ingredient_string) == 2):
            ingredient = Ingredient(ingredient_full=ingredient_full,
                                    ingredient_name=ingredient_string[1],
                                    amount=ingredient_string[0])
        else:
            ingredient = Ingredient(ingredient_full=ingredient_full,
                                    ingredient_name=ingredient_string[2],
                                    amount=ingredient_string[0],
                                    units=ingredient_string[1])
        return ingredient

    def __str__(self):
        """
        Override __str__ method.

        :return: String. Formatted print for Ingredient object
        """
        return_str = self.ingredient + " " + str(self.amount)
        if self.units is not None:
            return_str += " " + self.units
        return return_str

    def __repr__(self):
        """
        Override __repr__ method.

        :return: String. Formatted print for Ingredient object
        """
        return_str = self.ingredient + " " + str(self.amount)
        if self.units is not None:
            return_str += " " + self.units
        return return_str


# Sample ingredient object
sample_ingredient = Ingredient(
    "\'4 cups apple\'", "\'apple\'", "4", "\'cups\'")


class Recipe:
    """
    Recipe class for Recipe object.
    """

    def __init__(self, recipe_id=None, recipe_name: str = None,
                 source_url: str = None, img_url: str = None,
                 description: str = None, ingredients: list = None):
        """
        Constructor for the recipe object

        :param recipe_id: int. Recipe id
        :param recipe_name: String. Recipe name
        :param source_url: String. Source url for the recipe
        :param img_url: String. Image url for the recipe
        :param description: String. Description of the recipe
        :param ingredients: list(Ingredient). List of the ingredients used to
        make the recipe.
        """
        self.recipe_id = recipe_id
        self.recipe_name = recipe_name
        self.source_url = source_url
        self.img_url = img_url
        self.description = description
        self.ingredients = ingredients

    def __str__(self):
        """
        Override __str__ method.

        :return: String. Formatted print for Recipe object
        """
        return ("recipe id: {recipe_id} \n recipe name {recipe_name} \n"
                " source_url: {source_url}").format(
            recipe_id=self.recipe_id, recipe_name=self.recipe_name,
            source_url=self.source_url)


# api key point threshold
api_out_of_points_threshold = 100


def check_api_errors(response):
    """
    Check that we have enough api points to call to Spoonacular.

    :param response: A response object
    Raises exception if there are not enough points, otherwise does nothing.
    """
    if int(response.headers["X-RateLimit-requests-Remaining"]) <= \
            api_out_of_points_threshold or \
            int(response.headers["X-RateLimit-results-Remaining"]) <= \
            api_out_of_points_threshold or \
            int(response.headers["X-RateLimit-tinyrequests-Remaining"]) \
            <= api_out_of_points_threshold:
        raise ApikeyOutOfPoints("This API Key is out of points for the day")


class ApikeyOutOfPoints(Exception):
    """
    Exception class. Raised when API key is out of points.
    """
    pass


# Rapid API header for spoonacular
api_request_headers = {
    'x-rapidapi-key': "c65a4130b1msh767c11b9104ee56p1a93cdjsn9f1028eb2e98",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
}

# Rapid API base URL
api_base_url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
