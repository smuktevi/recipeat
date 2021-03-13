# render_template() invokes Jinja2 template engine for powerful operations in
# templates
from flask import session, render_template, request, redirect, url_for, flash
from app import app
from app.forms.login_form import LoginForm
from app.forms.register_form import RegisterForm
from app.forms.ingredients_form import IngredientForm
from app.forms.recipe_form import RecipeForm
from modules.user import User
from modules.bag_of_ingredients import BagOfIngredients
from modules.recipe_recommender import RecipeRecommender
from modules.comparator import Compare
from modules.constants import Recipe, Ingredient, ApikeyOutOfPoints
import json

"""
This file is the flask router file. It is used to route from one page to
another.
"""


@app.route('/index')
# view function
def index():
    """
    Index Page. Displays the user data on this page.

    :return: Rendered template for index page.
    """
    if 'username' in session:
        user = session['name']
        user_obj = User.get_user(session['username'])
    else:
        user = 'New User'
    return render_template('index.html', user=user, user_obj=user_obj)


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login page. Has the form for a user to login.

    :return: Rendered template for login page.
    """
    form = LoginForm()
    if 'username' in session:
        username = session['username']
        return 'Logged in as ' + username + '<br>' + ("<a href='/index'>Go to "
                                                      "main page!</a><br><b><a"
                                                      " href = '/logout'>Click"
                                                      " here to log out!</a></"
                                                      "b>")

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        login_success = User.authenticate_user(username, password)

        if login_success:
            # Successful login
            session['username'] = username
            session['password'] = password
            session['recipe_list'] = to_json([])
            session['compare_list'] = to_json([])
            user_obj = User.get_user(username)
            session['name'] = user_obj.name
            return redirect(url_for('index'))
        else:
            # Failed login
            unsuccessful = 'Please check your credentials'
            return render_template('login.html', title='Sign In', form=form,
                                   alertmessage=unsuccessful)

    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')

    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register page. Has the form to enter user data to register a new user.

    :return: Rendered template for Register page.
    """
    form = RegisterForm()

    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        age = request.form['age']
        height = request.form['height']
        weight = request.form['weight']
        gender = request.form['gender']

        unsuccessful = ('Failed to register account! Check if formats are vali'
                        'd! Check if password is long enough! Email may alread'
                        'y be registered! There cannot be empty Fields!')
        if name == "" or age == "" or height == "" or weight == "":
            return render_template('register.html', title='Register',
                                   form=form, alertmessage=unsuccessful)

        register_success = User.register_user(username, password, name, age,
                                              height, weight, gender)

        if register_success:
            # Successful Registration
            return render_template('register.html', title='Register',
                                   form=form,
                                   successmessage=('Successfully Registered Ac'
                                                   'count!'))
        else:
            # Failed Registration
            return render_template('register.html', title='Register',
                                   form=form, alertmessage=unsuccessful)

    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index', name=name)

    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    """
    Logout page. Pops all the session variables

    :return: Redirect to Login page.
    """
    # remove the username from the session if it is there
    session.pop('username', None)
    session.pop('password', None)
    session.pop('user_obj', None)
    session.pop('recipe_list', None)
    session.pop('compare_list', None)
    Compare.compare = None
    RecipeRecommender.recipe_recommender = None
    return redirect(url_for('login'))


