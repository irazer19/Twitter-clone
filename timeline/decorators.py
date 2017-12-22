from flask_login import current_user
from flask import abort
from functools import wraps


def is_user(f):
    """ Creating the decorator function to check if the page belongs to the original user """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if kwargs['username'] == current_user.username:
            return f(*args, **kwargs)
        else:
            return abort(403, "Be a good person and don't peek in others businesss!!!")
    return wrapper