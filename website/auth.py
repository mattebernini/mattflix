from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db 
from .models import Utente

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from website.utility import save_cookie

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    save_cookie("signup")
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username').lower()
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user1 = Utente.query.filter_by(email=email).first()
        user2 = Utente.query.filter_by(username=username).first()
        if user1 or user2:
            flash('Email or username already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(username) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = Utente(email=email, username=username, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('frontend.index'))

    return render_template("auth/signup.html", user=current_user)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    save_cookie("login")
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Utente.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('frontend.index'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("auth/login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout effettuato!', category='success')
    return redirect(url_for('frontend.index'))
