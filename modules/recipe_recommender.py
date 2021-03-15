import requests
import pandas as pd
import modules.constants as constants
import json

###########################################################################
# The RecipeRecommender class allows the user to interact with the
# Spoonacular API and get recipes that meet the given requirements.
###########################################################################


class RecipeRecommender:
    """
    The RecipeRecommender class allows the user to interact with the
    Spoonacular API and get recipes that meet the given requirements.
    """

    @staticmethod
    def search_recipes(
        ingredients: list = [],
        nutritional_req: dict = {},
        diet: str = "",
        intolerances: list = [],
    ):
        """
        Call Spoonacular API with given inputs and finds recipes that meet
        the requirements.

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
            search_url, params=search_params,
            headers=constants.api_request_headers)

        constants.check_api_errors(search_response)

        search_results = pd.DataFrame(search_response.json()["results"])

        if not search_results.empty:
            search_results = search_results[["id", "image", "title"]]
            get_bulk_recipe_info_url = ("{baseUrl}"
                                        "/recipes/informationBulk").format(
                baseUrl=constants.api_base_url)
            get_info_params = {'ids': ','.join(
                str(id) for id in list(search_results["id"]))}
            get_info_response = requests.get(
                url=get_bulk_recipe_info_url,
                params=get_info_params,
                headers=constants.api_request_headers)
            get_info_results = pd.DataFrame(get_info_response.json())[
                ["id", "sourceUrl"]]
            results = search_results.join(get_info_results.set_index(
                "id"), on="id", how='left', rsuffix='right')[
                    ["id", "title", "sourceUrl", "image"]]

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
        Call Spoonacular API to retrieve ingredients required for the
        given recipe ID.

        param: recipe_id

        return: list[Ingredient]
        """
        ingredients = []

        # calls Spoonacular to pull ingredients for given recipe ID
        get_ingredients_url = ("{baseUrl}"
                               "/recipes/{recipe_id}"
                               "/ingredientWidget.json").format(
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
                        ingredient['amount.metric.value']) + " "
                    + ingredient["amount.metric.unit"] + " "
                    + ingredient["name"],
                    ingredient_name=ingredient["name"],
                    amount=ingredient["amount.metric.value"],
                    units=ingredient["amount.metric.unit"]))

        return ingredients

    @ staticmethod
    def get_recipe_info(recipe_id):
        """
        Call Spoonacular API to retrieve instructions to make recipe.

        param: recipe_id

        return: json
        """
        # calls Spoonacular to pull recipe directions
        get_recipe_info_url = ("{baseUrl}"
                               "/recipes/{recipe_id}"
                               "/information").format(
            baseUrl=constants.api_base_url, recipe_id=recipe_id)

        get_recipe_info_response = requests.get(
            url=get_recipe_info_url, headers=constants.api_request_headers)

        constants.check_api_errors(get_recipe_info_response)

        return get_recipe_info_response

def to_json(recipe_list):
    """
    Function used to serialize a list of recipes.

    :param recipe_list: list(Recipe). list of recipes
    :return: json. A json dictionary to be serialized.
    """
    return json.dumps(recipe_list, default=lambda o: o.__dict__,
                    sort_keys=True, indent=4)

def from_json(json_list):
    """
    Function used to convert a serialized dictionary back to a list of recipes.

    :param json_list: json. A json dictionary.
    :return: list(Recipe). List of recipes constructed back
    """
    json_list = json.loads(json_list)
    recipe_list = []
    for recipe_dictionary in json_list:
        recipe_id = recipe_dictionary['recipe_id']
        recipe_name = recipe_dictionary['recipe_name']
        recipe_source_url = recipe_dictionary['source_url']
        recipe_img_url = recipe_dictionary['img_url']
        recipe_description = recipe_dictionary['description']
        ingredient_list = []
        for ingredient in recipe_dictionary['ingredients']:
            ingredient_full_name = ingredient['ingredient_full']
            ingredient_name = ingredient['ingredient']
            ingredient_amount = ingredient['amount']
            ingredient_unit = ingredient['units']
            new_ingredient = Ingredient(ingredient_full=ingredient_full_name,
                                        ingredient_name=ingredient_name,
                                        amount=ingredient_amount,
                                        units=ingredient_unit)
            ingredient_list.append(new_ingredient)
        new_recipe = Recipe(recipe_id=recipe_id, recipe_name=recipe_name,
                            source_url=recipe_source_url,
                            img_url=recipe_img_url,
                            description=recipe_description,
                            ingredients=ingredient_list)
        recipe_list.append(new_recipe)
    return recipe_list

# def reconstruct_recipe_list(recipe_dictionary_list):
#     """
#     This is a helper function used to reconstruct Recipe and Ingredient objects
#     back into their original form from a dictionary.

#     :param recipe_dictionary_list: dict. A serialized dictionary.
#     :return: list(Recipe). List of recipes constructed from the dictionary.
#     """
#     recipe_list = []
#     for recipe_dictionary in recipe_dictionary_list:
#         recipe_id = recipe_dictionary['recipe_id']
#         recipe_name = recipe_dictionary['recipe_name']
#         recipe_source_url = recipe_dictionary['source_url']
#         recipe_img_url = recipe_dictionary['img_url']
#         recipe_description = recipe_dictionary['description']
#         ingredient_list = []
#         for ingredient in recipe_dictionary['ingredients']:
#             ingredient_full_name = ingredient['ingredient_full']
#             ingredient_name = ingredient['ingredient']
#             ingredient_amount = ingredient['amount']
#             ingredient_unit = ingredient['units']
#             new_ingredient = Ingredient(ingredient_full=ingredient_full_name,
#                                         ingredient_name=ingredient_name,
#                                         amount=ingredient_amount,
#                                         units=ingredient_unit)
#             ingredient_list.append(new_ingredient)
#         new_recipe = Recipe(recipe_id=recipe_id, recipe_name=recipe_name,
#                             source_url=recipe_source_url,
#                             img_url=recipe_img_url,
#                             description=recipe_description,
#                             ingredients=ingredient_list)
#         recipe_list.append(new_recipe)
#     return recipe_list
