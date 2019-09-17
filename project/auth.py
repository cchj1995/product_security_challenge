# auth.py

from re import match
from flask import Blueprint
from . import db
from flask import Blueprint, render_template, redirect, url_for, request, flash, escape
from flask_login import login_user, logout_user, login_required
from .users import User
from bcrypt import hashpw, gensalt

auth = Blueprint('auth', __name__)

@auth.route('/register')
def register():
    return render_template('register.html')
    
@auth.route('/register', methods=['POST'])
def register_post():
    inputname = escape(request.form.get('name'))
    inputpassword = escape(request.form.get('password'))
    inputemail = escape(request.form.get('email'))
    
    if not match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$!*&])[\w\d@#$!*&]{6,12}$", inputpassword):
        flash('Password must have at least 1 uppercase letter, 1 lowercase letter, 1 digit and 1 special character (@#$!*&)')
        return redirect(url_for('auth.register'))
    
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
   
@auth.route('/login')
def login():
    return render_template('index.html')
    
@auth.route('/login', methods=['POST'])
def login_post():
    name = escape(request.form.get('name'))
    password = escape(request.form.get('password'))
    email = escape(request.form.get('email'))
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

    
    
    
    
    
    
    
    
    