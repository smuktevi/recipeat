import requests
import pandas as pd
import modules.constants as constants

###########################################################################
# The RecipeRecommender class allows the user to interact with the
# Spoonacular API and get recipes that meet the given requirements.
###########################################################################


class RecipeRecommender:

    @staticmethod
    def search_recipes(
        ingredients: list = [],
        nutritional_req: dict = {},
        diet: str = "",
        intolerances: list = [],
    ):
        """
        Call Spoonacular API with given inputs and finds recipes that meet the requirements.

        param: self, ingredients, nutritional_req, diet, intolerances

        return: list[Recipe]
        """
        recipes = []

        search_url = "{baseUrl}/recipes/complexSearch".format(
            baseUrl=constants.api_base_url)

        search_params = {
            "limitLicense": "true",
            "ranking": "0",
            "number": "5"}
        search_params.update(nutritional_req)
        if not ingredients == []:
            search_params["includeIngredients"] = ",".join(ingredients)
        if not diet == "":
            search_params["diet"] = diet
        if not intolerances == []:
            search_params["intolerances"] = ",".join(intolerances)

        search_response = requests.get(
            search_url, params=search_params, headers=constants.api_request_headers)

        # constants.check_api_errors(search_response)

        search_results = pd.DataFrame(search_response.json()["results"])

        if not search_results.empty:
            search_results = search_results[["id", "image", "title"]]
            get_bulk_recipe_info_url = "{baseUrl}/recipes/informationBulk".format(
                baseUrl=constants.api_base_url)
            get_info_params = {'ids': ','.join(
                str(id) for id in list(search_results["id"]))}
            get_info_response = requests.get(
                url=get_bulk_recipe_info_url, params=get_info_params, headers=constants.api_request_headers)
            get_info_results = pd.DataFrame(get_info_response.json())[
                ["id", "sourceUrl"]]
            results = search_results.join(get_info_results.set_index(
                "id"), on="id", how='left', rsuffix='right')[["id", "title", "sourceUrl", "image"]]

            # builds list[Recipe] for the output
            for index, recipe in results.iterrows():
                recipes.append(
                    constants.Recipe(
                        recipe["id"],
                        recipe["title"],
                        recipe["sourceUrl"],
                        recipe["image"],
                        str(RecipeRecommender.get_recipe_info(recipe["id"])),
                        RecipeRecommender.recipe_to_ingredients(recipe["id"]),
                    )
                )
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
        get_ingredients_url = "{baseUrl}/recipes/{recipe_id}/ingredientWidget.json".format(
            baseUrl=constants.api_base_url, recipe_id=recipe_id)

        get_ingredients_response = requests.get(
            url=get_ingredients_url, headers=constants.api_request_headers)

        constants.check_api_errors(get_ingredients_response)

        get_ingredient_results = pd.json_normalize(
            get_ingredients_response.json()["ingredients"])

        # builds list[Ingredient] for the output
        for index, ingredient in get_ingredient_results.iterrows():
            ingredients.append(
                constants.Ingredient(
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
        get_recipe_info_url = "{baseUrl}/recipes/{recipe_id}/information".format(
            baseUrl=constants.api_base_url, recipe_id=recipe_id)

        get_recipe_info_response = requests.get(
            url=get_recipe_info_url, headers=constants.api_request_headers)

        constants.check_api_errors(get_recipe_info_response)

        return get_recipe_info_response



# if __name__ == '__main__':
#     # test code
#     nutrients = {
#         'minCarbs': '1',
#         'maxCarbs': '100',
#         'minProtein': '1',
#         'maxProtein': '100',
#         'minCalories': '100',
#         'maxCalories': '1000',
#         'minFat': '1',
#         'maxFat': '100'
#     }
#     ingredients = ['chicken', 'potatoes']
#     diet = 'vegetarian'
#     intolerances = 'dairy'
#     rr = RecipeRecommender()
#     # response = rr.search_recipes(ingredients=ingredients, nutritional_req=nutrients)
#     # print(response.json())
#     for recipe in rr.search_recipes(diet=diet, intolerances=intolerances):
#         print(recipe)

    #     print(RecipeRecommender.search_recipes(ingredients,nutrients))
    # print(RecipeRecommender.get_recipe_info('fake').status_code)
    # print(RecipeRecommender.get_recipe_info(641072))

    # RecipeRecommender.recipe_to_ingredients(641072)
    # for ingredient in RecipeRecommender.recipe_to_ingredients(641072):
    #     print(ingredient)
