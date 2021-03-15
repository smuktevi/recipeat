from modules.recipe_recommender import RecipeRecommender, to_json, from_json
from modules.constants import Recipe, Ingredient
import unittest
import requests
import json


class TestSearchRecipes(unittest.TestCase):
    """
    This unittest class is used to test the recipe_recommender module
    """

    def test_search_recipes(self):
        """
        Search for a recipe with given attributes. Should get a list of
        recipes back.
        """
        nutrients = {'maxCarbs': '100'}
        ingredients = ['potatoes']
        diet = 'vegetarian'
        intolerances = ['dairy']
        recipe_list = RecipeRecommender.search_recipes(ingredients, nutrients,
                                                       diet, intolerances)
        self.assertIsInstance(recipe_list, list)
        if len(recipe_list) > 0:
            self.assertIsInstance(recipe_list[0], Recipe)

    def test_recipe_to_ingredients(self):
        """
        Get the ingredients of a certain recipe. Should get an Ingredient
        list back.
        """
        list_of_ingredients = RecipeRecommender.recipe_to_ingredients(632944)
        self.assertIsInstance(list_of_ingredients, list)
        self.assertIsInstance(list_of_ingredients[0], Ingredient)

    def test_get_recipe_info(self):
        """
        Get recipe info from a recipe_id. Should get a request response back.
        """
        response = RecipeRecommender.get_recipe_info(632944)
        self.assertIsInstance(response, requests.Response)


class TestRecipeJSON(unittest.TestCase):
    """
    This is a test class to test the functionality
    of JSON conversion for Recipe objects.
    """

    def __init__(self, *args, **kwargs):
        super(TestRecipeJSON, self).__init__(*args, **kwargs)
        self.recipe_list = [
            Recipe(
                recipe_id=631763,
                recipe_name="Warm and Luscious Sipping Chocolate",
                img_url=("https://spoonacular.com/recipeImages"
                         "/631763-312x231.jpg"),
                ingredients=[
                    Ingredient(ingredient_name="salt", amount=2),
                    Ingredient(ingredient_name="potato", amount=3,
                               units="gram"),
                ],
                source_url=("https://spoonacular.com/recipes/warm-and-luscious"
                            "-sipping-chocolate-with-xocai-healthy-dark-sippin"
                            "g-xocolate-631763"),
            ),
            Recipe(
                recipe_id=632944,
                recipe_name="Asparagus Soup",
                img_url=("https://spoonacular.com/recipeImages"
                         "/632944-312x231.jpg"),
                ingredients=[
                    Ingredient(ingredient_name="not salt", amount=99),
                    Ingredient(
                        ingredient_name="not potato", amount=999,
                        units="grammys"
                    ),
                ],
                source_url=("https://www.onceuponachef.com/recipes/asparagus-s"
                            "oup-with-lemon-and-parmesan.html"),
            ),
        ]
        self.json_obj = json.dumps(self.recipe_list,
                                   default=lambda o: o.__dict__,
                                   sort_keys=True, indent=4)

    def test_to_json(self):
        """
        Test Conversion of Recipe object to JSON format.
        """
        output = to_json(self.recipe_list)
        self.assertEqual(output, self.json_obj)

    def test_from_json(self):
        """
        Test Conversion of JSON to Recipe object.
        """
        output = from_json(self.json_obj)
        self.assertIsInstance(output, list)
        self.assertIsInstance(output[0], Recipe)


if __name__ == '__main__':
    unittest.main()
