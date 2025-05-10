import os

class Config(object):
    MAIL_FROM_EMAIL = "mulirokhaemba@gmail.com" # For use in application emails
    SQLALCHEMY_DATABASE_URI = "sqlite:///fitness.db"
    SECRET_KEY = 'relapse'
    STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
    STRIPE_PUBLIC_KEY = "pk_test_51RNKsRQ21kVJaE9p11frh2gRCBzUlX8mCNYKvkqdgemNpAUVGODCyNExwjb3Wmk9PLJqcXZRkBvueNIRjnmK6GoY00hlNreb4l"
