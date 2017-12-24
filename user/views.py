from flask import render_template, redirect, session, url_for, request
from twitter import app, db, login_manager
from user.models import Signup
from twitter import app, db
from user.forms import SignupForm, LoginForm
from user.models import Signup, Profile
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Creating a view/route for the registration form"""
    form = SignupForm()
    # Validating the signup form
    unique_error = ""
    if form.validate_on_submit():
        # Checking if the username is already taken
        if not Signup.query.filter_by(username=form.username.data).first():
            user = Signup(form.username.data, 
                          form.email.data, 
                          generate_password_hash(form.password.data),
                          date.today().strftime('%d %B, %Y'))
            db.session.add(user)
            db.session.commit()
            # Creating an instance of user profile info
            profile = Profile(user.id)
            db.session.add(profile)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            # Error is username is already taken
            unique_error = 'Username is already taken.'
    return render_template('user/signup.html', form=form, unique_error=unique_error)


@login_manager.user_loader
def load_user(user_id):
    """ Return the current user object that has logged in """
    return Signup.query.filter_by(id=user_id).first()



@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    """ This is a login route. It validates the login form and checks the user
    if it exists or not and also checks for the correct username and password"""
    error = ""
    # Initialzing the login form
    form = LoginForm()
    # Checking if redirect url is present after login
    if request.args.get('next'):
        session['next'] = request.args.get('next')
    if form.validate_on_submit():
        if Signup.query.filter_by(username=form.username.data).first():
            user = Signup.query.filter_by(username=form.username.data).first()
            # Matching the password and logging user
            if check_password_hash(user.password, form.password.data):
                if 'next' in session and session['next']!=None and session['next']!='/logout':
                    next = session['next']
                    if form.remember.data:
                        login_user(user, remember=True)
                        return redirect(next)
                    else:
                        login_user(user, remember=False)
                        return redirect(next)
                else:
                    if form.remember.data:
                        login_user(user, remember=True)
                        return redirect(url_for('timeline', username=user.username))
                    else:
                        login_user(user, remember=False)
                        return redirect(url_for('timeline', username=user.username))
            else:
                error = 'Wrong username or password'

        else:
            error = 'Wrong username or password'


    return render_template('user/login.html', form=form, error=error)


@app.route('/logout')
@login_required
def logout():
    """ Logging user out """
    logout_user()
    return redirect(url_for('login'))