@app.route('/ingredients', methods=['GET', 'POST'])
def ingredients():
    """
    Ingredients page. Shows the user their ingredients. Also has forms to add,
    delete, and update their ingredients.

    :return: Rendered template for ingredients page
    """
    form = IngredientForm()

    user_boi = BagOfIngredients(session['username'])
    ingredients_list = user_boi.get_boi()

    if request.method == 'POST':

        if 'submit' in request.form:

            ingredient = request.form['ingredient']
            quantity = request.form['quantity']
            units = request.form['units']

            if ingredient == "" or quantity == "":
                return render_template('ingredients.html', form=form,
                                       ingredients=ingredients_list,
                                       alertmessage=("Ingredient and Quantity "
                                                     "cannot be empty! Make su"
                                                     "re Quantity is a number!"
                                                     ))

            # Add ingredient to database
            ingredient_obj = Ingredient(
                ingredient_full=quantity + " " + units + " " + ingredient,
                ingredient_name=ingredient, amount=quantity, units=units)
            push_success = user_boi.push_boi(ingredient_obj)

            # Check if push to database was not successful. Return error page.
            if not push_success:
                return render_template('ingredients.html', form=form,
                                       ingredients=ingredients_list,
                                       alertmessage=("Ingredient is already in"
                                                     " bag!"))

            # Get the new list to display
            ingredients_list = user_boi.get_boi()
            return render_template('ingredients.html', form=form,
                                   ingredients=ingredients_list,
                                   pushsuccess="Successfully added ingredient!"
                                   )

        elif 'update_submit' in request.form:
            ingredient_name = request.form['update_ingredient']
            quantity = request.form['update_quantity']

            if ingredient_name == "" or quantity == "":
                return render_template('ingredients.html', form=form,
                                       ingredients=ingredients_list,
                                       alertmessage2=("Ingredient and Quantity"
                                                      " cannot be empty! Make "
                                                      "sure Quantity is a numb"
                                                      "er!"))

            update_success = user_boi.update_ingredient(
                "\'" + ingredient_name + "\'", "\'" + quantity + "\'")

            # Check if not successful. Return error page.
            if not update_success:
                return render_template('ingredients.html', form=form,
                                       ingredients=ingredients_list,
                                       alertmessage2=("Cannot update that quan"
                                                      "tity!"))

            # Get the new list to display
            ingredients_list = user_boi.get_boi()
            return render_template('ingredients.html', form=form,
                                   ingredients=ingredients_list,
                                   updatesuccess=("Successfully updated ingred"
                                                  "ient!"))

        elif 'delete_submit' in request.form:
            ingredient_name = request.form['delete_ingredient']

            if ingredient_name == "":
                return render_template('ingredients.html', form=form,
                                       ingredients=ingredients_list,
                                       alertmessage3=("Ingredient cannot be em"
                                                      "pty!"))

            delete_success = user_boi.delete_ingredient(
                "\'" + ingredient_name + "\'")

            # Check if not successful. Return error page.
            if not delete_success:
                return render_template('ingredients.html', form=form,
                                       ingredients=ingredients_list,
                                       alertmessage3=("Ingredient not in the b"
                                                      "ag!"))

            # Get the new list to display
            ingredients_list = user_boi.get_boi()
            return render_template('ingredients.html', form=form,
                                   ingredients=ingredients_list,
                                   deletesuccess=("Successfully deleted "
                                                  "ingredient!"))

    return render_template('ingredients.html', form=form,
                           ingredients=ingredients_list)


