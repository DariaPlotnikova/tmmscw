import webapp2
from google.appengine.api import users
from google.appengine.ext import db
from models.visitor import Leader


def current_leader_user(fn):
    def wrapped(self):
        user = users.get_current_user()
        leader = db.Query(Leader).filter('user =', user).get()
        if leader:
            return fn(self)
        else:
            webapp2.abort(404)
    return wrapped
