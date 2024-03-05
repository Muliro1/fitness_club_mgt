from app import app, db, bcrypt
from sqlalchemy.event import listen
from flask import render_template, url_for, flash, redirect, request, abort
from app.forms import RegistrationForm, LoginForm, AccountUpdateForm, PostForm
from app.models import User, Post, Physical
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image


classes = [
    {
        'day': 'Monday',
        'title': 'Zumba dance fitness',
        'content': 'Dance your way to a fit body',
        'date_posted': 'April 20, 2018'
    },
    {
        'day': 'Tuesday',
        'title': 'Step aerobics',
        'content': 'Aerobics to the rescue!!',
        'date_posted': 'April 21, 2018'
    },
    {
        'day': 'Wednesday',
        'title': 'Hike Away',
        'content': 'If you love hiking, this is for you!!',
        'date_posted': 'April 21, 2018'
    },
    {
        'day': 'Thursday',
        'title': 'Pool aerobics',
        'content': 'Are you ready to get wet in the pool',
        'date_posted': 'April 21, 2018'
    },
    {
        'day': 'Friday',
        'title': 'Weight training',
        'content': 'for the muscle heads!!',
        'date_posted': 'April 21, 2018'
    },
    {
        'day': 'Saturday',
        'title': 'Taebo!!',
        'content': 'Train with some taekwondo and boxing!!!',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts, classes=classes)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.password.data is not None and form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_profile_picture(form_pic):
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(form_pic.filename)
    pic_name = random_hex + file_extension
    pic_path = os.path.join(app.root_path, 'static/pics', pic_name)
    pic_size = (125, 125)
    pic = Image.open(form_pic)
    pic.thumbnail(pic_size)
    pic.save(pic_path)
    return pic_name

@app.route("/account", methods=['GET', 'POST'])
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
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        #form.body_mass_index.data = current_user.fitness_status[-1]
    image_file = url_for('static', filename='pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('your post has been created!!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@app.route("/classes", methods=['GET', 'POST'])
@login_required
def d_class():
    return render_template('classes.html', classes=classes)

@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('successfully edited!!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Edit Post', form=form, legend='Edit Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))
    