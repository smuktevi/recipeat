# render_template() invokes Jinja2 template engine for powerful operations in templates
from flask import *
from app import app
from app.forms.login_form import LoginForm
from app.forms.register_form import RegisterForm
from app.forms.ingredients_form import IngredientForm
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

        register_success = User.register_user(username, password, name, age, height, weight, gender)
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

    if request.method == 'POST':
        ingredient = request.form['ingredient']
        quantity = request.form['quantity']

        # TODO call update ingredient to bag of ingredients
        #session['user'].update_boi()

    return render_template('ingredients.html', form=form)


@app.route('/recipe', methods=['GET', 'POST'])
def recipe():
    return render_template('recipe.html')