from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, BooleanField


class SignupForm(FlaskForm):
	"""Creating the registration form"""
	username = StringField('Name', [validators.Required('A username is required.'),
									validators.Length(min=5, max=100)])
	email = StringField('Email', [validators.Required('An Email ID is requried.')])
	password = PasswordField('Password', [validators.Required('A password is required.'),
										  validators.Length(min=5, max=80)])


class LoginForm(FlaskForm):
	username = StringField('Username', [validators.Required('Please enter your username.')])
	password = PasswordField('Password', [validators.Required('Please enter your password.')])
	remember = BooleanField('Remember me')