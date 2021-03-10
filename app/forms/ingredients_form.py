from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired


class IngredientForm(FlaskForm):
    """
    Recipe form class. Sets up all the required form widgets for the
    ingredient form.
    """
    ingredient = StringField('Ingredient', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    units = StringField('Units (Metric)')
    submit = SubmitField('Add Ingredient')

<<<<<<< HEAD
    update_ingredient = StringField(
        'Ingredient to update', validators=[
            DataRequired()])
    update_quantity = IntegerField('New Quantity', validators=[DataRequired()])
    update_submit = SubmitField('Update Ingredient')

    delete_ingredient = StringField(
        'Ingredient to delete', validators=[
            DataRequired()])
=======
    update_ingredient = StringField('Ingredient to update',
                                    validators=[DataRequired()])
    update_quantity = IntegerField('New Quantity', validators=[DataRequired()])
    update_submit = SubmitField('Update Ingredient')

    delete_ingredient = StringField('Ingredient to delete',
                                    validators=[DataRequired()])
>>>>>>> develop
    delete_submit = SubmitField('Delete Ingredient')
