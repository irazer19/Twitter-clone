from flask_wtf import FlaskForm
from wtforms import TextAreaField, validators


class Tweet(FlaskForm):
	""" Creating tweet form """
	tweet = TextAreaField('Tweet', [validators.Required()])