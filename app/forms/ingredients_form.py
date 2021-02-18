from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class IngredientForm(FlaskForm):
    item = StringField()

class MoreIngredientsForm(FlaskForm):
    """A form for one or more ingredients"""
    bag_of_ingredients = FieldList(FormField(IngredientForm), min_entries = 1)
