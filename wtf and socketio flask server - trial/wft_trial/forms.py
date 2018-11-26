from flask_wtf import FlaskForm
from wtforms import StringField, TextField, TextAreaField, BooleanField, DecimalField
from wtforms.validators import DataRequired


# http://www.tutorialspoint.com/flask/flask_wtf.htm - fields

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    text_field = TextField('text_field', validators=[])
    text_area_field = TextAreaField('text_area_field', validators=[])
    boolean_field = BooleanField('boolean_field', validators=[])
    decimial_field = DecimalField('decimial_field', validators=[])