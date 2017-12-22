from twitter import db


class Tweets(db.Model):
    """ Creating the table tweets for storing all the user tweets """
    id = db.Column(db.Integer, primary_key=True)
    tweet = db.Column(db.String(500))
    username = db.Column(db.String(80))
    retweet = db.Column(db.Integer)
    likes = db.Column(db.Integer)
    email = db.Column(db.String(80))
    profile_photo = db.Column(db.String(80))
    date = db.Column(db.String(30))

    def __init__(self, tweet, username, email, profile_photo, date, retweet=0, likes=0):
        """ Initializing the table tweets """
        self.tweet = tweet
        self.username = username
        self.email = email
        self.profile_photo = profile_photo
        self.retweet = retweet
        self.likes = likes
        self.date = date

class Followers(db.Model):
    """ Creating the table followers to store all the followers of each user """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    followers = db.Column(db.String(80))
    date = db.Column(db.String(30))

    def __init__(self, username, followers, date):
        """ Initializing the table followers """
        self.username = username
        self.followers = followers
        self.date = date

class Following(db.Model):
    """ Creating the table following to store all the user who is following others """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    following = db.Column(db.String(80))

    def __init__(self, username, following):
        """ Initializing the table following """
        self.username = username
        self.following = following


class Notifications(db.Model):
    """ Creating the table notifications to store all the user notifications and delete
        them after they are checked """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    follower_name = db.Column(db.String(80))

    def __init__(self, username, follower_name):
        """ Initialzing the table notifications """
        self.username = username
        self.follower_name = follower_name