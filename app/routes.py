#render_template() invokes Jinja2 template engine for powerful operations in templates
from flask import render_template   
from app import app

#when url inside this function is called the following function executes and returns to the browser page that called it.
@app.route('/')
@app.route('/index')
#view function
def index():
    user = {'username': 'User'}
    return render_template('index.html', user=user)