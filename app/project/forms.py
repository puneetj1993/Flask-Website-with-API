from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from project.models import User
from flask import flash

class Registration(FlaskForm):

    username = StringField('username',validators =[DataRequired()])
    email = StringField('email', validators=[DataRequired(),Email()])
    password = PasswordField('password',validators=[])
    confirm_password = PasswordField('confirm password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        '''
            Validates if username already exists and returns a validation error
        '''
        user = User.query.filter_by(username=username.data).first()
        if user:
            flash("Username already exists. Please try with another username")
            raise ValidationError()
    
    def validate_email(self,email):
        '''
            Validates if email already exists and returns a validation error
        '''
        user = User.query.filter_by(email=email.data).first() 
        if user:
            flash("Email already exists. Please try with some other email")
            raise ValidationError()
    
class LoginForm(FlaskForm):

    
    email = StringField('email',validators=[DataRequired(),Email()])
    password = StringField('password',validators=[DataRequired()])
    submit = SubmitField('Sign In')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            flash("Email id which you have entered doesn't exist.")
            raise ValidationError("Email doesn't exists")