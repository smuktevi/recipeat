import unittest
from unittest import mock
import pytest
from modules.constants import check_api_errors, Ingredient, Recipe, ApikeyOutOfPoints
import json
import requests


class TestConstantObjects(unittest.TestCase):
    """
    Testing objects and their methods from constants file.
    """

    def test_check_api_errors(self):
        """
        Testing if the API is out of points. Should raise Exception.
        """

        class MockResponse:
            def __init__(self, json_data, status_code):
                self.headers = json_data
                self.status_code = status_code

        mock_response = MockResponse(
            {
                "X-RateLimit-requests-Remaining": 50,
                "X-RateLimit-results-Remaining": 50,
                "X-RateLimit-tinyrequests-Remaining": 50,
            },
            200,
        )
        self.assertRaises(ApikeyOutOfPoints, check_api_errors, mock_response)

    def test_ingredient_parse_string_2_words(self):
        """
        Test for success of parsing Ingredient string with 2 word input.
        """
        ingredient_full = "2  chicken"
        output = Ingredient.parse_string(ingredient_full)
        self.assertIsInstance(output, Ingredient)

    def test_ingredient_parse_string_3_words(self):
        """
        Test for success of parsing Ingredient string with 3 word input.
        """
        ingredient_full = "2 g chicken"
        output = Ingredient.parse_string(ingredient_full)
        self.assertIsInstance(output, Ingredient)

    def test_output_is_string(self):
        """
        Testing if output is string for object to_string methods.
        """

        # Checking for Ingredient object.
        ingredient = Ingredient(
            ingredient_full="1 cup green tea",
            ingredient_name="green tea",
            amount=1,
            units="cup",
        )
        self.assertIsInstance(ingredient.__str__(), str)
        self.assertIsInstance(ingredient.__repr__(), str)

        # Checking for Recipe object.
        recipe = Recipe(
            recipe_id=631763,
            recipe_name="Warm and Luscious Sipping Chocolate",
            img_url=("https://spoonacular.com/recipeImages" "/631763-312x231.jpg"),
            ingredients=[
                Ingredient(ingredient_name="salt", amount=2),
                Ingredient(ingredient_name="potato", amount=3, units="gram"),
            ],
            source_url=(
                "https://spoonacular.com/recipes/warm-and-luscious"
                "-sipping-chocolate-with-xocai-healthy-dark-sippin"
                "g-xocolate-631763"
            ),
        )
        self.assertIsInstance(recipe.__str__(), str)
