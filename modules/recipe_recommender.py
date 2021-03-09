import requests
import pandas as pd
from .constants import *


class RecipeRecommender:
    def search_recipes(self, ingredients: list = [], nutritional_req: dict = {}, diet: str = "", intolerances: list = []):
        search_recipes_url = "https://api.spoonacular.com/recipes/complexSearch"
        result_option_url = 'instructionsRequired=true&ignorePantry=true&sort=min-missing-ingredients&number=2&limitLicense=true'
        preferences_url = 'diet={diet}&intolerances={intolerances}'.format(
            diet=diet, intolerances=','.join(intolerances))
        ingredients_url = 'includeIngredients=' + ','.join(ingredients)
        nutr_url = '&'.join("{!s}={!r}".format(key, val)
                            for (key, val) in nutritional_req.items())

        search_url = "{search}?{apikey}&{result_options}&{ingredients}&{nutrition}&{preferences}".format(
            search=search_recipes_url,
            apikey=apikey2,
            result_options=result_option_url,
            ingredients=ingredients_url,
            nutrition=nutr_url,
            preferences=preferences_url)

        payload = {}
        headers = {
            'Cookie': '__cfduid=d443da310537f29e03b78e744720641111613622052'
        }

        recipes = []

        search_response = requests.request(
            "GET", search_url, headers=headers, data=payload)
        # print(search_response.json())
        check_api_errors(search_response)
        search_results = pd.DataFrame(search_response.json()["results"])

        if not search_results.empty:
            search_results = search_results[["id", "image", "title"]]
            # print(search_results)
            get_bulk_recipe_info_url = 'https://api.spoonacular.com/recipes/informationBulk'
            recipe_id_url = 'ids=' + ','.join(str(id)
                                              for id in list(search_results["id"]))
            recipe_info_url = "{get_recipe}?{apikey}&{recipe_ids}".format(
                get_recipe=get_bulk_recipe_info_url,
                apikey=apikey2,
                recipe_ids=recipe_id_url)

            source_response = requests.request(
                "GET", recipe_info_url, headers=headers, data=payload)
            source_results = pd.DataFrame(source_response.json())[
                ["id", "sourceUrl"]]

            results = search_results.join(source_results.set_index(
                "id"), on="id", how='left', rsuffix='right')[["id", "title", "sourceUrl", "image"]]
            # print(results)
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
        request_url = 'https://api.spoonacular.com/recipes/{}/ingredientWidget.json?'.format(
            recipe_id)

        ingredients = []

        url = request_url + apikey2
        payload = {}
        headers = {
            'Cookie': '__cfduid=dff952ebbf9c020c4f07c314e6bcb9c711613423774'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        check_api_errors(response)

        results = pd.json_normalize(response.json()["ingredients"])

        for index, ingredient in results.iterrows():
            ingredients.append(Ingredient(ingredient_full=str(ingredient['amount.metric.value']) + " " + ingredient["amount.metric.unit"] + " " +
                                          ingredient["name"], ingredient_name=ingredient["name"], amount=ingredient["amount.metric.value"], units=ingredient["amount.metric.unit"]))

        return ingredients
        # return list of Ingredient

    @staticmethod
    def get_recipe_info(recipe_id):
        request_url = 'https://api.spoonacular.com/recipes/{}/analyzedInstructions?'.format(
            recipe_id)

        url = request_url + apikey2
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
