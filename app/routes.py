# render_template() invokes Jinja2 template engine for powerful operations in templates
from flask import *
from app import app
from app.forms.login_form import LoginForm
from app.forms.register_form import RegisterForm
from app.forms.ingredients_form import IngredientForm
from app.forms.recipe_form import RecipeForm
from modules.user import User
from modules.constants import *


# when url inside this function is called the following function executes and returns to the browser page that called it.
@app.route('/index')
# view function
def index():
    if 'username' in session:
        user = session['name']
    else:
        user = 'New User'
    return render_template('index.html', user=user)


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if 'username' in session:
        username = session['username']
        return 'Logged in as ' + username + '<br>' + "<b><a href = '/logout'>click here to log out</a></b>"

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        login_success = User.authenticate_user(username, password)

        if(login_success):
            # Successful login
            session['username'] = username
            session['password'] = password
            user_obj = User.get_user(username)
            session['name'] = user_obj.name
            return redirect(url_for('index'))
        else:
            # Failed login
            unsuccessful = 'Please check your credentials'
            return render_template('login.html', title='Sign In', form=form, alertmessage=unsuccessful)

    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')

    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        age = request.form['age']
        height = request.form['height']
        weight = request.form['weight']
        gender = request.form['gender']

        register_success = User.register_user(
            username, password, name, age, height, weight, gender)
        unsuccessful = 'Failed to register account! Check if formats are valid! Check if password is long enough! Email may already be registered! There cannot be empty Fields!'
        if(name == "" or age == "" or height == "" or weight == ""):
            return render_template('register.html', title='Register', form=form, alertmessage=unsuccessful)

        if(register_success):
            # Successful Registration
            return render_template('register.html', title='Register', form=form, successmessage='Successfully Registered Account!')
        else:
            # Failed Registration
            return render_template('register.html', title='Register', form=form, alertmessage=unsuccessful)

    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index', name=name)

    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    session.pop('password', None)
    session.pop('user_obj', None)
    return redirect(url_for('login'))


@app.route('/ingredients', methods=['GET', 'POST'])
def ingredients():
    form = IngredientForm()

    # TODO Query the database for BOI to display
    #username = session['username']


    if request.method == 'POST':
        ingredient = request.form['ingredient']
        quantity = request.form['quantity']
        units = request.form['units']

        if(ingredient == "" or quantity == ""):
            return render_template('ingredients.html', form=form, alertmessage="Ingredient and Quantity cannot be empty! Make sure Quantity is a number!")

        # TODO call update ingredient to bag of ingredients
        # session['user'].update_boi()

    return render_template('ingredients.html', form=form)


@app.route('/recipe', methods=['GET', 'POST'])
def recipe():
    form = RecipeForm()

    if request.method == 'POST':
        nutr = {}

        min_carb = request.form['min_carb']
        max_carb = request.form['max_carb']

        min_fat = request.form['min_fat']
        max_fat = request.form['max_fat']

        min_cal = request.form['min_cal']
        max_cal = request.form['max_cal']

        min_protein = request.form['min_protein']
        max_protein = request.form['max_protein']

        intolerances = request.form.getlist('intolerances')
        diets = request.form.getlist('diets')

        if(min_carb != ""):
            nutr['minCarbs'] = int(min_carb)
        if(max_carb != ""):
            nutr['maxCarbs'] = int(max_carb)
        if(min_fat != ""):
            nutr['minFat'] = int(min_fat)
        if (max_fat != ""):
            nutr['maxFat'] = int(max_fat)
        if (min_cal != ""):
            nutr['minCalories'] = int(min_cal)
        if (max_cal != ""):
            nutr['maxCalories'] = int(max_cal)
        if (min_protein != ""):
            nutr['minProtein'] = int(min_protein)
        if (max_protein != ""):
            nutr['maxProtein'] = int(max_protein)

    return render_template('recipe.html', form=form)
