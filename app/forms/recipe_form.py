from flask_wtf import FlaskForm
from wtforms import *


class RecipeForm(FlaskForm):
    """
    Recipe form class. Sets up all the required form widgets for recipe
    recommender here.
    """
    min_carb = IntegerField('Minimum Carbohydrates')
    max_carb = IntegerField('Maximum Carbohydrates')

    min_fat = IntegerField('Minimum Fat')
    max_fat = IntegerField('Maximum Fat')

    min_cal = IntegerField('Minimum Calories')
    max_cal = IntegerField('Maximum Calories')

    min_protein = IntegerField('Minimum Protein')
    max_protein = IntegerField('Maximum Protein')

    intolerance_options = [('Dairy', 'Dairy'), ('Egg', 'Egg'),
                           ('Gluten', 'Gluten'), ('Grain', 'Grain'),
                           ('Peanut', 'Peanut'), ('Seafood', 'Seafood'),
                           ('Sesame', 'Sesame'), ('Shellfish', 'Shellfish'),
                           ('Soy', 'Soy'), ('Sulfite', 'Sulfite'),
                           ('Tree Nut', 'Tree Nut'), ('Wheat', 'Wheat')]
    intolerances = SelectMultipleField('Intolerances',
                                       choices=intolerance_options)

    diet_options = [('Gluten Free', 'Gluten Free'), ('Ketogenic', 'Ketogenic'),
                    ('Vegetarian', 'Vegetarian'),
                    ('Lacto-Vegetarian', 'Lacto-Vegetarian'),
                    ('Ovo-Vegetarian', 'Ovo-Vegetarian'), ('Vegan', 'Vegan'),
                    ('Pescetarian', 'Pescetarian'), ('Paleo', 'Paleo'),
                    ('Primal', 'Primal'), ('Whole30', 'Whole30')]
    diets = SelectMultipleField('Diets', choices=diet_options)

    ingredients = SelectMultipleField('Ingredients')

    submit = SubmitField('Search Recipes')

    compare_submit = SubmitField('Compare Recipes')
