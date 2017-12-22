"""Creating models for storing User information"""
from twitter import db
from flask_login import UserMixin


class Signup(UserMixin, db.Model):
    """Creating a table for storing user registered info"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(30))
    password = db.Column(db.String(80))
    date = db.Column(db.String(30))
    profile = db.relationship('Profile', backref='signup', lazy='dynamic')


    def __init__(self, username, email, password, date):
        """Initialzing the class variables"""
        self.username = username
        self.email = email
        self.password = password
        self.date = date

    def __repr__(self):
        """ Representation of the user instance """
        return '<User {}>'.format(self.username)


class Profile(db.Model):
    """ Creating the table for storing User profile personal information """
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.String(80))
    location = db.Column(db.String(80))
    website = db.Column(db.String(80))
    profile_photo = db.Column(db.String(80))
    header_photo = db.Column(db.String(80))
    tweets = db.Column(db.Integer)
    following = db.Column(db.Integer)
    followers = db.Column(db.Integer)
    signup_id = db.Column(db.Integer, db.ForeignKey('signup.id'))

    def __init__(self, signup_id, bio='Hi there!', location='',
                       website='', profile_photo='sample_photo.svg',
                       header_photo='sample_header.jpg', tweets=0,
                       following=0, followers=0):
        """ Initializing the table profile"""
        self.bio = bio
        self.location = location
        self.website = website
        self.profile_photo = profile_photo
        self.header_photo = header_photo
        self.tweets = tweets
        self.following = following
        self.followers = followers
        self.signup_id = signup_id
