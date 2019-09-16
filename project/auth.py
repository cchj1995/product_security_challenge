# auth.py

from flask import Blueprint
from . import db
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from .users import User
from bcrypt import hashpw, gensalt

auth = Blueprint('auth', __name__)

@auth.route('/register')
def register():
    return render_template('register.html')
    
@auth.route('/register', methods=['POST'])
def register_post():
    inputname = request.form.get('name')
    inputpassword = request.form.get('password')
    inputemail = request.form.get('email')
    
    usernameExists = User.query.filter_by(name=inputname).first()
    emailExists = User.query.filter_by(email=inputemail).first()
    
    if usernameExists:
        flash('User with the same username already exists')
        return redirect(url_for('auth.register'))
    elif emailExists:
        flash('User with the same email already exists')
        return redirect(url_for('auth.register'))
    else:
         new_user = User(name=inputname, password=hashpw(inputpassword.encode('utf8'), gensalt()),email=inputemail)
         db.session.add(new_user)
         db.session.commit()
         return redirect(url_for('auth.login'))
   
@auth.route('/')
def login():
    return render_template('index.html')
    
@auth.route('/', methods=['POST'])
def login_post():
    name = (request.form.get('name'))
    password = request.form.get('password')
    email = request.form.get('email')
    remember = True if request.form.get('remember') else False
    
    user = User.query.filter_by(name=name).first()
    
    if not user:
        flash('No such username found')
        return redirect(url_for('auth.login'))
    elif not (hashpw(password.encode('utf8'), user.password) == user.password):
        flash('Username does not match password')
        return redirect(url_for('auth.login'))
    else:
        login_user(user, remember=remember)
        return redirect(url_for('main.userpage'))
    
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))  

    
    
    
    
    
    
    
    
    