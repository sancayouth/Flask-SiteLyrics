# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask.ext.login import login_user, logout_user, login_required
from forms import LoginForm
from ..app import bcrypt
from app.models import User

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    rform = request.form
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=rform.get('username')).first()
            if user is not None and bcrypt.check_password_hash(
                user.password, rform.get('password')
            ):
                remember = rform.get('remember_me') == 'y'
                login_user(user, remember=remember)
                flash('You were logged in')
                return redirect(url_for('home.home_'))
            else:
                flash('Oops , Try Again!')
    return render_template('login.html', title='Flask Lyrics - login',
                           form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.')
    return redirect(url_for('home.home_'))
