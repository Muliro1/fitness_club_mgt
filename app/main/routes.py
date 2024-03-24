from app import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from app.models import  Post, Schedule
from flask_login import current_user, login_required

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    classes = Schedule.query.all()
    posts = Post.query.all()
    return render_template('home.html', posts=posts, classes=classes)


@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/classes", methods=['GET', 'POST'])
@login_required
def d_class():
    classes = Schedule.query.all()
    return render_template('classes.html', classes=classes)