from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Email

class UserLoginForms(FlaskForm):


    firstname = StringField('First Name', validators = [DataRequired()])
    lastname = StringField('Last Name', validators = [DataRequired()])
    username = StringField('Username', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    date_of_birth = DateField('Date of Birth (YYYY-MM-DD)', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()]) #, EqualTo('confirm_password', message='Passwords must match')])
    #confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit_button = SubmitField()

class MovieForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    director = StringField('Director', validators=[DataRequired()])
    release_date = StringField('Release Date (YYYY-MM-DD)', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()])
    rating = DecimalField('Rating', validators=[DataRequired()])
    description = StringField('Description')
    image_url = StringField('Image_url')
    submit_button = SubmitField('Submit')