import requests
from .constants import *


class Compare:
    """
    Class that is used to compare recipes.
    """

    def nutrient_compare(self, recipes):
        """
        returns HTML response with a information on nutrients in given recipes

        Args:
            recipes: list of recipe objects

        Returns: list of HTML responses with nutrition information graphics
        """
        nutr_html_list = []
        for recipe in recipes:
            url = (
                "https://spoonacular-recipe-food-nutrition-"
                "v1.p.rapidapi.com/recipes/{id}"
                "/nutritionWidget?defaultCss=true"
            ).format(id=recipe.recipe_id)
            payload = {}
            headers = {
                "accept": "text/html",
                "x-rapidapi-key": "c65a4130b1msh767c11b9104ee56p1a93cdjsn9f1028eb2e98",
                "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
            }
            response = requests.request("GET", url,
                                        headers=headers, data=payload)
            # response.header["X-Ratelimit-Classifications-Limit: X"]
            # >= remaining
            # X-Ratelimit-Classifications-Limit: X
            # X-Ratelimit-Classifications-Remaining: X
            # X-Ratelimit-Requests-Limit: X
            # X-Ratelimit-Requests-Remaining: X
            # X-Ratelimit-Tinyrequests-Limit: X
            # X-Ratelimit-Tinyrequests-Remaining: X

            nutr_html_list.append(
                '<div class="header"><h3>{recipe_name}</h3></div>'.format(
                    recipe_name=recipe.recipe_name
                )
                + response.text
            )
        return nutr_html_list

    def ingredient_compare(self, recipes):
        """
        returns HTML response with a information
        on ingredients in given recipes

        Args:
            recipes: list of recipe objects

        Returns: list of HTML responses with ingredient graphics
        """
        ingrd_html_list = []
        for recipe in recipes:
            url = (
                "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
                "/recipes/{id}"
                "/ingredientWidget?defaultCss=true"
            ).format(id=recipe.recipe_id)
            payload = {}
            headers = {
                "accept": "text/html",
                "x-rapidapi-key": "c65a4130b1msh767c11b9104ee56p1a93cdjsn9f1028eb2e98",
                "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
            }
            response = requests.request("GET", url,
                                        headers=headers, data=payload)

            ingrd_html_list.append(
                '<div class="header"><h3>{recipe_name}</h3></div>'.format(
                    recipe_name=recipe.recipe_name
                )
                + response.text
            )
        return ingrd_html_list
