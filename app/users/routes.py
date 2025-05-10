from app import app, db, bcrypt
from sqlalchemy.event import listen
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from app.users.forms import RegistrationForm, LoginForm, AccountUpdateForm, SubscriptionForm
from app.models import User, Post, Physical, Monthly, Annually, BiAnnually, Schedule
from flask_login import login_user, current_user, logout_user, login_required
from app.users.utils import save_profile_picture
import stripe
import os

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    """
    Route for registering a new user.

    The function checks if the current user is authenticated. If they are,
    they are redirected to the home page.

    The function then creates a registration form and if the form is submitted
    and validates, the user's password is hashed and the user is added to the
    database.

    Finally, the user is flashed a success message and redirected to the
    login page.
    """
    # If the user is already logged in, send them back to the home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    # Create a registration form
    form = RegistrationForm()

    # If the form is submitted and validates
    if form.password.data is not None and form.validate_on_submit():
        # Hash the user's password
        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode('utf-8')

        # Create a new user with the form data
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )

        # Add the user to the database
        db.session.add(user)
        db.session.commit()

        # Flash a success message
        flash(f'Account created for {form.username.data}!', 'success')

        # Redirect to the login page
        return redirect(url_for('users.login'))

    # Render the registration template
    return render_template(
        'register.html',
        title='Register',
        form=form
    )



@users.route("/login", methods=['GET', 'POST'])
def login():
    """
    Route for logging in a user.
    """
    # If the user is already logged in, send them back to the home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    # Create a login form
    form = LoginForm()

    # If the form is submitted and validates
    if form.validate_on_submit():
        # Query the database for a user with the given email address
        user = User.query.filter_by(email=form.email.data).first()

        # Check if the user exists and their password is correct
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Log the user in
            login_user(user, remember=form.remember.data)

            # Check for a 'next' URL in the query string and redirect to it if it exists
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            # Flash a message to the user saying that their login was unsuccessful
            flash('Login Unsuccessful. Please check username and password', 'danger')

    # Render the login template with the form
    return render_template('login.html', title='Login', form=form)




"""
Logs out the current user.
"""

@users.route("/logout")
def logout():
    """
    Logs out the current user.
    """
    # Log the current user out
    logout_user()

    # Redirect the user to the home page
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """
    Route for handling user account info.
    
    This route handles both GET and POST requests. For GET requests, it
    retrieves the user's account info and renders the 'account.html' template.
    For POST requests, it updates the user's account info and redirects to
    the same route ('users.account').

    Returns:
        - For GET requests: a rendered 'account.html' template.
        - For POST requests: a redirect to the same route ('users.account').

    """
    # Create a form for updating the user's account info
    form = AccountUpdateForm()

    # If the form is submitted and validates
    if form.validate_on_submit():
        # If a new picture is uploaded, save it and update the user's image_file
        if form.picture.data:
            pic_file = save_profile_picture(form.picture.data)
            current_user.image_file = pic_file

        # Calculate the user's BMI
        bmi = form.weight.data / (form.height.data ** 2)

        # Create a new Physical object with the new data and add it to the session
        physical = Physical(weight=form.weight.data, height=form.height.data, user_id=current_user.id, bmi=bmi)
        db.session.add(physical)

        # Update the user's username and email and commit the changes to the database
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()

        # Flash a success message and redirect to the same route ('users.account')
        flash('Your account info has been updated successfully', 'success')
        return redirect(url_for('users.account'))

    # If the request is a GET request, pre-populate the form fields with the user's data
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    # Get the URL for the user's profile picture
    image_file = url_for('static', filename='pics/' + current_user.image_file)

    # Render the 'account.html' template with the form and other data
    return render_template('account.html', title='Account', image_file=image_file, form=form)




@users.route("/subscribe", methods=['POST', 'GET'])
@login_required
def subscribe():
    """
    Route for handling subscription form submissions.

    If the form is valid and the user's password is correct, a new subscription
    is created in the database and the user is redirected to the home page.
    """

    # Create a form for subscribing to a plan
    form = SubscriptionForm()

    # Check if the form is submitted and if the user's password is correct
    if form.validate_on_submit() and bcrypt.check_password_hash(current_user.password, form.password.data):
        # Determine the type of subscription selected
        subscription_type = form.subscription.data

        # Create a new subscription object with the correct price
        if subscription_type == 'monthly':
            subscription = Monthly(user_id=current_user.id, price=5000)
            price_id = "price_1RNMKEQ21kVJaE9pzs7mrsJS"
        elif subscription_type == 'annually':
            subscription = Annually(user_id=current_user.id, price=50000)
            price_id = "price_1RNMKoQ21kVJaE9pR8qLoPe8"
        elif subscription_type == 'bi_annually':
            subscription = BiAnnually(user_id=current_user.id, price=25000)
            price_id = "price_1RNMLNQ21kVJaE9pb55H7O2C"
        else:
            # If the subscription type is invalid, flash an error and redirect back
            flash('Invalid subscription type. Please try again.', 'danger')
            return redirect(url_for('users.subscribe'))
        
        try:
            checkout_session = stripe.checkout.Session.create(
            line_items=[
            {
                    # Provide the exact Price ID (for example, price_1234) of the product you want to sell
                    'price': price_id,
                    'quantity': 1,
            },
            ],
        mode='subscription',
        success_url='https://fitness-club-mgt-1.onrender.com' + '/success.html',
        cancel_url='https://fitness-club-mgt-1.onrender.com' + '/cancel.html',
        )
        except Exception as e:
                return str(e)

        # Add the subscription to the session and commit the changes
        db.session.add(subscription)
        db.session.commit()

        # Flash a success message and redirect to the home page
        flash(f'Subscribed to {subscription_type} successfully!', 'success')
        return redirect(checkout_session.url, code=303)

    # If the request is a GET request, render the 'subscriptions.html' template
    # with the subscription form
    return render_template('subscriptions.html', form=form)



@users.route("/classes", methods=['GET', 'POST'])
@login_required
def d_class():
    """
    Route for displaying a list of all classes.
    """
    # Get all the classes from the database
    classes = Schedule.query.all()

    # Render the 'classes.html' template with the list of classes
    return render_template('classes.html', classes=classes)
