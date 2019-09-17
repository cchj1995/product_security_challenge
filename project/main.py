# main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('userpage.html');

@main.route('/userpage')
@login_required
def userpage():
    return render_template('userpage.html', name=current_user.name);
    