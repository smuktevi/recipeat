import unittest
import requests
import pandas as pd
from modules.constants import *
from modules.recipe_recommender import *


class TestSearchRecipes(unittest.TestCase):
    """
    This Class is used to test the Recipes returned from search_recipes
    """

    def __init__(self, *args, **kwargs):
        super(TestSearchRecipes, self).__init__(*args, **kwargs)
        self.rr = RecipeRecommender()
        self.payload = {}
        self.headers = {
            'Cookie': '__cfduid=d443da310537f29e03b78e744720641111613622052'
        }

    def test_nutrition_requirements(self):
        """
        Test if Recipes returned meet the nutritional requirements
        """
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

        recipes = self.rr.search_recipes(nutritional_req=nutrients)

        slicer = slice(0, -1, 1)
        for recipe in recipes:
            get_nutrition_url = "https://api.spoonacular.com/recipes/{id}/nutritionWidget.json?{apikey}".format(
                id=recipe.recipe_id, apikey=apikey4)

            response = requests.request(
                "GET", get_nutrition_url, headers=self.headers, data=self.payload)
            results = response.json()

            recipeCalories = int(results["calories"])
            recipeCarbs = int(results["carbs"][slicer])
            recipeProtein = int(results["protein"][slicer])
            recipeFat = int(results["fat"][slicer])

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

    def test_ingredient_requirements(self):
        """
        Test if Recipes returned includes at least one of the input ingredients
        """
        ingredients = ["chicken", "potato"]
        recipes = self.rr.search_recipes(ingredients=ingredients)
        # print(recipes)
        contains_ingredient = False
        for recipe in recipes:
            recipe_ingredients = RecipeRecommender.recipe_to_ingredients(
                recipe.recipe_id)
            # print(recipe.recipe_name)
            for recipe_ingredient in recipe_ingredients:
                # print(recipe_ingredient.ingredient)
                contains_ingredient = contains_ingredient or recipe_ingredient.ingredient in ingredients

        self.assertTrue(
            contains_ingredient, "recipes do not contain at least one provided ingredient")

    def test_diet_requirements(self):
        """
        Test if the recipes returned meet diet requirements
        """
        diets = ["glutenFree", "vegetarian", "vegan"]

        # test gluten-free
        recipes_gf = self.rr.search_recipes(diet=diets[0])

        for recipe in recipes_gf:
            get_recipe_info_url = "https://api.spoonacular.com/recipes/{id}/information?{apikey}".format(
                id=recipe.recipe_id, apikey=apikey4)

            response = requests.request(
                "GET", get_recipe_info_url, headers=self.headers, data=self.payload)
            results = response.json()
            self.assertTrue(results["glutenFree"],
                            "recipes are not gluten free")

        # test vegetarian
        recipes_veg = self.rr.search_recipes(diet=diets[1])

        for recipe in recipes_veg:
            get_recipe_info_url = "https://api.spoonacular.com/recipes/{id}/information?{apikey}".format(
                id=recipe.recipe_id, apikey=apikey4)

            response = requests.request(
                "GET", get_recipe_info_url, headers=self.headers, data=self.payload)
            results = response.json()
            self.assertTrue(results["vegetarian"],
                            "recipes are not vegetarian")

        # test vegan
        recipes_vegan = self.rr.search_recipes(diet=diets[2])

        for recipe in recipes_vegan:
            get_recipe_info_url = "https://api.spoonacular.com/recipes/{id}/information?{apikey}".format(
                id=recipe.recipe_id, apikey=apikey4)

            response = requests.request(
                "GET", get_recipe_info_url, headers=self.headers, data=self.payload)
            results = response.json()
            # print(results)
            self.assertTrue(results["vegan"], "recipes are not vegan")

    def test_intolerances_requirements(self):
        """
        Test if the Recipes returned meet intolerance requirements
        """
        intolerances = ["gluten"]#, "dairy"]
        for intolerance in intolerances:
            print('------------')
            print(intolerance)
            print('------------')
            recipes = self.rr.search_recipes(intolerances=list(intolerance))
            for recipe in recipes:
                get_recipe_info_url = "https://api.spoonacular.com/recipes/{id}/information?{apikey}".format(
                    id=recipe.recipe_id, apikey=apikey4)
                response = requests.request(
                    "GET", get_recipe_info_url, headers=self.headers, data=self.payload)
                results = response.json()
                print('------------')
                print(results)
                print('------------')
                self.assertTrue(
                    results[intolerance+"Free"], "recipes are not {intolerance}Free".format(intolerance=intolerance))

        recipes = self.rr.search_recipes(intolerances=intolerances)
        for recipe in recipes:
            get_recipe_info_url = "https://api.spoonacular.com/recipes/{id}/information?{apikey}".format(
                id=recipe.recipe_id, apikey=apikey4)
            response = requests.request(
                "GET", get_recipe_info_url, headers=self.headers, data=self.payload)
            results = response.json()
            print(results)
            for intolerance in intolerances:
                self.assertTrue(
                    results[intolerance+"Free"], "recipes are not {intolerance}Free".format(intolerance=intolerance))


class TestRecipeToIngredients(unittest.TestCase):
    """
    This class is used to test the recipe_to_ingredients function raises proper expceptions
    """

    def test_invalid_recipe_id(self):
        """
            Test if invalidRecipeID is raised for invalid recipeID input
        """
        try:
            RecipeRecommender.recipe_to_ingredients("invalid_recipe_id")
        except InvalidRecipeID:
            pass
        except:
            self.fail("InvalidRecipeID exception was not thrown")

    # def test_apikey_out_of_points(self):
    #     """
    #         Test if ApikeyOutOfPoints is raised when apikey is out of points
    #     """
    #     try:
    #         RecipeRecommender.recipe_to_ingredients(641072)
    #     except ApikeyOutOfPoints:
    #         pass
    #     except:
    #         self.fail("ApikeyOutOfPoints exception was not thrown")


class TestGetRecipeInfo(unittest.TestCase):
    """
    This class is used to test the get_recipe_info function raises proper expceptions
    """

    def test_invalid_recipe_id(self):
        """
            Test if invalidRecipeID is raised for invalid recipeID input
        """
        try:
            RecipeRecommender.get_recipe_info("invalid_recipe_id")
        except InvalidRecipeID:
            pass
        except:
            self.fail("InvalidRecipeID exception was not thrown")

    # def test_apikey_out_of_points(self):
    #     """
    #         Test if ApikeyOutOfPoints is raised when apikey is out of points
    #     """
    #     try:
    #         RecipeRecommender.get_recipe_info(641072)
    #     except ApikeyOutOfPoints:
    #         pass
    #     except:
    #         self.fail("ApikeyOutOfPoints exception was not thrown")


if __name__ == '__main__':
    unittest.main()
