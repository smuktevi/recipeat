from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, RadioField, \
    SubmitField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    """
    Register form class. Sets up all the required form widgets for
    registration here.
    """
    name = StringField('Full Name', validators=[DataRequired()])
    username = StringField('Username (Email Address)',
                           validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    age = IntegerField('Age (Number)')
    height = IntegerField('Height (Number in Inches)')
    weight = IntegerField('Weight (Number in Pounds)')
    gender = RadioField('Gender', choices=['Male', 'Female'], default='Male')
    submit = SubmitField('Register')
