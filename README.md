# RecipEat
[![Build Status](https://api.travis-ci.com/smuktevi/recipeat.svg?branch=main)](https://travis-ci.com/github/smuktevi/recipeat)
[![codecov](https://codecov.io/gh/smuktevi/recipeat/branch/main/graph/badge.svg?token=PM8ZSJ7H0N)](https://codecov.io/gh/smuktevi/recipeat)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**By: Corina Geier, Jeffery Lai, Edward Lou, Sai Muktevi, Andrew Zhou**

**Here's our Web App: [RecipEat!](https://recipeat-app.herokuapp.com/login)**

## Installation and Setup

**Quick Info**

* Testing was implemented mainly on our 'modules' folder where we have all of our back-end source code. 
* For testing we excluded files from our 'app' folder as it consisted mainly of HTML templates. We did not implement testing on routes.py.
* We have achieved a 100% coverage using unit tests for all our back-end python files. This can be seen in our coverage reports and Codecov.
* You may choose to run the app locally or via the website link.

**Installation Tutorial**  
This tutorial will allow you to run the code locally on your own machine!
1) Clone the git repository to your local machine and change directory to recipeat
```
git clone https://github.com/smuktevi/recipeat.git
cd recipeat
```
2) Install required packages and dependecies:
```
pip install -e .
```
3) You're ready to start running our app locally!  

* Use flask run to run our web app locally!
```
flask run
```
* Check the code for flake8 standards!
```
flake8 --ignore=E722,W503 --exclude=app/__init__.py
```
* Run the implemented unit tests!
```
pytest --cov=modules --cov-config=.coveragerc
```

## Background
Figuring out what to eat based on the food you have in your fridge can be a difficult task for many. This task is made even harder when someone is trying to eat healthy. RecipEat aims to solve this problem by providing healthy recipes that can be made with the food someone has on hand. RecipEat works with a user’s dietary constraints and nutritional goals to provide recipe recommendations that are the most relevant to the user. RecipEat also allows for a visual comparison of recipes so that users can quickly decide which recipe they would rather make. 

## Modules

### user.py
A class that maintains a user's information and session. Has methods to:
* Register a new user
* Login an existing user
* Delete an existing user

### bag_of_ingredients.py
A class that maintains a user's Bag of Ingredients. A user can:
* Add ingredients to their bag.
* Delete/update ingredients in their bag.

### recipe_recommender.py
A class that has methods to search for recipes with given inputs:
* Desired ingredients (i.e. chicken, potatoes, etc)
* Nutritional Requirements (i.e. calories, carbohydrates, proteins, and fats)
* Intolerances (i.e. dairy, egg, etc)
* Diet (i.e. Gluten Free, Ketogenic, etc)

### comparator.py
A class that has methods to visually compare nutrients and ingredients for selected recipes.
* The nutrient comparator shows a bargraph of different nutrional information amounts per each recipe
* The ingredient comparator shows pictures of the ingredients in a selected recipe

### database.py
A class that acts as a wrapper around psycopg2 to enable easier PostrgreSQL database access.
* Interacts with the Bag of Ingredients to maintain user data in the backend.


## Project Data
### Spoonacular: 
Spoonacular is a Recipe-Food-Nutrition API providing access to over 365,000 recipes through ingredient- and nutrient-based queries. The user can also include keywords or phrases, such as ‘lactose intolerance’, to search for recipes that accommodate any special dietary restrictions or preferences. Additionally, the user can analyze nutritional information for each recipe by utilizing the visualization widgets.

## PEP 8
This code follows standards set by Flake-8. The code ignores Flake-8 errors: E722 and W503. E722 does not allow the use of bare 'except'. The code for registering and logging in users requires the use of a bare 'except', and therefore E722 has been ignored. W503 does not allow line break before binary operators. This warning is ignored as it contradicts with W504, which does not allow line break after binary operators. The code follows W504 standards, and therefore W503 is ignored. Flake-8 also ignores one file: app/__init__.py. The import statement in app/__init__.py is required be on the bottom of the file to work for flask, and therefore this file is ignored.

The command used to check flake-8:
```
flake8 --ignore=E722,W503 --exclude=app/__init__.py
```

## Testing
The code that is tested in this project are in the modules folder. Unit tests are used to test the code in the modules. The unit tests must be run in a specific order, and since pytest test order is used to ensure proper unit test order; it is necessary to run the unit tests using pytest. Pytest also allows checking for unit test coverage.

For Coverage, only the modules folder is tested, as functionality is all in the modules. The app folder is not tested as the code is for the UI of the webpage. Inside the modules folder, constants.py is ignored. constants.py does not have any functional code and only variables with fixed constant values, and therefore is not tested.

The command used to run the unit tests:
```
pytest --cov=modules --cov-config=.coveragerc
```

## Documentation
[Component Specification](https://github.com/smuktevi/recipeat/blob/main/docs/Component%20Specification.pdf)  
[Functional Specification](https://github.com/smuktevi/recipeat/blob/main/docs/Component%20Specification.pdf)  

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


