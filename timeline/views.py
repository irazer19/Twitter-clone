from twitter import app, db, login_manager
from flask import render_template, session, redirect, url_for, request
from timeline.forms import Tweet
from user.models import Signup
from timeline.models import Tweets, Followers, Following
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date
import random
import json
import requests


@login_manager.user_loader
def load_user(user_id):
    return Signup.query.filter_by(id=user_id).first()


@app.route('/timeline/<username>', methods=['GET', 'POST'])
@login_required
def timeline(username):
    """ Creating the view for timeline like tweets and displaying them """
    form = Tweet()
    user = Signup.query.filter_by(id=current_user.id).first()
    #Creating tweet and posting them
    if form.validate_on_submit():
        tweet = Tweets(form.tweet.data, user.username, date.today().strftime('%d %B, %Y'))
        db.session.add(tweet)
        db.session.commit()
    # Generating all the self made tweets
    tweets = Tweets.query.filter_by(username=username).all()
    user_profile = user.profile.first()
    #Finding the total number of tweets
    total_tweets = len(tweets)
    users = Signup.query.filter(Signup.username!=user.username).all()
    # Storing the instance of each user tweets in a list and sending it to the html file
    following_tweets = []
    following = Following.query.filter_by(username=user.username).all()
    for following_user in following:
        user_tweets = Tweets.query.filter_by(username=following_user.following).all()
        #Appending all the tweets made by a single user in a list!
        following_tweets.append(user_tweets)
    # Displaying the 'who to follow' section and including 3 random real users in it
    display_users = []
    for i in range(3):
        temp = []
        user = random.choice(users)
        temp.append(user)
        if Following.query.filter_by(username=current_user.username, following=user.username).first():
            temp.append('Unfollow')
        else:
            temp.append('Follow')
        display_users.append(temp)


    return render_template('timeline/timeline.html', 
                            form=form, tweets=tweets, 
                            display_users=display_users, 
                            total_tweets=total_tweets,
                            user_profile=user_profile,
                            following_tweets=following_tweets)


@app.route('/fname', methods=['POST'])
def fname():
    """ Creating an ajax request function that accepts username that follows """
    obj = request.json['username']
    # Checking is the user is already following that person
    # IF yes then remove the unfollow him.
    followed_person = obj
    if Following.query.filter_by(username=current_user.username, following=followed_person).first():
        followers = Followers.query.filter_by(username=followed_person, followers=current_user.username).first()
        following = Following.query.filter_by(username=current_user.username, following=followed_person).first()
        db.session.delete(followers)
        db.session.delete(following)
        db.session.commit()
        return 'Follow'
    # Following the person on click of follow and adding them in tables
    else:
        following_person = current_user.username
        followers = Followers(followed_person, following_person)
        following = Following(following_person, followed_person)
        db.session.add(followers)
        db.session.add(following)
        db.session.commit()
        return 'Unfollow'

@app.route('/profile/<username>')
def profile(username):
    return 'profile'


@app.route('/notifications/<username>')
def notifications(username):
    return 'notifications'