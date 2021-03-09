import unittest
import requests
import pandas as pd
from modules.constants import *
from modules.recipe_recommender import *


class TestSearchRecipes(unittest.TestCase):
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
                id=recipe.recipe_id, apikey=apikey1)

            response = requests.request(
                "GET", get_nutrition_url, headers=headers, data=payload)
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

    # test if recipes returned include at least one of the input ingredients
    def test_ingredient_requirements(self):
        ingredients = ["chicken", "potato"]
        rr = RecipeRecommender()
        recipes = rr.search_recipes(ingredients=ingredients)
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

    # test if the recipes returned meet diet requirements
    def test_diet_requirements(self):
        diets = ["glutenFree", "vegetarian", "vegan"]

        payload = {}
        headers = {
            'Cookie': '__cfduid=d443da310537f29e03b78e744720641111613622052'
        }
        rr = RecipeRecommender()
        for diet in diets:
            # print(diet)
            recipes = rr.search_recipes(diet=diet)
            for recipe in recipes:
                get_recipe_info_url = "https://api.spoonacular.com/recipes/{id}/information?{apikey}".format(
                    id=recipe.recipe_id, apikey=apikey1)
                response = requests.request(
                    "GET", get_recipe_info_url, headers=headers, data=payload)
                results = response.json()
                # print(results)
                self.assertTrue(
                    results[diet], "recipes are not {diet}".format(diet=diet))

        # test gluten-free
        rr_gf = RecipeRecommender()
        recipes_gf = rr_gf.search_recipes(diet=diets[0])

        for recipe in recipes_gf:
            get_recipe_info_url = "https://api.spoonacular.com/recipes/{id}/information?{apikey}".format(
                id=recipe.recipe_id, apikey=apikey1)

            response = requests.request(
                "GET", get_recipe_info_url, headers=headers, data=payload)
            results = response.json()
            self.assertTrue(results["glutenFree"],
                            "recipes are not gluten free")

        # test vegetarian
        rr_veg = RecipeRecommender()
        recipes_veg = rr_veg.search_recipes(diet=diets[1])

        for recipe in recipes_veg:
            get_recipe_info_url = "https://api.spoonacular.com/recipes/{id}/information?{apikey}".format(
                id=recipe.recipe_id, apikey=apikey1)

            response = requests.request(
                "GET", get_recipe_info_url, headers=headers, data=payload)
            results = response.json()
            self.assertTrue(results["vegetarian"],
                            "recipes are not vegetarian")

        # test vegan
        rr_vegan = RecipeRecommender()
        recipes_vegan = rr_vegan.search_recipes(diet=diets[2])

        for recipe in recipes_vegan:
            get_recipe_info_url = "https://api.spoonacular.com/recipes/{id}/information?{apikey}".format(
                id=recipe.recipe_id, apikey=apikey1)

            response = requests.request(
                "GET", get_recipe_info_url, headers=headers, data=payload)
            results = response.json()
            # print(results)
            self.assertTrue(results["vegan"], "recipes are not vegan")

    # test if the recipes returned meet intolerance requirements
    def test_intolerances_requirements(self):
        intolerances = ["dairy", "gluten"]
        payload = {}
        headers = {
            'Cookie': '__cfduid=d443da310537f29e03b78e744720641111613622052'
        }
        rr = RecipeRecommender()
        for intolerance in intolerances:
            # print(diet)
            recipes = rr.search_recipes(intolerances=intolerance)
            for recipe in recipes:
                get_recipe_info_url = "https://api.spoonacular.com/recipes/{id}/information?{apikey}".format(
                    id=recipe.recipe_id, apikey=apikey1)
                response = requests.request(
                    "GET", get_recipe_info_url, headers=headers, data=payload)
                results = response.json()
                # print(results)
                self.assertTrue(
                    results[intolerance+"Free"], "recipes are not {intolerance}Free".format(intolerance=intolerance))

        intolerances = ["gluten", "dairy"]
        recipes = rr.search_recipes(intolerances=intolerances)
        for recipe in recipes:
            get_recipe_info_url = "https://api.spoonacular.com/recipes/{id}/information?{apikey}".format(
                id=recipe.recipe_id, apikey=apikey1)
            response = requests.request(
                "GET", get_recipe_info_url, headers=headers, data=payload)
            results = response.json()
            # print(results)
            for intolerance in intolerances:
                self.assertTrue(
                    results[intolerance+"Free"], "recipes are not {intolerance}Free".format(intolerance=intolerance))


class TestRecipeToIngredients(unittest.TestCase):
    # test if recipe is valid/raises appropriate exception with recipe_id is not valid
    def test_invalid_recipe_id(self):
        try:
            RecipeRecommender.recipe_to_ingredients("invalid_recipe_id")
        except InvalidRecipeID:
            pass
        except:
            self.fail("InvalidRecipeID exception was not thrown")

    # # test is apikey is out of points for the day
    # def test_apikey_out_of_points(self):
    #     try:
    #         RecipeRecommender.recipe_to_ingredients(641072)
    #     except ApikeyOutOfPoints:
    #         pass
    #     except:
    #         self.fail("ApikeyOutOfPoints exception was not thrown")


class TestGetRecipeInfo(unittest.TestCase):
    # test if recipe is valid/raises appropriate exception with recipe_id is not valid
    def test_invalid_recipe_id(self):
        try:
            RecipeRecommender.get_recipe_info("invalid_recipe_id")
        except InvalidRecipeID:
            pass
        except:
            self.fail("InvalidRecipeID exception was not thrown")

    # # test is apikey is out of points for the day
    # def test_apikey_out_of_points(self):
    #     try:
    #         RecipeRecommender.get_recipe_info(641072)
    #     except ApikeyOutOfPoints:
    #         pass
    #     except:
    #         self.fail("ApikeyOutOfPoints exception was not thrown")


if __name__ == '__main__':
    unittest.main()
