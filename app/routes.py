#render_template() invokes Jinja2 template engine for powerful operations in templates
from flask import render_template, flash, redirect
from app import app
from app.forms.ingredients_form import LoginForm, MoreIngredientsForm


#when url inside this function is called the following function executes and returns to the browser page that called it.
@app.route('/')
@app.route('/index')
#view function
def index():
    user = {'username': 'User'}
    return render_template('index.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('landing.html', title='Sign In', form=form)

@app.route('/ingredients', methods=['GET', 'POST'])
def ingredients():
    user_ingredients = [{"name":"First Ingredient"},{"name":"Second Ingredient"},{"name":"Third Ingredient"}]
    form = MoreIngredientsForm(bag_of_ingredients = user_ingredients)
    return render_template('ingredients.html', form=form)