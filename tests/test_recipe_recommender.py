import unittest
import requests
import pandas as pd
from modules.constants import *
from modules.recipe_recommender import *


class Test_Search_Recipes(unittest.TestCase):
    # test if recipes returned meet the nutritional requirements
    def test_nutrition_requirements(self):
        nutrients = {
            'minCarbs': 1,
            'maxCarbs': 100,
            'minProtein': 1,
            'maxProtein': 100,
            'minCalories': 100,
            'maxCalories': 1000,
            'minFat': 1,
            'maxFat': 100
        }
        rr = RecipeRecommender()
        recipes = rr.search_recipes(nutritional_req=nutrients)

        payload = {}
        headers = {
            'Cookie': '__cfduid=d443da310537f29e03b78e744720641111613622052'
        }
        slicer = slice(0, -1, 1)
        for recipe in recipes:
            get_nutrition_url = "https://api.spoonacular.com/recipes/{id}/nutritionWidget.json?{apikey}".format(
                id=recipe.recipe_id, apikey=apikey6)

            response = requests.request(
                "GET", get_nutrition_url, headers=headers, data=payload)

            recipeCalories = int(response["calories"])
            recipeCarbs = int(response["carbs"][slicer])
            recipeProtein = int(response["protein"][slicer])
            recipeFat = int(response["fat"][slicer])

            self.assertGreaterEqual(
                nutrients["maxCalories"], recipeCalories, "Recipe calories > maxCalories")
            self.assertGreaterEqual(
                nutrients["maxCarbs"], recipeCarbs, "Recipe carbs > maxCarbs")
            self.assertGreaterEqual(
                nutrients["maxProtein"], recipeProtein, "Recipe protein > maxProtein")
            self.assertGreaterEqual(
                nutrients["maxFat"], recipeFat, "Recipe fat > maxFat")

            self.assertLessEqual(
                nutrients["minCalories"], recipeCalories, "Recipe calories < minCalories")
            self.assertLessEqual(
                nutrients["minCarbs"], recipeCarbs, "Recipe carbs < minCarbs")
            self.assertLessEqual(
                nutrients["minProtein"], recipeProtein, "Recipe protein < minProtein")
            self.assertLessEqual(
                nutrients["minFat"], recipeFat, "Recipe fat < minFat")

#     # test if recipes returned include at least one of the input ingredients
#     def test_ingredient_requirements(self):


#     # test if the recipes returned meet diet requirements
#     def test_diet_requirements(self):

#     # test if the recipes returned meet intolerance requirements
#     def test_intolerances_requirements(self):

# class Test_Recipe_to_Ingredients(unittest.TestCase):
#     # test if recipe is valid/raises appropriate exception with recipe_id is not valid

# class Test_Get_Recipe_Info(unittest.TestCase):
#     # test if recipe is valid/raises appropriate exception with recipe_id is not valid

if __name__ == '__main__':
    unittest.main()
