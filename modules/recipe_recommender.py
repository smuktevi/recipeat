import requests
import pandas as pd

class RecipeRecommender:
    def search_recipes(ingredients: list, nutritional_req: dict):
        base_url = 'https://api.spoonacular.com/'
        search_url = 'recipes/complexSearch?'
        get_info_url = 'recipes/informationBulk?'
        apiKey = 'apiKey=f25da678f94b474ba41918b8da3f390f&'
        result_option_url = 'instructionsRequired=true&ignorePantry=true&sort=min-missing-ingredients&sortDirection=asc&number=15&limitLicense=true&'
        ingredient_url = 'includeIngredients=' + ','.join(ingredients) + '&'
        nutr_url = '&'.join("{!s}={!r}".format(key,val) for (key,val) in nutritional_req.items())

        search_url = base_url + search_url + apiKey + result_option_url + ingredient_url + nutr_url
        payload={}
        headers = {
            'Cookie': '__cfduid=d443da310537f29e03b78e744720641111613622052'
        }

        search_response = requests.request("GET", search_url, headers=headers, data=payload)
        search_results = pd.DataFrame(search_response.json()["results"])[["id","image"]] #add recipe link and reamining bag items

        recipe_id_url = 'ids=' + ','.join(str(id) for id in list(search_results["id"]))
        recipe_info_url = base_url + get_info_url + apiKey + recipe_id_url
        source_response = requests.request("GET", recipe_info_url, headers=headers, data=payload)
        source_results = pd.DataFrame(source_response.json())[["id", "sourceUrl"]]

        results = search_results.join(source_results.set_index("id"), on="id", how='left', rsuffix='right')[["id", "sourceUrl", "image"]]
        return results

    def recipe_to_ingredients(recipe_id):
        request_url = 'https://api.spoonacular.com/recipes/{}/ingredientWidget.json?'.format(recipe_id)
        apikey = 'apiKey=4078ba908cf14212b9c3754a84a262f5'
        filterby = ''


        url = request_url + apikey + filterby
        payload={}
        headers = {
            'Cookie': '__cfduid=dff952ebbf9c020c4f07c314e6bcb9c711613423774'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        return pd.json_normalize(response.json()['ingredients'])

    def get_recipe_info (recipe_id):
        request_url = 'https://api.spoonacular.com/recipes/{}/analyzedInstructions?'.format(recipe_id)
        apikey = 'apiKey=4078ba908cf14212b9c3754a84a262f5'
        filterby = ''


        url = request_url + apikey + filterby
        payload={}
        headers = {
            'Cookie': '__cfduid=dff952ebbf9c020c4f07c314e6bcb9c711613423774'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()

if __name__ == '__main__':
    #test code
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
    ingredients = ['potatoes', 'chicken']
    print(RecipeRecommender.search_recipes(ingredients,nutrients))