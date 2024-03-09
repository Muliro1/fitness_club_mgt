from app import db, login_manager, app
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    #loads current_user
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    """
    defines the user table within the database
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
        """prints the representation of a user
        """
        all_subs = [self.monthly_subscriptions, self.annual_subscriptions, self.bi_annual_subscriptions]
        return f"User('{self.username}', '{self.email}') subscribed to ('{all_subs}')"


class Post(db.Model):
    """defines the posts table within the database"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        """post representation"""
        return f"Post('{self.title}', '{self.date_posted}')"
    
class Physical(db.Model):
    """defines the physical table within the database"""
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bmi = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """physical table representation"""
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



        