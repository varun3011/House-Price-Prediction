from flask_wtf import FlaskForm
from wtforms import StringField ,IntegerField,PasswordField, SubmitField, RadioField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired,InputRequired, ValidationError,NumberRange

class PredictForm(FlaskForm):
    total_sqft = IntegerField(label="Area", validators=[InputRequired(), NumberRange(min=370, message='Must enter a number greater than 0')])
    location = SelectField(label="Location", validators=[DataRequired()])
    Type = RadioField('Type', choices=[('apartment', 'Apartment'), ('villa', 'Villa')],validators=[DataRequired()])
    submit = SubmitField(label="Submit")
