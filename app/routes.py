# render_template() invokes Jinja2 template engine for powerful operations in templates
from flask import *
import pyrebase
from app import app
from app.forms.ingredients_form import LoginForm
from app.forms.register_form import RegisterForm

config = {
    "apiKey": "AIzaSyALmQ-MUJqlIWPmZZK8P73JTxgiWFzcTwY",
    "authDomain": "recipeat-e5c29.firebaseapp.com",
    "databaseURL": "https://recipeat-e5c29-default-rtdb.firebaseio.com",
    "projectId": "recipeat-e5c29",
    "storageBucket": "recipeat-e5c29.appspot.com",
    "messagingSenderId": "141820818637",
    "appId": "1:141820818637:web:303e5636dc57aabbd9e584",
    "measurementId": "G-SHGP23CXCE"
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
    form = LoginForm()
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
            return render_template('login.html', title='Sign In', form=form,  alertmessage=unsuccessful)

    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')

    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        session['name'] = request.form['name']
        session['username'] = request.form['username']
        session['password'] = request.form['password']


        try:
            auth.create_user_with_email_and_password(session['username'], session['password'])
            return render_template('register.html', title='Register', form=form, successmessage="Successfully Registered Account!")
        except:
            unsuccessful = 'Failed to register account! Check if email is valid! Check if password is long enough! Email may already be registered!'
            return render_template('register.html', title='Register', form=form, alertmessage=unsuccessful)


        #return redirect(url_for('home'))

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
