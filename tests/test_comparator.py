from bs4 import BeautifulSoup
from modules.comparator import *
from modules.recipe_recommender import *
import unittest
import pandas as pd


class TestComparator(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestComparator, self).__init__(*args, **kwargs)
        self.recipe_list, self.cp = [], None
        self.generate_stubs()

    def generate_stubs(self):
        self.cp = Compare()
        self.recipe_list = [
            Recipe(
                recipe_id=631763,
                recipe_name="Warm and Luscious Sipping Chocolate",
                img_url="https://spoonacular.com/recipeImages/631763-312x231.jpg",
                ingredients=[
                    Ingredient(ingredient_name="salt", amount=2),
                    Ingredient(ingredient_name="potato", amount=3, units="gram"),
                ],
                source_url="https://spoonacular.com/recipes/warm-and-luscious-sipping-chocolate-with-xocai-healthy-dark-sipping-xocolate-631763",
            ),
            Recipe(
                recipe_id=632944,
                recipe_name="Asparagus Soup",
                img_url="https://spoonacular.com/recipeImages/632944-312x231.jpg",
                ingredients=[
                    Ingredient(ingredient_name="not salt", amount=99),
                    Ingredient(
                        ingredient_name="not potato", amount=999, units="grammys"
                    ),
                ],
                source_url="https://www.onceuponachef.com/recipes/asparagus-soup-with-lemon-and-parmesan.html",
            ),
        ]

    def test_output_length(self):
        """
        tests HTML output list is the correct length for both nutrient_compare
        and ingredient_compare
        """
        self.assertEqual(len(self.recipe_list), len(self.cp.nutrient_compare(self.recipe_list)))
        self.assertEqual(len(self.recipe_list), len(self.cp.ingredient_compare(self.recipe_list)))

    def test_html_nutrient(self):
        """
        tests that the HTML format is correct HTML format
        for nutrient_compare output

        Returns:
        """
        
        HTML_list = self.cp.nutrient_compare(self.recipe_list)
        self.assertTrue(
            all(bool(BeautifulSoup(html, "html.parser").find()) for html in HTML_list)
        )

    def test_html_ingredients(self):
        """
        tests that the HTML format is correct HTML format
        for ingredrient_compare output

        Returns:
        """
        HTML_list = self.cp.ingredient_compare(self.recipe_list)
        self.assertTrue(
            all(bool(BeautifulSoup(html, "html.parser").find()) for html in HTML_list)
        )