@app.route('/recipe', methods=['GET', 'POST'])
def recipe():
    """
    Recipe Recommender page. This page allows a user to select ingredients,
    nutritional requirements, intolerances, and a diet to find recipes. This
    page can display the recipes and allow the user to select recipes for
    comparison.

    :return: Rendered template for recipe page.
    """
    form = RecipeForm()
    user_boi = BagOfIngredients(session['username'])
    ingredients_list = user_boi.get_boi()
    choices = []
    for ingredient in ingredients_list:
        choices.append((ingredient[1], ingredient[1]))
    form.ingredients.choices = choices

    if request.method == 'POST':

        if 'submit' in request.form:
            min_carb = request.form['min_carb']
            max_carb = request.form['max_carb']

            min_fat = request.form['min_fat']
            max_fat = request.form['max_fat']

            min_cal = request.form['min_cal']
            max_cal = request.form['max_cal']

            min_protein = request.form['min_protein']
            max_protein = request.form['max_protein']

            # nutr is the nutrition dictionary to be passed into recipe
            # recommender
            nutr = {}
            if min_carb != "":
                nutr['minCarbs'] = str(min_carb)
            if max_carb != "":
                nutr['maxCarbs'] = str(max_carb)
            if min_fat != "":
                nutr['minFat'] = str(min_fat)
            if max_fat != "":
                nutr['maxFat'] = str(max_fat)
            if min_cal != "":
                nutr['minCalories'] = str(min_cal)
            if max_cal != "":
                nutr['maxCalories'] = str(max_cal)
            if min_protein != "":
                nutr['minProtein'] = str(min_protein)
            if max_protein != "":
                nutr['maxProtein'] = str(max_protein)

            # intolerances and diets are the lists that will be passed into
            # recipe recommender. May need to check if it is empty or not first
            intolerances = request.form.getlist('intolerances')
            diets = request.form.getlist('diets')
            ingredients = request.form.getlist('ingredients')

            if(len(diets) == 0):
                diets = ""
            else:
                diets = diets[0]

            # chosen ingredients is the ingredient list that will need to be
            # passed into recipe recommender
            chosen_ingredients_objects = []
            chosen_ingredients_names = []
            for ingredient in ingredients:
                ingredient_obj = Ingredient.parse_string(ingredient)
                chosen_ingredients_objects.append(ingredient_obj)
                chosen_ingredients_names.append(ingredient_obj.ingredient)

            # TODO add intolerances when the search_recipes has been modified
            try:
                recipe_list = RecipeRecommender.search_recipes(
                    ingredients=chosen_ingredients_names,
                    nutritional_req=nutr, diet=diets,
                    intolerances=intolerances)
                session['recipe_list'] = to_json(recipe_list)
            except ApikeyOutOfPoints:
                return render_template('recipe.html', form=form,
                                       empty_search="No more API points!")
            except:
                return render_template('recipe.html', form=form,
                                       empty_search="Back End Error!")

            if len(recipe_list) == 0:
                return render_template('recipe.html', form=form,
                                       empty_search="Found no recipes! Sorry!")
            return render_template('recipe.html', form=form,
                                   recipe_list=recipe_list)

        elif 'compare_submit' in request.form:
            try:

                recipe_compare_list = []
                recipe_list = from_json(session['recipe_list'])
                for recipe in recipe_list:
                    if str(recipe.recipe_id) in request.form:
                        recipe_compare_list.append(recipe)

                if len(recipe_compare_list) < 2:
                    return render_template('recipe.html', form=form,
                                           recipe_list=recipe_list,
                                           alertmessage=("At least two recipes"
                                                         " must be selected!"))

                session['compare_list'] = to_json(recipe_compare_list)
            except:
                print("ERROR IN COMPARATOR")
                redirect('/compare')
                return render_template('visual_comparator.html',
                                       msg=("Sorry, please try again, error oc"
                                            "curred in the Back End!"))
            return redirect('/compare')

    recipe_list = from_json(session['recipe_list'])
    if len(recipe_list) == 0:
        return render_template('recipe.html', form=form)
    else:
        return render_template('recipe.html', form=form,
                               recipe_list=recipe_list)


@app.route('/compare', methods=['GET', 'POST'])
def compare():
    """
    Compare page. This page displays visual comparison of the user's selected
    recipes to compare.

    :return: Rendered template for comparison page.
    """

    compare_list = from_json(session['compare_list'])

    if len(compare_list) == 0:
        return render_template('visual_comparator.html')

    nutrient_compare_html = Compare.nutrient_compare(compare_list)
    ingredient_compare_html = Compare.ingredient_compare(compare_list)

    if nutrient_compare_html is None or ingredient_compare_html is None:
        return render_template('visual_comparator.html')
    else:
        return render_template('visual_comparator.html',
                               ingredient_compare=ingredient_compare_html,
                               nutrient_compare=nutrient_compare_html)


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
    recipe_list = reconstruct_recipe_list(json_list)
    return recipe_list


def reconstruct_recipe_list(recipe_dictionary_list):
    """
    This is a helper function used to reconstruct Recipe and Ingredient objects
    back into their original form from a dictionary.

    :param recipe_dictionary_list: dict. A serialized dictionary.
    :return: list(Recipe). List of recipes constructed from the dictionary.
    """
    recipe_list = []
    for recipe_dictionary in recipe_dictionary_list:
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
