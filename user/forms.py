from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, BooleanField
from flask_wtf.file import FileField, FileAllowed


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


class ProfileForm(FlaskForm):
	username = StringField('Username', [validators.Required('Please enter your username.')])
	bio = StringField('Bio')
	location = StringField('Location')
	website = StringField('Website')
	profile_photo = FileField('Display picture', validators=[FileAllowed(['jpg', 'png'], 'Images only')])
	header_photo = FileField('Header picture', validators=[FileAllowed(['jpg', 'png'], 'Images only')])
