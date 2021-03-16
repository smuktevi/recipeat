# RecipEat
[![Build Status](https://api.travis-ci.com/smuktevi/recipeat.svg?branch=main)](https://travis-ci.com/github/smuktevi/recipeat)
[![codecov](https://codecov.io/gh/smuktevi/recipeat/branch/main/graph/badge.svg?token=PM8ZSJ7H0N)](https://codecov.io/gh/smuktevi/recipeat)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**By: Corina Geier, Jeffery Lai, Edward Lou, Sai Muktevi, Andrew Zhou**

Figuring out what to eat based on the food you have in your fridge can be a difficult task for many. This task is made even harder when someone is trying to eat healthy. RecipEat aims to solve this problem by providing quick healthy recipes that can be made with the food someone has on hand. RecipEat works with a user’s dietary constraints and nutritional goals to provide recipe recommendations that are the most relevant to the user. RecipEat also allows for a visual comparison of the nutritional information and ingredients in recipes so that users can quickly decide which recipe they would rather make.  
**Here's our Web App: [RecipEat!](https://recipeat-app.herokuapp.com/)**

## Installation and Setup

**<ins>Quick Info</ins>**  

* Testing was implemented mainly on our 'modules' folder where we have all of our back-end source code. 
* For testing we excluded files from our 'app' folder as it consisted mainly of HTML templates. We did not implement testing on routes.py.
* We have achieved a 100% coverage using unit tests for all our back-end python files. This can be seen in our coverage reports and Codecov.
* You may choose to run the app locally or via the website link.

**<ins>Installation</ins>**  

This tutorial will allow you to run the code locally on your own machine!  
*It is recommended that you create a new conda environment (if you have conda) or a new virtual environment before installation.*

1) Clone the git repository to your local machine and change directory to recipeat
```
git clone https://github.com/smuktevi/recipeat.git
cd recipeat
```
2) Install required packages and dependecies. This installs from our `setup.py` file.
```
pip install -e .
```
3) You're ready to start running our app locally!  

* Use flask run to run our web app locally.
```
flask run
```
* Check the code for flake8 standards!
```
flake8 --ignore=W503 --exclude=app/__init__.py
```
* Run the implemented unit tests!
```
pytest --cov=modules
```
* You may also use the following code to check code coverage in the form of HTML pages.
```
pytest --cov-report html
```
These reports can be found in the `miscellaneous/htmlcov` directory.

## Documentation
**<ins>Documents</ins>**

For more information on the Software Engineering and Design behind our project please refer to these links:
* [Component Specification](https://github.com/smuktevi/recipeat/blob/main/docs/Component%20Specification.pdf)  
* [Functional Specification](https://github.com/smuktevi/recipeat/blob/main/docs/Component%20Specification.pdf)
* [Technology Review on Spoonacular](https://github.com/smuktevi/recipeat/blob/main/docs/Technology%20Review.pdf)

**<ins>Web Demo</ins>**

A demo of the usage of the application in video format can be downloaded from the [examples folder](https://github.com/smuktevi/recipeat/tree/main/examples).
This folder also contains a quick 9 minute video recording of our Final Presentation for a better understanding of our project outline, uses cases, software architecture, design, challenges faced, future work, etc.




## Directory Structure
```bash
.
|-- app
|   |-- forms
|   |   |-- ingredients_form.py
|   |   |-- login_form.py
|   |   |-- recipe_form.py
|   |   `-- register_form.py
|   |-- static
|   |   |-- assets
|   |   `-- styles
|   |       `-- base.css
|   |-- templates
|   |   |-- base.html
|   |   |-- index.html
|   |   |-- ingredients.html
|   |   |-- login.html
|   |   |-- logout.html
|   |   |-- recipe.html
|   |   |-- register.html
|   |   `-- visual_comparator.html
|   |-- __init__.py
|   `-- routes.py
|-- docs
|   |-- Component\ Specification.pdf
|   |-- Functional\ Specification.pdf
|   `-- Technology\ Review.pdf
|-- examples
|   `-- Web\ App\ Demo.mp4
|-- miscellaneous
|   `-- commands
|       |-- command.py
|       `-- create_table.py
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
|   |-- test_constants.py
|   |-- test_database.py
|   |-- test_recipe_recommender.py
|   `-- test_user.py
|-- LICENSE
|-- Procfile
|-- README.md
|-- config.py
|-- requirements.txt
|-- setup.py
`-- wsgi.py

12 directories, 43 files
```

## Modules

### `user.py`
A class that maintains a user's information and session. Has methods to:
* Register a new user
* Login an existing user
* Delete an existing user

### `bag_of_ingredients.py`
A class that maintains a user's Bag of Ingredients. A user can:
* Add/Delete/update ingredients in their bag.

### `recipe_recommender.py`
A class that has methods to search for recipes with given inputs:
* Desired ingredients (i.e. chicken, potatoes, etc)
* Nutritional Requirements (i.e. min and max values of calories, carbohydrates, proteins, and fats)
* Intolerances (i.e. lactose, egg, gluten etc)
* Diet (i.e. Vegan, Gluten-Free, Ketogenic, etc)  
The recipes displayed can be used for comparison.

### `comparator.py`
A class that has methods to visually compare nutrients and ingredients for selected recipes.
* The nutrient comparator shows a bargraph of different nutritional information amounts per each recipe
* The ingredient comparator shows pictures of the ingredients in a selected recipe

### `database.py`
A class that acts as a wrapper around psycopg2 to enable easier PostrgreSQL database access.
* Interacts with the Bag of Ingredients to maintain user data in the backend.

### `constants.py`
This module consists of global constants like apikeys, sample objects, and so on, used in multiple modules .
It also consists of: 
* Two classes that define the objects for recipes and ingredients used everywhere.
* A function that raises an ApikeyOutOfPoints exception to avoid overage costs.
* The definition of the ApikeyOutOfPoints exception.

## Data Sources and Management

### Spoonacular
Spoonacular is a Recipe-Food-Nutrition API providing access to over 365,000 recipes through ingredient- and nutrient-based queries. The user can also include keywords or phrases, such as ‘lactose intolerance’, to search for recipes that accommodate any special dietary restrictions or preferences. Additionally, the user can analyze nutritional information for each recipe by utilizing the visualization widgets.

### Firebase
Firebase is part of the google cloud services and is used in this project for User Authentication and User ID management. This is used for User Registration and Login.

### PostgreSQL
PostgreSQL is an open-source relational database management system offered by Heroku along with deployment capabilities to host our website online. We use PostgreSQL to store User data and Bag of Ingredients data. Database transactions are managed using the database wrapper around `psycopg2` we developed which performs the necessary functions for our use cases.

## Coding Standards  - PEP8  
This code follows standards set by Flake-8. The code ignores Flake-8 warning: W503. W503 does not allow line break __before__ binary operators. This warning is ignored as it contradicts with W504, which does not allow line break __after__ binary operators. The code follows W504 standards, and therefore W503 is ignored. Flake-8 also ignores one file: `app/__init__.py`. The import statement in `app/__init__.py` is required be on the bottom of the file to work for flask, and therefore this file is ignored.

The command used to check flake-8:
```
flake8 --ignore=W503 --exclude=app/__init__.py
```

## Testing
The code that is tested in this project are in the modules folder. Unit tests are used to test the code in the modules. The unit tests must be run in a specific order, and since pytest test order is used to ensure proper unit test order; it is necessary to run the unit tests using pytest. Pytest also allows checking for unit test coverage.

For Coverage, only the modules folder is tested, as functionality is all in the modules. The app folder is not tested as the code is for the UI of the webpage.

The command used to run the unit tests:
```
pytest --cov=modules
```

## Future Work

* Add in Machine Learning to recommend recipes based on user ratings of past recipes - building a recommendation system.
* Allowing users to save recipes they like to their profile.
* Saving user preferences such as food intolerances during registration.
* Creating functionality for “guest” users that don’t want to create a profile.
* Making visual comparator more interactive.
* Making our application highly scalable and highly available by using cloud services.
* Developing a Meal Planner.

More information about the project proposal can be found [HERE.](https://docs.google.com/document/d/1VCmc425JY53zHsUiasGh4CeFm5eu0YMbTKfwk1pRHZA/edit#heading=h.5x0d5h95i329)   
