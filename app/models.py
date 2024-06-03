from app import db, login_manager, app
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from flask_login import UserMixin

"""
Defines a function that is used to load a user

It is used by the login_manager to load a user from the database

:param user_id: An integer representing the user's id

:return: A User instance representing the user with the given id
"""

@login_manager.user_loader
def load_user(user_id):
    """
    Load a user from the database

    This function is used by the login_manager to load a User
    instance from the database.

    :param user_id: An integer representing the user's id
    :type user_id: int

    :return: A User instance representing the user with the given id
    :rtype: User
    """
    # Load a user from the database
    return User.query.get(int(user_id))




class User(db.Model, UserMixin):
    """
    User class for the database. It uses Flask-Login for user management.

    It's important to note that Flask-Login uses the UserMixin to provide default implementations
    for the methods that Flask-Login expects user objects to have.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    fitness_status = db.relationship('Physical', backref='member', lazy=True)
    monthly_subscriptions = db.relationship('Monthly', backref='subscribed_monthly', lazy=True)
    annual_subscriptions = db.relationship('Annually', backref='subscribed_annually', lazy=True)
    bi_annual_subscriptions = db.relationship('BiAnnually', backref='subscribed_bi_annually', lazy=True)


    def __repr__(self):
        """
        Returns a printable representation of the User.

        :return: A string representing the User's information.
        :rtype: str
        """
        # Get all subscriptions and convert to a string
        all_subs = [self.monthly_subscriptions, self.annual_subscriptions, self.bi_annual_subscriptions]
        subs_str = ", ".join(map(str, all_subs))

        # Return the representation string
        return f"User('{self.username}', '{self.email}') subscribed to ({subs_str})"

class Post(db.Model):
    """
    Defines the posts table within the database. Each post has a title, a date when it was
    posted, and the content of the post. It also has a user_id which is a foreign key to the
    User table. This means that each post is owned by a user.
    """
    # Unique id for the post
    id = db.Column(db.Integer, primary_key=True)
    # Title of the post
    title = db.Column(db.String(100), nullable=False)
    # Date when the post was created
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # Content of the post
    content = db.Column(db.Text, nullable=False)
    # Foreign key to the User table. This means that each post is owned by a user.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        """
        Returns a printable representation of the Post.

        :return: A string representing the Post's information.
                 Example: 'Post('Title', '2023-01-01')'
        :rtype: str
        """
        return f"Post('{self.title}', '{self.date_posted}')"
    
class Physical(db.Model):
    """
    defines the physical table within the database
    """
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float(precision=8, asdecimal=False), nullable=False)
    height = db.Column(db.Float(precision=8, asdecimal=False), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bmi = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """
        physical table representation
        """
        # return a printable representation of the physical table
        return f"your height is '{self.height}'metres, your weight is '{self.weight}' kg and bmi is '{self.bmi}'"
    
class Monthly(db.Model):
    ''' defines the monthly subscription model within the database'''
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)                 
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow() + timedelta(days = 28))
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"subscription started on('{self.start_date}') and ends on ('{self.end_date}')"
    
class Annually(db.Model):
    ''' defines the annual subscription model'''
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)                 
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow() + relativedelta(months = 12))
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"subscription started on('{self.start_date}') and ends on ('{self.end_date}')"
    
class BiAnnually(db.Model):
    '''defines the half yearlysubscription model'''
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)                 
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow() + relativedelta(months = 6))
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f" subscription started on('{self.start_date}') and ends on ('{self.end_date}')"
    
class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    time = db.Column(db.String(100), nullable=False)



        