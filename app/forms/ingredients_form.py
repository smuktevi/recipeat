from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired

class IngredientForm(FlaskForm):
    ingredient = StringField('Ingredient', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    units = StringField('Units (Metric)')
    submit = SubmitField('Add Ingredient')

