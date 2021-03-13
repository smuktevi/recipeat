# RecipEat
[![Build Status](https://api.travis-ci.com/smuktevi/recipeat.svg?branch=main)](https://travis-ci.com/github/smuktevi/recipeat)
[![codecov](https://codecov.io/gh/smuktevi/recipeat/branch/main/graph/badge.svg?token=PM8ZSJ7H0N)](https://codecov.io/gh/smuktevi/recipeat)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

test travis #4

**By: Corina Geier, Jeffery Lai, Edward Lou, Sai Muktevi, Andrew Zhou**

**Here's our Web App: [RecipEat!](https://recipeat-app.herokuapp.com/login)**

## Background
Figuring out what to eat based on the food you have in your fridge can be a difficult task for many. This task is made even harder when someone is trying to eat healthy. RecipEat aims to solve this problem by providing healthy recipes that can be made with the food someone has on hand. RecipEat works with a user’s dietary constraints and nutritional goals to provide recipe recommendations that are the most relevant to the user. RecipEat also allows for a visual comparison of recipes so that users can quickly decide which recipe they would rather make. 

## Modules

### bag_of_ingredients.py
A class that maintains a user's Bag of Ingredients. A user can:
* add ingredients to their bag.
* delete/update ingredients in their bag.

### recipe_recommender.py
A class that has methods to search for recipes with given inputs:
* Desired ingredients (i.e. chicken, potatoes, etc)
* Nutritional Requirements (i.e. calories, carbohydrates, proteins, and fats)
* Intolerances (i.e. dairy, egg, etc)
* Diet (i.e. Gluten Free, Ketogenic, etc)

### comparator.py
A class that has methods to visually compare nutrients and ingredients for selected recipes.
* the nutrient comparator shows a bargraph of different nutrional information amounts per each recipe
* the ingredient comparator shows pictures of the ingredients in a selected recipe

### database.py
A class that acts as a wrapper around psycopg2 to enable easier PostrgreSQL database access.
* interacts with the Bag of Ingredients to maintain user data in the backend.


## Project Data
### Spoonacular: 
Spoonacular is a Recipe-Food-Nutrition API providing access to over 365,000 recipes through ingredient- and nutrient-based queries. The user can also include keywords or phrases, such as ‘lactose intolerance’, to search for recipes that accommodate any special dietary restrictions or preferences. Additionally, the user can analyze nutritional information for each recipe by utilizing the visualization widgets.

## Testing

## Documentation

## Directory Structure
```bash
|-- app
|   |-- forms
|   |   |-- ingredients_form.py
|   |   |-- login_form.py
|   |   |-- recipe_form.py
|   |   `-- register_form.py
|   |-- static
|   |   `-- styles
|   |       `-- base.css
|   |-- templates
|   |   |-- base.html
|   |   |-- index.html
|   |   |-- ingredients.html
|   |   |-- login.html
|   |   |-- recipe.html
|   |   |-- register.html
|   |   `-- visual_comparator.html
|   |-- __init__.py
|   `-- routes.py
|-- commands
|   `-- create_table.py
|-- docs
|   |-- Component\ Specification.pdf
|   |-- Functional\ Specification.pdf
|   `-- Technology\ Review.pdf
|-- modules
|   |-- __init__.py
|   |-- bag_of_ingredients.py
|   |-- comparator.py
|   |-- constants.py
|   |-- database.py
|   |-- readme.txt
|   |-- recipe_recommender.py
|   `-- user.py
|-- tests
|   |-- __init__.py
|   |-- test_bag_of_ingredients.py
|   |-- test_comparator.py
|   |-- test_database.py
|   |-- test_recipe_recommender.py
|   `-- test_user.py
|-- Procfile
|-- README.md
|-- config.py
|-- github_commands.md
|-- recipeat.py
|-- requirements.txt
`-- wsgi.py
```


## Future Work

[More information about the project propsal here.](https://docs.google.com/document/d/1VCmc425JY53zHsUiasGh4CeFm5eu0YMbTKfwk1pRHZA/edit#heading=h.5x0d5h95i329) 

>Run the following code to install all the requuired packages/dependecies to run this application locally.

```
while read requirement; do pip install $requirement; done < requirements.txt
```

> Run the application using the following command line while in app.py directory.

```
flask run
```


