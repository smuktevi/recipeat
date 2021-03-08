import .comparator as cp
import unittest
import pandas as pd


class testComparator(unittest.TestCase):
    def test_output_length(self):
        """
        tests HTML output list is the correct length for both nutrient_compare
        and ingredient_compare
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
        ingredients = ['chicken', 'potatoes']
        recipe_list = RecipeRecommender.search_recipes(ingredients=ingredients, nutritional_req=nutrients)
        self.assertEqual(len(recipe_list), len(cp.nutrient_compare(recipe_list)))
        self.assertEqual(len(recipe_list), len(cp.ingredient_compare(recipe_list)))

    def test_html_nutrient(self):
        """
        tests that the HTML format is correct HTML format for nutrient_compare output

        Returns:
        """
        #self.assertTrue( )

    def test_html_ingredients(self):
        """
        tests that the HTML format is correct HTML format for ingredrient_compare output

        Returns:
        """
