from modules.recipe_recommender import RecipeRecommender
from modules.constants import Recipe, Ingredient
import unittest
import requests


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
        recipe_list = RecipeRecommender.search_recipes(ingredients, nutrients, diet,
                                             intolerances)
        self.assertIsInstance(recipe_list, list)
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


if __name__ == '__main__':
    unittest.main()
