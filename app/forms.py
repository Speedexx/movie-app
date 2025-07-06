from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, FileField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, NumberRange

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=150)])
    email = StringField('Email', validators=[DataRequired(), Length(min=6, max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class MovieForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    image = FileField('Image')
    description = TextAreaField('Description')  # Nowe pole dla opisu filmu
    submit = SubmitField('Submit')

class RatingForm(FlaskForm):
    rating = IntegerField('Rating (1-5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit_rating = SubmitField('Submit Rating')  # Zmieniono nazwę

class CommentForm(FlaskForm):
    content = StringField('Comment', validators=[DataRequired()])
    submit_comment = SubmitField('Add Comment')  # Zmieniono nazwę