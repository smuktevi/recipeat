import requests
from bs4 import BeautifulSoup


class Compare:
    """
    Class that is used to compare recipes.
    """

    @staticmethod
    def nutrient_compare(recipe_list):
        """
        returns HTML response with a information on nutrients in given recipes

        Args:
            recipe_list: list of recipe objects

        Returns: list of HTML responses with nutrition information graphics
        """
        nutr_html_list = []
        for recipe in recipe_list:
            url = (
                "https://spoonacular-recipe-food-nutrition-"
                "v1.p.rapidapi.com/recipes/{id}"
                "/nutritionWidget?defaultCss=true"
            ).format(id=recipe.recipe_id)
            payload = {}
            headers = {
                "accept": "text/html",
                "x-rapidapi-key": ("c65a4130b1msh767c11b9104"
                                   "ee56p1a93cdjsn9f1028eb2e98"),
                "x-rapidapi-host": ("spoonacular-recipe-food"
                                    "-nutrition-v1.p.rapidapi.com"),
            }
            response = requests.request("GET", url,
                                        headers=headers, data=payload)

            soup = BeautifulSoup(response.text, "html.parser")
            for div in soup.find_all("div", {'style': ('margin-top:3px;margin-'
                                                       'right:10px;text-align:'
                                                       'right;')}):
                div.decompose()

            nutr_html_list.append(
                '<div class="header"><h3>{recipe_name}</h3></div>'.format(
                    recipe_name=recipe.recipe_name
                ) + str(soup)
            )
        return nutr_html_list

    @staticmethod
    def ingredient_compare(recipe_list):
        """
        returns HTML response with a information
        on ingredients in given recipes

        Args:
            recipe_list: list of recipe objects

        Returns: list of HTML responses with ingredient graphics
        """
        ingrd_html_list = []
        for recipe in recipe_list:
            url = (
                "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
                "/recipes/{id}"
                "/ingredientWidget?defaultCss=true"
            ).format(id=recipe.recipe_id)
            payload = {}
            headers = {
                "accept": "text/html",
                "x-rapidapi-key": ("c65a4130b1msh767c11b9104"
                                   "ee56p1a93cdjsn9f1028eb2e98"),
                "x-rapidapi-host": ("spoonacular-recipe-food-"
                                    "nutrition-v1.p.rapidapi.com"),
            }
            response = requests.request("GET", url,
                                        headers=headers, data=payload)

            soup = BeautifulSoup(response.text, "html.parser")
            for div in soup.find_all("div", {'class': ('spoonacular-ingredient'
                                                       's-menu')}):
                div.decompose()
            for div in soup.find_all("div", {'style': ('margin-top:3px;margin-'
                                                       'right:10px;text-align:'
                                                       'right;')}):
                div.decompose()

            ingrd_html_list.append(
                '<div class="header"><h3>{recipe_name}</h3></div>'.format(
                    recipe_name=recipe.recipe_name
                ) + str(soup)
            )
        return ingrd_html_list
