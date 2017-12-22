from twitter import app, db, login_manager, photos
from flask import render_template, session, redirect, url_for, request
from timeline.forms import Tweet
from user.forms import ProfileForm
from user.models import Signup, Profile
from timeline.models import Tweets, Followers, Following, Notifications
from timeline.decorators import is_user
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date
import random
import json
import requests


@login_manager.user_loader
def load_user(user_id):
    """ Function to return the current user instance """
    return Signup.query.filter_by(id=user_id).first()


@app.route('/timeline/<username>', methods=['GET', 'POST'])
@login_required
@is_user
def timeline(username):
    """ Creating the view for timeline like tweets and displaying them """
    form = Tweet()
    user = Signup.query.filter_by(id=current_user.id).first()
    total_notifications = 0
    # Extracting profile photo and header photo url
    profile = Profile.query.filter_by(signup_id=current_user.id).first()
    profile_url = '/static/images/{}'.format(profile.profile_photo)
    header_url = '/static/images/{}'.format(profile.header_photo)
    #Creating tweet and posting them
    if request.method == 'POST' and form.validate_on_submit():
        tweet = Tweets(form.tweet.data, user.username, user.email, profile_url, date.today().strftime('%d %B, %Y'))
        db.session.add(tweet)
        db.session.commit()
        return redirect(url_for('timeline', username=user.username))

    # Checking Notifications
    if Notifications.query.filter_by(username=username).first():
        notifications = Notifications.query.filter_by(username=username).all()
        total_notifications = len(notifications)

    # Generating all the self made tweets
    tweets = Tweets.query.filter_by(username=username).order_by(Tweets.id.desc()).all()
    total_attrib = []
    #Finding the total number of tweets
    total_attrib.append(len(tweets))
    users = Signup.query.filter(Signup.username!=user.username).all()
    # Storing the instance of each user tweets in a list and sending it to the html file
    following_tweets = []
    following = Following.query.filter_by(username=user.username).all()
    total_attrib.append(len(following))
    followers = Followers.query.filter_by(username=user.username).all()
    total_attrib.append(len(followers))
    for following_user in following:
        temp = []
        signup_following = Signup.query.filter_by(username=following_user.following).first()
        following_url = '/static/images/{}'.format(signup_following.profile.first().profile_photo)
        user_tweets = Tweets.query.filter_by(username=following_user.following).order_by(Tweets.id.desc()).all()
        #Appending all the tweets made by a single user in a list!
        temp.append(user_tweets)
        temp.append(following_url)
        following_tweets.append(temp)
    # Displaying the 'who to follow' section and including 3 random real users in it
    display_users = []
    if users:
        for i in range(3):
            temp = []
            user = random.choice(users)
            signup_url = Signup.query.filter_by(username=user.username).first()
            user_url = '/static/images/{}'.format(signup_url.profile.first().profile_photo)
            temp.append(user)
            if Following.query.filter_by(username=current_user.username, following=user.username).first():
                temp.append('Unfollow')
            else:
                temp.append('Follow')
            temp.append(user_url)
            display_users.append(temp)


    return render_template('timeline/timeline.html', 
                            form=form, tweets=tweets, 
                            display_users=display_users, 
                            total_attrib=total_attrib,
                            profile=profile,
                            profile_url=profile_url,
                            header_url=header_url,
                            following_tweets=following_tweets,
                            total_notifications=total_notifications)


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
        followers = Followers(followed_person, following_person, date.today().strftime('%d %B, %Y'))
        # Stroing the notification
        notifications = Notifications(followed_person, following_person)
        following = Following(following_person, followed_person)
        db.session.add(followers)
        db.session.add(following)
        db.session.add(notifications)
        db.session.commit()
        return 'Unfollow'


@app.route('/likes', methods=['POST'])
def likes():
    """Creating method to handle ajax for number of tweet likes"""
    data = request.json['like']
    tid = request.json['id']
    tweet = Tweets.query.filter_by(id=tid).first()
    # Checking if likes are added or subtracted
    if data == 'True':
        tweet.likes = tweet.likes + 1
        db.session.commit()
        return 'success'
    else:
        tweet.likes = tweet.likes - 1
        db.session.commit()
        return 'success'

