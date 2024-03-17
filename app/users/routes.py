from app import app, db, bcrypt
from sqlalchemy.event import listen
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from app.users.forms import RegistrationForm, LoginForm, AccountUpdateForm, SubscriptionForm
from app.models import User, Post, Physical, Monthly, Annually, BiAnnually, Schedule
from flask_login import login_user, current_user, logout_user, login_required
from app.users.utils import save_profile_picture


users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.password.data is not None and form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            pic_file = save_profile_picture(form.picture.data)
            current_user.image_file = pic_file
        bmi = form.weight.data / form.height.data ** 2
        physical = Physical(weight=form.weight.data, height=form.height.data, user_id=current_user.id, bmi=bmi)
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.add(physical)
        db.session.commit()
        flash('Your account info has been updated successfully', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)



@users.route("/subscribe", methods=['POST', 'GET'])
@login_required
def subscribe():
    form = SubscriptionForm()
    if form.validate_on_submit() and bcrypt.check_password_hash(current_user.password, form.password.data):
        if form.subscription.data == 'monthly':
            monthly_sub = Monthly(user_id=current_user.id, price=5000)
            db.session.add(monthly_sub)
            db.session.commit()
            flash('successfully subscribed to monthly!!', 'success')
            return redirect(url_for('main.home'))
        elif form.subscription.data == 'annually':
            annual_sub = Annually(user_id=current_user.id, price=50000)
            db.session.add(annual_sub)
            db.session.commit()
            flash('successfully subscribed to annual subscription!!', 'success')
            return redirect(url_for('main.home'))
        elif form.subscription.data == 'bi_annually':
            bi_annual_sub = BiAnnually(user_id=current_user.id, price=25000)
            db.session.add(bi_annual_sub)
            db.session.commit()
            flash('successfully subscribed to bi_annual subscription!!', 'success')
            return redirect(url_for('main.home'))
    return render_template('subscriptions.html', form=form)

@users.route("/classes", methods=['GET', 'POST'])
@login_required
def d_class():
    classes = Schedule.query.all()
    return render_template('classes.html', classes=classes)