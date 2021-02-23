# render_template() invokes Jinja2 template engine for powerful operations in templates
from flask import render_template, flash, redirect, url_for, escape, request, session
import pyrebase
from app import app
from app.forms.ingredients_form import LoginForm
from app.forms.register_form import RegisterForm

config = {
    "apiKey": "AIzaSyALmQ-MUJqlIWPmZZK8P73JTxgiWFzcTwY",
    "authDomain": "recipeat-e5c29.firebaseapp.com",
    "projectId": "recipeat-e5c29",
    "storageBucket": "recipeat-e5c29.appspot.com",
    "messagingSenderId": "141820818637",
    "appId": "1:141820818637:web:d29b714c5cc98bb6d9e584",
    "measurementId": "G-28H1MDHXJC"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


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

        try:
            auth.sign_in_with_email_and_password(session['username'], session['password'])
            return redirect(url_for('index'))
        except:
            unsuccessful = 'Please check your credentials'
            return render_template('login.html', alertmessage=unsuccessful)

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

        '''
        try:
            auth.create_user_with_email_and_password(email, password)
            return render_template('register.html', successmessage="Successfully Registered Account!")
        except:
            unsuccessful = 'Email is already registered'
            return render_template('register.html', alertmessage=unsuccessful)
        '''

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
