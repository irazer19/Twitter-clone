from twitter import app, db, login_manager
from flask import render_template, session, redirect, url_for
from timeline.forms import Tweet
from user.models import Signup
from timeline.models import Tweets
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date
import random


@login_manager.user_loader
def load_user(user_id):
    return Signup.query.filter_by(id=user_id).first()


@app.route('/timeline/<username>', methods=['GET', 'POST'])
@login_required
def timeline(username):
    """ Creating the view for timeline like tweets and displaying them """
    form = Tweet()
    user = Signup.query.filter_by(id=current_user.id).first()
    if form.validate_on_submit():
        tweet = Tweets(form.tweet.data, user.username, date.today().strftime('%d %B, %Y'))
        db.session.add(tweet)
        db.session.commit()

    tweets = Tweets.query.filter_by(username=username).all()
    user_profile = user.profile.first()
    total_tweets = len(tweets)
    users = Signup.query.all()
    display_users = []
    for i in range(3):
        display_users.append(random.choice(users))

    return render_template('timeline/timeline.html', 
                            form=form, tweets=tweets, 
                            display_users=display_users, 
                            total_tweets=total_tweets,
                            user_profile=user_profile)


@app.route('/profile/<username>')
def profile(username):
    return 'profile'


@app.route('/notifications/<username>')
def notifications(username):
    return 'notifications'