@app.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    """ Creating the fucntion profile to process and display all the actions on 
        profile page/template """
    # Creating instances of Forms
    form = ProfileForm(username=username)
    form_tweet = Tweet()
    signup = Signup.query.filter_by(username=username).first()
    profile = Profile.query.filter_by(signup_id=signup.id).first()
    # Storing the photo urls
    profile_url = '/static/images/{}'.format(profile.profile_photo)
    header_url = '/static/images/{}'.format(profile.header_photo)

    # Logic for uploading photos and redirecting them after editing the profile
    if request.method == 'POST' and form.validate_on_submit():
        try:
            profile_name = photos.save(request.files['profile_photo'])
            profile_url = '/static/images/{}'.format(profile_name)
            profile.profile_photo = profile_name
        except:
            pass

        try:
            header_name = photos.save(request.files['header_photo'])
            header_url = '/static/images/{}'.format(header_name)
            profile.header_photo = header_name
        except:
            pass

        signup.username = form.username.data
        profile.bio = form.bio.data
        profile.location = form.location.data
        profile.website = form.website.data
        db.session.commit()
        return redirect(url_for('profile', username=username))
    # Find the total number of tweets
    total_likes = 0
    tweets = Tweets.query.filter_by(username=username).order_by(Tweets.id.desc()).all()
    for tweet in tweets:
        total_likes = total_likes + tweet.likes
    users = Signup.query.filter(Signup.username!=current_user.username).all()
    # finding the total number of followers and following and tweets
    total_attrib = []
    total_attrib.append(len(tweets))
    following = Following.query.filter_by(username=username).all()
    total_attrib.append(len(following))
    followers = Followers.query.filter_by(username=username).all()
    total_attrib.append(len(followers))
    # Displaying the 'who to follow' section and including 3 random real users in it
    display_users = []
    if users:
        for i in range(3):
            temp = []
            user = random.choice(users)
            signup_url = Signup.query.filter_by(username=user.username).first()
            user_url = '/static/images/{}'.format(signup_url.profile.first().profile_photo)
            temp.append(user)
            if Following.query.filter_by(username=current_user.username, following=user.username).first():
                temp.append('Unfollow')
            else:
                temp.append('Follow')
            temp.append(user_url)
            display_users.append(temp)
    return render_template('timeline/profile.html', tweets=tweets,
                                                    display_users=display_users,
                                                    total_attrib=total_attrib,
                                                    profile=profile,
                                                    total_likes=total_likes,
                                                    form=form,
                                                    profile_url=profile_url,
                                                    header_url=header_url,
                                                    form_tweet=form_tweet)


@app.route('/notifications/<username>')
@is_user
def notifications(username):
    """ Function to process all the actions on the page notifications """
    profile = Profile.query.filter_by(signup_id=current_user.id).first()
    form_tweet = Tweet()
    # Storing the profile photo url of the respective user
    profile_url = '/static/images/{}'.format(profile.profile_photo)
    # Displaying all the users that followed the current user
    followers = Followers.query.filter_by(username=current_user.username).order_by(Followers.id.desc()).all()
    total_followers = []
    for follower in followers:
        follow = []
        follower_user = Signup.query.filter_by(username=follower.followers).first()
        follower_profile = Profile.query.filter_by(signup_id=follower_user.id).first()
        follower_url = '/static/images/{}'.format(follower_profile.profile_photo)
        follow.append(follower)
        follow.append(follower_url)
        total_followers.append(follow)

    # Deleting all the Notifications of the current user.
    notif_del = Notifications.query.filter_by(username=username).delete()
    db.session.commit()

    # Displaying the 'who to follow' section and including 3 random real users in it
    users = Signup.query.filter(Signup.username!=current_user.username).all()
    display_users = []
    if users:
        for i in range(3):
            temp = []
            user = random.choice(users)
            signup_url = Signup.query.filter_by(username=user.username).first()
            user_url = '/static/images/{}'.format(signup_url.profile.first().profile_photo)
            temp.append(user)
            if Following.query.filter_by(username=current_user.username, following=user.username).first():
                temp.append('Unfollow')
            else:
                temp.append('Follow')
            temp.append(user_url)
            display_users.append(temp)

    return render_template('user/notifications.html', profile_url=profile_url,
                                                      total_followers=total_followers,
                                                      display_users=display_users,
                                                      form_tweet=form_tweet)
