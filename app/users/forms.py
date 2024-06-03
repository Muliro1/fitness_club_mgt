from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User





# Defines the user registration form and all its fields
# The following fields are defined:
# - username (DataRequired, Length(min=2, max=20))
# - email (DataRequired, Email)
# - password (DataRequired)
# - confirm_password (DataRequired, EqualTo('password'))
# - submit (SubmitField)
# The following validators are defined:
# - validate_username: checks the presence of username within the form, if the username is already taken, a ValidationError is raised
# - validate_email: checks the presence of email within the form before submitting, if the email is already taken, a ValidationError is raised
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        """checks the presence of username within the form, if the username is already taken, a ValidationError is raised"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('username is already taken please choose a different one.')
        
    """
    This method checks the presence of email within the form before submitting.
    If the email is already taken, a ValidationError is raised.
    """

    def validate_email(self, email):
        """
        Checks the presence of email within the form before submitting.

        Parameters:
        - email (StringField): The email field in the form.

        Raises:
        - ValidationError: When the email is already taken.
        """

        # Check if email is already in the database
        email_entry = User.query.filter_by(email=email.data).first()

        # Raise error if email is already taken
        if email_entry:
            raise ValidationError('Email is already taken, please choose a different one.')









class LoginForm(FlaskForm):
    """
    Defines the user login form and all its fields.
    """
    # The email field with validation for email and required data
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    # The password field with validation for required data
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
    # The remember me checkbox
    remember = BooleanField('Remember Me')
    # The login submit button
    submit = SubmitField('Login')


class AccountUpdateForm(FlaskForm):
    """
    Defines the account update form and all its fields.
    """
    # The username field with validation for presence and length
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=2, max=20)
        ]
    )
    # The email field with validation for presence and email format
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )
    # The weight field with validation for presence
    weight = FloatField(
        'Weight',
        validators=[
            DataRequired()
        ]
    )
    # The height field with validation for presence
    height = FloatField(
        'Height',
        validators=[
            DataRequired()
        ]
    )
    # The picture field for uploading the user's profile picture
    picture = FileField(
        'Update Profile Picture',
        validators=[
            FileAllowed(['jpg', 'png'])
        ]
    )
    # The submit button for the form
    submit = SubmitField('Update Account')

    def validate_username(self, username):
        """
        Validates the presence of username within the form.

        Raises:
        - ValidationError: When the username is already taken.
        """
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('username is already taken please choose a different one.')

    def validate_email(self, email):
        """
        Validates the presence of email within the form before submitting.

        Raises:
        - ValidationError: When the email is already taken.
        """
        if email.data != current_user.email:
            email_entry = User.query.filter_by(email=email.data).first()
            if email_entry:
                raise ValidationError('Email is already taken, please choose a different one.')

            
class SubscriptionForm(FlaskForm):
    """
    Form for creating a new subscription.

    Fields:
    - username: The username of the user.
    - email: The email of the user.
    - password: The password of the user.
    - subscription: The subscription model.
    - submit: The submit button.
    """

    # The username field for the subscription form
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=2, max=20)
        ],
        description='Enter your username'
    )

    # The email field for the subscription form
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Length(min=2, max=20)
        ],
        description='Enter your email'
    )

    # The password field for the subscription form
    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ],
        description='Enter your password'
    )

    # The subscription field for the subscription form
    subscription = SelectField(
        u'Subscription model',
        choices=[
            ('monthly'),
            ('annually'),
            ('bi_annually')
        ],
        description='Choose your subscription model'
    )

    # The submit button for the subscription form
    submit = SubmitField(
        'Subscribe',
        description='Subscribe to our service'
    )
