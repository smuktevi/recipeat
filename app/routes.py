# render_template() invokes Jinja2 template engine for powerful operations in templates
from flask import render_template, flash, redirect, url_for, escape, request, session
from app import app
from app.forms.ingredients_form import LoginForm
from app.forms.register_form import RegisterForm


# when url inside this function is called the following function executes and returns to the browser page that called it.
@app.route('/')
@app.route('/index')
# view function
def index():
    user = {'username': 'User'}
    return render_template('index.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        username = session['username']
        return 'Logged in as ' + username + '<br>' + "<b><a href = '/logout'>click here to log out</a></b>"

    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')

    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        session['name'] = request.form['name']
        session['username'] = request.form['username']
        session['password'] = request.form['password']

        return redirect(url_for('home'))

    form = RegisterForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/register')

    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('index'))


@app.route('/ingredients', methods=['GET', 'POST'])
def ingredients():
    return render_template('ingredients.html')
