from flask_wtf import FlaskForm
from wtforms import TextAreaField, validators

class Tweet(FlaskForm):
	"""Creating tweet form on timeline page"""
	tweet = TextAreaField('Tweet', [validators.Required()])