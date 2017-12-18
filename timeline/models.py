from twitter import db

class Tweets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tweet = db.Column(db.String(500))
    username = db.Column(db.String(80))
    retweet = db.Column(db.Integer)
    likes = db.Column(db.Integer)
    date = db.Column(db.String(40))

    def __init__(self, tweet, username, date, retweet=0, likes=0):
        self.tweet = tweet
        self.username = username
        self.retweet = retweet
        self.likes = likes
        self.date = date




