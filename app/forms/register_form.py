from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    username = StringField('Username (Email Address)', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    age = IntegerField('Age')
    height = IntegerField('Height')
    weight = IntegerField('Weight')
    gender = RadioField('Gender', choices=['Male', 'Female'])
    submit = SubmitField('Register')
