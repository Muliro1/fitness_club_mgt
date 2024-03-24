from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User




class RegistrationForm(FlaskForm):
    """Defines the user registration form
    and all its fields"""
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('username is already taken please choose a different one')
        
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email is already taken, please choose a different one.')


class LoginForm(FlaskForm):
    """defines the user login form and all its fields"""
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AccountUpdateForm(FlaskForm):
    """defines the account update form ald all its fields"""
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    weight = FloatField('Weight',
                          validators=[DataRequired()])
    height = FloatField('Height',
                          validators=[DataRequired()])
    #body_mass_index = FloatField('bmi')
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update Account')

    def validate_username(self, username):
        """validates the presence of username within the form"""
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('username is already taken please choose a different one')
        
    def validate_email(self, email):
        """validates the presence of email within 
        the form before submitting"""
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('Email is already taken, please choose a different one.')
            
class SubscriptionForm(FlaskForm):
    ''' defines the user subscription form'''
    username = StringField('Username', validators=[Length(min=2, max=20)])
    email = StringField('Email', validators=[Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    subscription = SelectField(u'Subscription model', choices = [('monthly'), ('annually'), ('bi_annually')])
    submit = SubmitField('Subscribe')