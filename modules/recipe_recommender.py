import requests
import pandas as pd
from .constants import constants

###########################################################################
# The RecipeRecommender class allows the user to interact with the
# Spoonacular API and get recipes that meet the given requirements.
###########################################################################

"""
search_response.request.body
search_response.json()["results"]
search_response.status_code
"""

class RecipeRecommender:
    def __init__(self, baseUrl:str = constants.api_base_url):
        self.baseUrl = baseUrl

    # revert back to original input
    def search_recipes(self, search_inputs_user:dict = {}):
        """
        Call Spoonacular API with given inputs and finds recipes that meet the requirements.

        param: self, ingredients, nutritional_req, diet, intolerances

        return: list[Recipe]
        """
        recipes = []

        search_url = "{baseUrl}/recipes/searchComplex".format(baseUrl=self.baseUrl)

        search_inputs = {
            "limitLicense":"true",
            "ranking":"0",
            "number":"5"}

        search_inputs.update(search_inputs_user)

        search_response = requests.get(search_url,params=search_inputs,headers=constants.api_request_headers)

        constants.check_api_errors(search_response)

        search_results = pd.DataFrame(search_response.json()["results"])

        get_bulk_recipe_info_url = "{baseUrl}/recipes/informationBulk".format(baseUrl=self.baseUrl)
        
        if not search_results.empty:
            search_results = search_results[["id", "image", "title"]]

            # builds url and calls Spoonacular to retrieve recipe source url
            get_bulk_recipe_info_url = 'https://api.spoonacular.com/recipes/informationBulk'
            recipe_id_url = 'ids=' + ','.join(str(id)
                                              for id in list(search_results["id"]))
            recipe_info_url = "{get_recipe}?{apikey}&{recipe_ids}".format(
                get_recipe=get_bulk_recipe_info_url,
                apikey=apikey4,
                recipe_ids=recipe_id_url)
            source_response = requests.request(
                "GET", recipe_info_url, headers=headers, data=payload)
            source_results = pd.DataFrame(source_response.json())[
                ["id", "sourceUrl"]]
            results = search_results.join(source_results.set_index(
                "id"), on="id", how='left', rsuffix='right')[["id", "title", "sourceUrl", "image"]]

            # builds list[Recipe] for the output
            for index, recipe in results.iterrows():
                recipes.append(Recipe(
                    recipe["id"],
                    recipe["title"],
                    recipe["sourceUrl"],
                    recipe["image"],
                    str(RecipeRecommender.get_recipe_info(recipe["id"])),
                    RecipeRecommender.recipe_to_ingredients(recipe["id"])))

        return recipes

    @staticmethod
    def recipe_to_ingredients(recipe_id):
        """
        Call Spoonacular API to retrieve ingredients required for the given recipe ID.

        param: recipe_id

        return: list[Ingredient]
        """
        ingredients = []

        # calls Spoonacular to pull ingredients for given recipe ID
        request_url = 'https://api.spoonacular.com/recipes/{}/ingredientWidget.json?'.format(
            recipe_id)
        url = request_url + apikey4
        payload = {}
        headers = {
            'Cookie': '__cfduid=dff952ebbf9c020c4f07c314e6bcb9c711613423774'
        }
        response = requests.request("GET", url, headers=headers, data=payload)

        check_api_errors(response)

        results = pd.json_normalize(response.json()["ingredients"])

        # builds list[Ingredient] for the output
        for index, ingredient in results.iterrows():
            ingredients.append(
                Ingredient(
                    ingredient_full=str(
                        ingredient['amount.metric.value']) +
                    " " +
                    ingredient["amount.metric.unit"] +
                    " " +
                    ingredient["name"],
                    ingredient_name=ingredient["name"],
                    amount=ingredient["amount.metric.value"],
                    units=ingredient["amount.metric.unit"]))

        return ingredients

    @staticmethod
    def get_recipe_info(recipe_id):
        """
        Call Spoonacular API to retrieve instructions to make recipe.

        param: recipe_id

        return: json
        """
        # calls Spoonacular to pull recipe directions
        request_url = 'https://api.spoonacular.com/recipes/{}/analyzedInstructions?'.format(
            recipe_id)
        url = request_url + apikey4
        payload = {}
        headers = {
            'Cookie': '__cfduid=dff952ebbf9c020c4f07c314e6bcb9c711613423774'
        }
        response = requests.request("GET", url, headers=headers, data=payload)

        check_api_errors(response)

        return response.json()

# if __name__ == '__main__':
#     #test code
#     nutrients = {
#     'minCarbs': 1,
#     'maxCarbs': 100,
#     'minProtein': 1,
#     'maxProtein': 100,
#     'minCalories': 100,
#     'maxCalories': 1000,
#     'minFat': 1,
#     'maxFat': 100
#     }
#     ingredients = ['chicken','potatoes']
#     diet = 'vegetarian'
#     intolerances='dairy'
#     rr = RecipeRecommender()
#     for recipe in rr.search_recipes(ingredients=ingredients, nutritional_req=nutrients):
#         print(recipe)

#     print(RecipeRecommender.search_recipes(ingredients,nutrients))
#     print(RecipeRecommender.get_recipe_info('fake'))

#     RecipeRecommender.recipe_to_ingredients(641072)
#     for ingredient in RecipeRecommender.recipe_to_ingredients(641072):
#         print(ingredient)
