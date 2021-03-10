from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
<<<<<<< HEAD
    username = StringField(
        'Username (Email Address)',
        validators=[
            DataRequired()])
=======
    """
    Login form class. Sets up all the required form widgets for login here.
    """
    username = StringField('Username (Email Address)',
                           validators=[DataRequired()])
>>>>>>> develop
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
