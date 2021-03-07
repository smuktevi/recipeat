from bs4 import BeautifulSoup
import re
import pandas as pd
import requests
import seaborn as sns
import matplotlib.pyplot as plt
import requests
from IPython.core.display import display, HTML
from .constants import *
import recipe_recommender

class Compare:
    def nutrient_compare(recipes): 
        """
        returns HTML response with a information on nutrients in given recipes

        Args:
            recipes: list of recipe objects

        Returns: list of HTML responses with nutrition information graphics   
        """
        nutr_html_list = []
        for recipe in recipes:
            url = "https://api.spoonacular.com/recipes/{id}/nutritionWidget?{apikey}&defaultCss=true".format(id=recipe.recipe_id,apikey=apikey6)    
            payload={}
            headers = {
                'Cookie': '__cfduid=d443da310537f29e03b78e744720641111613622052'
                    }  
            response = requests.request("GET", url, headers=headers, data=payload)
            nutr_html_list.append(HTML('<div class="header"><h1>{recipe_name}</h1></div>'.format(recipe_name=recipe.recipe_name) + response.text))
        return nutr_html_list

    def ingredient_compare(recipes):
        """
        returns HTML response with a information on ingredients in given recipes

        Args:
            recipes: list of recipe objects

        Returns: list of HTML responses with ingredient graphics   
        """
        ingrd_html_list = []
        for recipe in recipes: 
            url = "https://api.spoonacular.com/recipes/{id}/ingredientWidget?{apikey}&defaultCss=true".format(id=recipe.recipe_id,apikey=apikey6)    
            payload={}
            headers = {
                'Cookie': '__cfduid=d443da310537f29e03b78e744720641111613622052'
                    }  
            response = requests.request("GET", url, headers=headers, data=payload)   
            ingrd_html_list.append(HTML('<div class="header"><h1>{recipe_name}</h1></div>'.format(recipe_name=recipe.recipe_name) + response.text))
        return ingrd_html_list






